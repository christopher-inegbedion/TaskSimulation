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
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def main():

    while True:
        action = input("\n~Wcommand: ")

        if action == "exit":
            return False
        else:
            parse_action(action)


def parse_action(command):
    global my_user
    if command == "cu":
        return create_user()
    elif command == "cp":
        loop.run_until_complete(create_pipe())
        return
    elif command == "sp":
        loop.run_until_complete(start_pipeline())
    elif command == "sc":
        loop.run_until_complete(start_constraint())
    elif command == "stpp":
        loop.run_until_complete(stop_pipeline())


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

    addr = "ws://localhost:5000/create_pipeline"
    socket = await websockets.connect(addr)

    task_name = input("~enter task name: ")
    stages = []
    available_constraints = None
    while True:
        stage_name = input("~enter stage name: ")
        if stage_name != "x":
            print("These are the available constraints")

            if available_constraints == None:
                available_constraints = jsonpickle.decode(await socket.recv())
                
            print(available_constraints["constraints_available"])
            selected_constraints = []
            while True:
                constraints = input(
                    f"Please select the constraints for Stage {stage_name}: ")
                if constraints != "x":
                    selected_constraints.append(int(constraints))

                else:
                    break
            stages.append({"stage_name": stage_name,
                           "constraints": selected_constraints})
        else:
            break

    print(stages)

    data_to_send = {
        "user_id": my_user['id'],
        "task_name": task_name,
        "stages": stages
    }

    await socket.send(jsonpickle.encode(data_to_send))

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

        if response == "done":
            break

        print(response)


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
