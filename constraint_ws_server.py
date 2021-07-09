import asyncio
import json
import threading
from constraints.constraint_main.constraint import Constraint
from constraints.enums.input_type import InputType
from constraints.enums.stage_status import StageStatus
import requests
from constraints.models.example_models.pause_thread import PauseModel
import jsonpickle
from stage.stage import Stage, StageGroup
from task_main.task import Task
from task_pipeline.pipeline import Pipeline
from internet_model import InternetModel
from constraints.constraint_main.custom_constraint import CustomConstraint
from product_description_model import ProductDescriptionModel
import websockets
import nest_asyncio
from rich.traceback import install

install()
nest_asyncio.apply()

all_pipelines = {}
all_pipeline_details = {}
all_pipeline_owner_websockets = {}

task_session_count_mutex = threading.Lock()
task_session_pending_users_mutex = threading.Lock()
task_session_active_users_mutex = threading.Lock()
task_session_complete_users_mutex = threading.Lock()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

print("Started Pipeline server")


def create_constraint(constraint_name):
    if constraint_name == "Exchange rate":
        return CustomConstraint("Exchange rate", "View the current exchange rate between 2 currencies", InternetModel())
    elif constraint_name == "Pause":
        return CustomConstraint("Pause", "A constraint to pause", PauseModel())
    elif constraint_name == "Product description":
        return CustomConstraint("Product description", "View the product's basic information", ProductDescriptionModel())


def event_handler(pipe, args):
    global loop
    loop.run_until_complete(event_handler_implementation(args[0], pipe))


async def event_handler_implementation(websocket, pipe: Pipeline):
    await websocket.send(jsonpickle.encode(pipe.current_stage.log.most_recent_update))


def stage_complete_handler(pipe: Pipeline, args):
    global loop
    task_id = args[0]
    user_id = args[1]
    event = pipe.current_stage.log.most_recent_update

    if event["event"] == "STAGE_COMPLETED":
        if event["value"] == "Pending":
            loop.run_until_complete(update_session_count(task_id))
            loop.run_until_complete(
                update_pending_users_count(task_id, user_id))
        elif event["value"] == "Active":
            loop.run_until_complete(
                update_active_users_count(task_id, user_id))
        elif event["value"] == "Complete":
            loop.run_until_complete(
                update_complete_users_count(task_id, user_id))


async def update_session_count(task_id):
    global all_pipeline_details
    task_session_count_mutex.acquire()
    session_count = all_pipeline_details[task_id]["session_count"]
    new_sess_count = session_count+1
    all_pipeline_details[task_id]["session_count"] = new_sess_count
    print("session count increased...")
    task_session_count_mutex.release()

    print("session counnt increment message sent...")
    if task_id in all_pipeline_owner_websockets:
        await all_pipeline_owner_websockets[task_id].send(jsonpickle.encode({"event": "count", "data": new_sess_count}))


async def update_pending_users_count(task_id, user_id):
    global all_pipeline_details
    task_session_pending_users_mutex.acquire()
    if user_id not in all_pipeline_details[task_id]["pending_users"]:
        all_pipeline_details[task_id]["pending_users"].append(user_id)
        print(f"User with ID: {user_id} started Pending stage")
    task_session_pending_users_mutex.release()

    if task_id in all_pipeline_owner_websockets:
        await all_pipeline_owner_websockets[task_id].send(jsonpickle.encode({"event": "new_pending_user", "data": user_id}))


async def update_active_users_count(task_id, user_id):
    global all_pipeline_details
    task_session_active_users_mutex.acquire()
    if user_id not in all_pipeline_details[task_id]["active_users"]:
        all_pipeline_details[task_id]["active_users"].append(user_id)
        print(f"User with ID: {user_id} started Active stage")
    task_session_active_users_mutex.release()

    if task_id in all_pipeline_owner_websockets:
        await all_pipeline_owner_websockets[task_id].send(jsonpickle.encode({"event": "new_active_user", "data": user_id}))


