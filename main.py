import json
import threading
from time import sleep, time
import jsonpickle
from task_pipeline.pipeline import Pipeline
from task_main.product_task import ProductTask
from constraints.constraint_main.custom_constraint import CustomConstraint
from constraints.models.example_models import pause_thread, time_model
from stage.stage import Stage, StageGroup
import requests
import websockets
import asyncio

my_user = None
my_pipeline_id = None


def main():

    while True:
        action = input("\ncommand: ")

        if action == "exit":
            return False
        else:
            parse_action(action)


def parse_action(command):
    global my_user
    if command == "cu":
        return create_user()
    elif command == "cp":
        asyncio.get_event_loop().run_until_complete(create_pipe())
        return
    elif command == "sp":
        asyncio.get_event_loop().run_until_complete(start_pipeline())
    elif command == "sc":
        asyncio.get_event_loop().run_until_complete(start_constraint())
    elif command == "stpp":
        asyncio.get_event_loop().run_until_complete(stop_pipeline())


def create_user():
    global my_user
    user_name = input("~enter name: ")
    my_user = perform_network_action(
        "http://localhost:8000/create/"+str(user_name), "get")
    print(
        f">[SERVER] User created with name: {my_user['name']}, ID: {my_user['id']}")
    return my_user


async def create_pipe():
    global my_user, my_pipeline_id

    if my_user == None:
        print("A user has not been created")
        return

    task_name = input("~enter task name: ")
    stages = []
    while True:
        stage_name = input("~enter stage name: ")
        if stage_name != "x":
            stages.append(stage_name)
        else:
            break
    number_of_constraints = input("~enter number of constraints: ")

    data_to_send = {
        "user_id": my_user['id'],
        "task_name": task_name,
        "stage_names": stages,
        "number_of_constraints": number_of_constraints
    }

    addr = "ws://localhost:5000/create_pipeline"
    socket = await websockets.connect(addr)
    await socket.send(json.dumps(data_to_send))

    result = jsonpickle.decode(await socket.recv())
    my_pipeline_id = result["id"]
    print(f"> Pipeline created with ID: {result['id']}")


async def start_pipeline():
    global my_pipeline_id

    if my_pipeline_id == None:
        pipeline_id = input("~enter pipeline id: ")
    else:
        pipeline_id = my_pipeline_id

    addr = "ws://localhost:5000/start"
    socket = await websockets.connect(addr)
    await socket.send(pipeline_id)

    while socket.open:
        response = await socket.recv()
        print(await socket.recv())

        if response == "done":
            break


async def start_constraint():
    global my_pipeline_id, my_user

    if my_pipeline_id == None:
        pipeline_id = input("~enter pipeline id: ")
    else:
        pipeline_id = my_pipeline_id
    constraint_name = input("~constraint name: ")
    stage_name = input("~stage name: ")

    addr = "ws://localhost:5000/start_constraint"
    data_to_send = {
        "user_id": my_user["id"],
        "pipeline_id": pipeline_id,
        "constraint_name": constraint_name,
        "stage_name": stage_name
    }

    print(f"< {data_to_send}")
    socket = await websockets.connect(addr)

    await socket.send(jsonpickle.encode(data_to_send))

    data_recv = jsonpickle.decode(await socket.recv())
    print(f"\nInput required for constraint {constraint_name}")
    if data_recv["response"]["msg"] != "done":
        response = ""

        while response != "done":
            data_input = input(f"~provide input for {constraint_name}: ")
            await socket.send(data_input)
            response = await socket.recv()
    print(f"> Constraint {constraint_name} started")


async def stop_pipeline():
    global my_pipeline_id

    if my_pipeline_id == None:
        pipeline_id = input("~enter pipeline id: ")
    else:
        pipeline_id = my_pipeline_id

    addr = "ws://localhost:5000/stop_pipeline"
    socket = await websockets.connect(addr)
    await socket.send(pipeline_id)

    response = await socket.recv()

    if response == "success":
        print(f"> Pipeline with id {response} stopped")
    else:
        print("> Error occured")


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


# def callback(pipeline):
#     print("update")


# con1 = CustomConstraint("constraint", pause_thread.PauseModel())
# con1.add_input(10)

# stage = Stage("PENDING")
# stage.add_constraint(con1)

# stage_group = StageGroup()
# stage_group.add_stage(stage)

# task = ProductTask("task", "desc")
# task.set_constraint_stage_config(stage_group)

# pipeline = Pipeline(task, stage_group)
# pipeline.on_update(
#     callback
# )
# pipeline.start()


# sleep(2)
# pipeline.start_constraint("PENDING", "constraint")

main()
