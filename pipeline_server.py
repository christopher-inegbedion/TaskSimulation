from asyncio.events import new_event_loop
import concurrent.futures
import asyncio
from concurrent.futures import thread
import threading
from constraints.constraint_main.custom_constraint import CustomConstraint
from constraints.models.example_models.pause_thread import PauseModel
from constraints.models.example_models.time_model import TimeModel
from constraints.models.example_models.test_model import TestModel
from task_main.task import Task
import websockets
from task_pipeline.pipeline import Pipeline
from stage.stage import Stage, StageGroup
import json
import jsonpickle
from internet_model import InternetModel
import nest_asyncio
nest_asyncio.apply()


pipelines = {}
models = [
    PauseModel(),
    TimeModel(),
    TestModel()
]

all_constraints = [
    CustomConstraint("con1", InternetModel()),
    CustomConstraint("con2", PauseModel()),
    CustomConstraint("con3", PauseModel()),
    CustomConstraint("con4", PauseModel()),
    CustomConstraint("con5", PauseModel()),
    CustomConstraint("con6", PauseModel())
]

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

print("\nStarted Pipeline websocket server...")


def create_pipeline(user_id, task_name, stage_names, number_of_constraints):
    stage_group = StageGroup()

    task = Task(task_name, "desc")

    for stage_name in stage_names:
        s = Stage(stage_name)

        # select the first n(number_of_constraints) constraints from constraints list
        for n in range(number_of_constraints):
            constraint = CustomConstraint(f"con{n}", models[n])
            s.add_constraint(constraint)

        stage_group.add_stage(s)

    task.set_constraint_stage_config(stage_group)
    pipeline = Pipeline(task, stage_group)
    pipeline.set_provider_id(user_id)

    return pipeline


def callback(pipe, args):
    global loop
    loop.run_until_complete(
        call(args[0], pipe.current_stage.log.most_recent_update["msg"]))


def close(pipe, args):
    global loop
    loop.run_until_complete(_close(args[0]))


async def _close(websocket):
    await websocket.send("done")
    print(f"< Pipeline completed")


async def call(websocket, msg):
    await websocket.send(msg)


async def launch(websocket, path):
    global pipelines, all_constraints

    if path == "/create_pipeline":
        stage_group = StageGroup()

        available_constraints = {"constraints_available": []}
        for i in all_constraints:
            available_constraints["constraints_available"].append(i.name)

        await websocket.send(jsonpickle.encode(available_constraints))

        data = jsonpickle.decode(await websocket.recv())
        user_id = data["user_id"]
        task_name = data["task_name"]
        all_stages = data["stages"]
        for i in all_stages:
            stage_name = i["stage_name"]
            constraints = i["constraints"]

            new_stage = Stage(stage_name)
            for constr_selected in constraints:
                constraint = all_constraints[constr_selected]
                new_stage.add_constraint(constraint)

            stage_group.add_stage(new_stage)

        pipeline = Pipeline(task_name, stage_group)
        pipelines[pipeline.id] = pipeline

        print(
            f"< User with ID: {user_id} created Pipeline with ID: {pipeline.id}")
        print(len(pipeline.constraint_config.stages))

        print("\n< Pipeline created with the following stages:")
        for stage in pipeline.constraint_config.stages:
            print(f"- Stage name: {stage.name}")
            for constraint in stage.constraints:
                print(f"\t- Constraint name: {constraint.name}")

        data_to_send = {
            "id": pipeline.id
        }

        await websocket.send(jsonpickle.encode(data_to_send))
    elif path == "/start":
        recv_pipeline_id = await websocket.recv()

        if recv_pipeline_id in pipelines:
            pipeline: Pipeline = pipelines[recv_pipeline_id]
            pipeline.on_update(callback, websocket)
            pipeline.on_complete(close, websocket)

            pipeline.start()

            while websocket.open:
                await asyncio.sleep(0)
        else:
            await websocket.send("cannot be found")
    elif path == "/start_constraint":
        recv_data = jsonpickle.decode(await websocket.recv())
        pipeline_id = recv_data["pipeline_id"]
        user_id = recv_data["user_id"]
        constriant_name = recv_data["constraint_name"]
        stage_name = recv_data["stage_name"]

        if pipeline_id in pipelines:
            pipeline: Pipeline = pipelines[pipeline_id]

            # check if constraint requires input
            if pipeline.is_input_req_for_constraint(constriant_name, stage_name):
                await websocket.send(jsonpickle.encode({"response": {
                    "msg": "input_required",
                    "input_count": pipeline.get_number_of_inputs_required_by_constraints(constriant_name, stage_name)
                }}))

                number_of_constraints_inputs = pipeline.get_number_of_inputs_required_by_constraints(
                    constriant_name, stage_name)
                for i in range(number_of_constraints_inputs):
                    input_recv = await websocket.recv()
                    pipeline.add_input_to_constraint(
                        constriant_name, stage_name, input_recv)

                    if i == number_of_constraints_inputs-1:
                        await websocket.send("done")
                    else:
                        await websocket.send("not done")

                pipeline.start_constraint(stage_name, constriant_name)
        else:
            print(
                f"User with ID: {user_id} started Constraint with name {constriant_name}")
            await websocket.send({"response": {
                "msg": "done"
            }})
    elif path == "/stop_pipeline":
        recv_id = await websocket.recv()

        if recv_id in pipelines:
            pipeline = pipelines[recv_id]
            pipeline.abort()
            await websocket.send("success")
        else:
            await websocket.send("fail")

start_server = websockets.serve(launch, "localhost", 5000)

loop.run_until_complete(start_server)
loop.run_forever()