async def update_complete_users_count(task_id, user_id):
    global all_pipeline_details
    task_session_complete_users_mutex.acquire()
    if user_id not in all_pipeline_details[task_id]["complete_users"]:
        all_pipeline_details[task_id]["complete_users"].append(user_id)
        print(f"User with ID: {user_id} started Complete stage")
    task_session_complete_users_mutex.release()

    if task_id in all_pipeline_owner_websockets:
        await all_pipeline_owner_websockets[task_id].send(jsonpickle.encode({"event": "new_complete_user", "data": user_id}))


def get_constraint_config_inputs(constraint_name, stage_name, stage_group_id):
    stage_data = perform_network_action(
        "http://localhost:8000/stage_group/"+stage_group_id + "/"+stage_name, "get")
    all_constraints = stage_data["constraints"]
    for constraint in all_constraints:
        if constraint["constraint_name"] == constraint_name:
            if constraint["config_inputs"] == {}:
                return None

            return constraint["config_inputs"]

    return None


async def launch(websocket, path):
    global all_pipeline_details, all_pipelines, all_pipeline_owner_websockets
    if path == "/start_pipeline":
        data = jsonpickle.decode(await websocket.recv())
        user_id = data["user_id"]
        stage_name = data["stage_name"]
        task_id = data["task_id"]
        print(f"start pipeline command. User ID: {user_id}...")

        if user_id not in all_pipelines[task_id]["sessions"]:
            print(f"Creating new pipeline instance for user: {user_id}")
            # Get the task's details from the DB
            task_data = perform_network_action(
                "http://localhost:8000/task/"+task_id, "get")
            task_name = task_data["name"]
            task_desc = task_data["desc"]
            stage_group_id = task_data["stage_group_id"]
            if task_data["msg"] == "success":
                print("Task details retrieved from database...")
                try:
                    new_task = Task(task_name, task_desc)
                    stage_group_data = perform_network_action(
                        "http://localhost:8000/stage_group/"+stage_group_id, "get")
                    print("Stage group details retrieved from database...")
                    new_stage_groups = StageGroup()
                    stages = stage_group_data["stages"]
                    for stage in stages:
                        new_stage = Stage(stage["stage_name"])
                        for constraint in stage["constraints"]:
                            constraint_details: Constraint = create_constraint(
                                constraint)

                            new_constraint = CustomConstraint(
                                constraint_details.name, constraint_details.description, constraint_details.model)
                            config_inputs = get_constraint_config_inputs(
                                constraint_details.name, stage_name, stage_group_id)
                            if config_inputs != None:
                                for i in config_inputs:
                                    new_constraint.add_configuration_input(
                                        config_inputs[i])

                            new_stage.add_constraint(new_constraint)
                        new_stage_groups.add_stage(new_stage)

                    new_task.set_constraint_stage_config(new_stage_groups)
                    pipeline = Pipeline(new_task, new_stage_groups)
                    # ^ Task and Pipeline object have been created

                    # Save the pipeline object for the user and initialize it in all_pipeline_details
                    all_pipelines[task_id]["sessions"][user_id] = pipeline

                    print("pipeline created...")
                    pipeline.start()
                    pipeline.on_stage_complete(
                        stage_complete_handler,  task_id, user_id, stage_name="",)
                    print(f"Stage: {stage_name} started...")
                    print()

                    await websocket.send(jsonpickle.encode({
                        "result": "success"
                    }))
                except Exception as e:
                    print(e)
                    await websocket.send(jsonpickle.encode({
                        "result": "fail"
                    }))

    elif path == "/start_constraint1":
        data = jsonpickle.decode(await websocket.recv())
        user_id = data["user_id"]
        constraint_name = data["constraint_name"]
        stage_name = data["stage_name"]
        task_id = data["task_id"]
        print(
            f"command to start constraint: [{constraint_name}] in stage: [{stage_name}] with task id: [{task_id}]")

        pipeline = all_pipelines[task_id]["sessions"][user_id]

        print("starting constraint...")
        constraint = pipeline.get_constraint(constraint_name, stage_name)

        # Check if the constraint requires input
        is_constraint_input_required = constraint.model.input_count != 0

        print("requesting input...")
        print()

        if is_constraint_input_required:
            print(f"constraint [{constraint_name}] requires input")

            # Request input
            await websocket.send(
                jsonpickle.encode({
                    "event": "INPUT_REQUIRED",
                    "value": {"input_count": constraint.model.input_count, "input_type": str(constraint.model.input_type)}
                })
            )
        else:
            print(f"constraint [{constraint_name}] does not require input")

            await websocket.send(
                jsonpickle.encode({
                    "event": "INPUT_NOT_REQUIRED"
                })
            )

            pipeline.start_constraint(stage_name, constraint_name)

    elif path == "/start_constraint2":
        # receive constraint input data
        constraint_inputs = jsonpickle.decode(await websocket.recv())

        data = constraint_inputs["data"]
        user_id = constraint_inputs["user_id"]
        constraint_name = constraint_inputs["constraint_name"]
        stage_name = constraint_inputs["stage_name"]
        task_id = constraint_inputs["task_id"]
        print(
            f"data recieved for constraint: [{constraint_name}] in stage: [{stage_name}] with task id: [{task_id}]")

        if task_id == None:
            raise Exception(f"Task with ID: {task_id} cannot be found")

        if user_id == None:
            raise Exception(f"User with ID: {user_id} cannot be found")

        pipeline: Pipeline = all_pipelines[task_id]["sessions"][user_id]
        print(f"running for stage: {stage_name}")
        constraint_obj = pipeline.get_constraint(
            constraint_name, stage_name)

        if constraint_inputs["response"] == "INPUT_REQUIRED":
            for constraint_input in data:
                if constraint_obj.model.input_type == InputType.INT:
                    constraint_obj.add_input(int(constraint_input))
                elif constraint_obj.model.input_type == InputType.STRING:
                    constraint_obj.add_input(str(constraint_input))
                else:
                    constraint_obj.add_input(constraint_input)

        pipeline.start_constraint(stage_name, constraint_name)
        print()

    elif path == "/on_constraint_complete":
        constraint_inputs = jsonpickle.decode(await websocket.recv())
        constraint_name = constraint_inputs["constraint_name"]
        stage_name = constraint_inputs["stage_name"]
        task_id = constraint_inputs["task_id"]
        user_id = constraint_inputs["user_id"]

        pipeline = all_pipelines[task_id]["sessions"][user_id]
        pipeline.on_constraint_complete(
            event_handler, websocket, constraint_name)
        print(f"client listening to {constraint_name} changes")
        print()

    elif path == "/constraint_detail":
        data = jsonpickle.decode(await websocket.recv())
        constraint_name = data["constraint_name"]
        stage_name = data["stage_name"]
        task_id = data["task_id"]
        user_id = data["user_id"]
        pipeline = all_pipelines[task_id]["sessions"][user_id]
        constraint = pipeline.get_constraint(constraint_name, stage_name)

        value = {
            "status": constraint.get_status().value,
            "required": constraint.model.input_count != 0
        }

        await websocket.send(jsonpickle.encode(value))

    elif path == "/is_stage_running":
        constraint_inputs = jsonpickle.decode(await websocket.recv())
        stage_name = constraint_inputs["stage_name"]
        task_id = constraint_inputs["task_id"]
        user_id = constraint_inputs["user_id"]

        print(f"user: {user_id} checking if {stage_name} is running...")
        # Check if a session has been created for the task with id [task_id]
        if task_id not in all_pipelines:
            all_pipelines[task_id] = {"sessions": {}}
            all_pipeline_details[task_id] = {"session_count": 0, "pending_users": [
            ], "active_users": [], "complete_users": []}

        if user_id in all_pipelines[task_id]["sessions"]:
            pipeline = all_pipelines[task_id]["sessions"][user_id]
            stage = pipeline.get_stage(stage_name)
            print(f"{stage_name} -> {pipeline.get_stage(stage_name).status}")

            if pipeline.get_stage(stage_name).status == StageStatus.COMPLETE:
                await websocket.send(jsonpickle.encode({"value": "complete"}))
            elif pipeline.get_stage(stage_name).status == StageStatus.ACTIVE:
                await websocket.send(jsonpickle.encode({"value": "running"}))
            elif pipeline.get_stage(stage_name).status == StageStatus.NOT_STARTED:
                await websocket.send(jsonpickle.encode({"value": "not_started"}))
        else:
            await websocket.send(jsonpickle.encode({"value": "not_started"}))
            print(f"{stage_name} has not started")
        print()

    elif path == "/is_pipe_running":
        data = jsonpickle.decode(await websocket.recv())
        task_id = data["task_id"]
        user_id = data["user_id"]

        if user_id in all_pipelines[task_id]["sessions"]:
            pipeline = all_pipelines[task_id]["sessions"][user_id]
            if pipeline.current_stage != None:
                await websocket.send(jsonpickle.encode({"value": "running"}))
            else:
                await websocket.send(jsonpickle.encode({"value": "not_running"}))
        else:
            await websocket.send(jsonpickle.encode({"value": "not_running"}))

    elif path == "/connect_task_details":
        task_id = jsonpickle.decode(await websocket.recv())["task_id"]
        all_pipeline_owner_websockets[task_id] = websocket
        print("client listening to task session added...")

    elif path == "/disconnect_task_details":
        task_id = jsonpickle.decode(await websocket.recv())["task_id"]

        if task_id in all_pipeline_owner_websockets:
            all_pipeline_owner_websockets.pop(task_id)
            print("client listening to session removed")

    elif path == "/pipeline_details":
        data = jsonpickle.decode(await websocket.recv())
        user_id = data["user_id"]
        task_id = data["task_id"]

        pipeline: Pipeline = all_pipelines[task_id]["sessions"][user_id]
        data = pipeline.get_stage_group_details()
        await websocket.send(jsonpickle.encode({"value": data}))

    elif path == "/pipeline_session_admin_details":
        data = jsonpickle.decode(await websocket.recv())
        task_id = data["task_id"]

        if task_id in all_pipeline_details:
            pipeline_details = all_pipeline_details[task_id]
            data_to_send = {"session_count": pipeline_details["session_count"], "pending_users": pipeline_details["pending_users"],
                            "active_users": pipeline_details["active_users"], "complete_users": pipeline_details["complete_users"]}
            await websocket.send(jsonpickle.encode(data_to_send))

    elif path == "/next_constraint_or_stage":
        data = jsonpickle.decode(await websocket.recv())
        current_constraint = data["constraint_name"]
        current_stage = data["stage_name"]
        user_id = data["user_id"]
        task_id = data["task_id"]

        pipeline: Pipeline = all_pipelines[task_id]["sessions"][user_id]

        await websocket.send(jsonpickle.encode(pipeline.get_next_constraint_or_stage(current_stage, current_constraint)))

    elif path == "/constraint_configuration_details":
        data = jsonpickle.decode(await websocket.recv())
        user_id = data["user_id"]
        task_id = data["task_id"]
        current_constraint = data["constraint_name"]
        current_stage = data["stage_name"]

        config_inputs = {"data": "datadata", "data2": "data2data2"}
        await websocket.send(jsonpickle.encode(config_inputs))

    while websocket.open:
        await asyncio.sleep(0)


def perform_network_action(addr, method, data=None):
    if method == "get":
        r = requests.get(addr)

    elif method == "post":
        r = requests.post(addr, data=data)

    if r.status_code == 200:
        result = r.json()
        return result
    else:
        return None


start_server = websockets.serve(launch, "0.0.0.0", 4321)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
