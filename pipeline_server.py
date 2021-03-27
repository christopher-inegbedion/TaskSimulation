import asyncio
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

pipelines = {}
models = [
    PauseModel(),
    TimeModel(),
    TestModel()
]


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


async def callback(pipe, args):
    await args[0].send("msg")


async def launch(websocket, path):
    global pipelines

    if path == "/create_pipeline":
        recv_data = json.loads(await websocket.recv())
        user_id = recv_data["user_id"]
        task_name = recv_data["task_name"]
        stage_names = recv_data["stage_names"]
        number_of_constraints = int(recv_data["number_of_constraints"])

        pipeline = create_pipeline(user_id,
                                   task_name, stage_names, number_of_constraints)
        pipelines[pipeline.id] = pipeline

        print(
            f"< User with ID: {user_id} created Pipeline with ID: {pipeline.id}")

        for stage in pipeline.constraint_config.stages:
            print(f"\n> Stage name: {stage.name}")
            for constraint in stage.constraints:
                print(f"\t> Constraint name: {constraint.name}")

        data_to_send = {
            "id": pipeline.id
        }

        await websocket.send(jsonpickle.encode(data_to_send))
    elif path == "/start":
        recv_pipeline_id = await websocket.recv()

        if recv_pipeline_id in pipelines:
            pipeline: Pipeline = pipelines[recv_pipeline_id]
            pipeline.start()

            send_msg = False
            while websocket.open:
                await asyncio.sleep(0.1)
                pipeline.on_update(True, callback, websocket)

                if send_msg:
                    send_msg = False
                    await websocket.send("msg")
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
                        constriant_name, stage_name, int(input_recv))

                    if i == number_of_constraints_inputs-1:
                        print("done here")
                        await websocket.send("done")
                    else:
                        print("done here")
                        await websocket.send("not done")

                constraint_to_run = pipeline.get_constraint(
                    constriant_name, stage_name).inputs
                print(constraint_to_run)
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


def pipeline_callback_func(pipeline):
    global send_msg

    send_msg = True


start_server = websockets.serve(launch, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
