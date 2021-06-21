import json
import jsonpickle
import requests
import websockets
import asyncio

my_user = None
my_pipeline_id = None
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def main():
    while True:
        action = input("\n~command: ")

        if action == "exit":
            return False
        else:
            parse_action(action)


def parse_action(command):
    global my_user
    if command == "cu":  # create user
        return create_user()
    elif command == "bcv":  # build constraint view
        return build_constraint_view()
    elif command == "ct":  # create task
        return create_task()
    elif command == "scv":  # set constraint's view
        set_constraint_view()
    elif command == "cp":  # create pipeline
        loop.run_until_complete(create_pipe())
    elif command == "mcsg":  # modify stage group
        modify_stage_group()
    elif command == "csg":  # create stage group
        create_stage_group()
    elif command == "sp":  # start pipeline
        loop.run_until_complete(start_pipeline())
    elif command == "sc":  # start constraint
        loop.run_until_complete(start_constraint())
    elif command == "stpp":  # stop pipeline
        loop.run_until_complete(stop_pipeline())


def build_constraint_view():
    print("+------------------------------------------+")
    print("| This tool will build a constraint's view |")
    print("+------------------------------------------+")

    constraint_name = input("~enter the constraint name: ")

    config_model_views = []
    while True:
        print()
        print("+--------------------------------+")
        print("| Configuration model properties |")
        print("+--------------------------------+")

        config_id = input("~enter config id: ")
        bg_color = input("~enter config background color: ")
        bottom_sheet_color = input("~enter bottom sheet color: ")

        while True:
            bottom_section_can_open = input(
                "~can the bottom sheet open (1-true, 0-false): ")
            if bottom_section_can_open == "1" or bottom_section_can_open == "0":
                break

        while True:
            bottom_section_can_expand = input(
                "~can the bottom section expand (1-true, 0-false): ")
            if bottom_section_can_expand == "1" or bottom_section_can_expand == "0":
                break
        while True:
            center_top_section_data = input(
                "~should the top section view be centered (1-true, 0-false): ")
            if center_top_section_data == "1" or center_top_section_data == "0":
                break

        draggable_sheet_max_height = input(
            "~enter the draggable sheet max height: ")
        print("+--------------------------------------------------------------+")

        print()
        print("+-------------+")
        print("| Top section |")
        print("+-------------+")

        top_section = []
        while True:
            print("Add a new entry")
            config_entry_margin = input("~enter entry margin: ")
            top_section_components = []
            while True:
                print("\n\tAdd component to entry")
                component_type = input("\t~enter component type: ")
                if component_type == "x":
                    break

                print(f"\n\tEnter {component_type} component's properties")

                component_properties = []
                while True:
                    component_property = input("\t~component property: ")
                    if component_property == "x":
                        print()
                        break
                    else:
                        component_properties.append(component_property)
                component = {
                    "type": component_type,
                    "component_properties": component_properties
                }
                top_section_components.append(component)

            top_section.append({"margin": config_entry_margin,
                                "components": top_section_components})

            is_user_done_top = input(
                "~are you done adding entries to the top section? (y, n): ")
            if is_user_done_top == "y":
                break

        print()
        print("+----------------+")
        print("| Bottom section |")
        print("+----------------+")

        bottom_section = []
        while True:
            print("Add a new entry")
            config_entry_margin = input("~enter entry margin: ")
            bottom_section_components = []
            while True:
                print("\n\tAdd component to entry")
                component_type = input("\t~enter component type: ")
                if component_type == "x":
                    break

                print(f"\n\tEnter {component_type} component's properties")

                component_properties = []
                while True:
                    component_property = input("\t~component property: ")
                    if component_property == "x":
                        print()
                        break
                    else:
                        component_properties.append(component_property)
                component = {
                    "type": component_type,
                    "component_properties": component_properties
                }
                bottom_section_components.append(component)

            bottom_section.append({"margin": config_entry_margin,
                                   "components": bottom_section_components})

            is_user_done_bottom = input(
                "~are you done adding an entry to the bottom section (y, n): ")
            if is_user_done_bottom == "y":
                break

        is_user_done = input("~are you done (y, n): ")

        config_model_views.append({
            "id": config_id,
            "bg_color": bg_color,
            "bottom_sheet_color": bottom_sheet_color,
            "bottom_section_can_open": bottom_section_can_open,
            "bottom_section_can_expand": bottom_section_can_expand,
            "center_top_section_data": center_top_section_data,
            "draggable_sheet_max_height": draggable_sheet_max_height,
            "top_section": top_section,
            "bottom_section": bottom_section
        })

        if is_user_done == "y":
            break

    constraint_view = {
        "constraint_name": constraint_name,
        "view": config_model_views
    }
    print()
    save_view = input("~do you want to save this view (y,n): ")
    if save_view == "y":
        set_constraint_view(constraint_name, constraint_view)


def set_constraint_view(constraint_name=None, constraint_view=None):
    if constraint_name == None and constraint_view == None:
        constraint_name = input("~enter constraint name: ")
        views = [{
            "constraint_name": "Exchange rate",
            "view": [
                {
                    "bg_color": "#ffffff",
                    "bottom_section": [
                        {
                            "components": [
                                {
                                    "component_properties": [
                                        "input1",
                                        "0,0,10,10",
                                        "Currency 1",
                                        "Please enter a currency code"
                                    ],
                                    "type": "input"
                                },
                                {
                                    "component_properties": [
                                        "input2",
                                        "0,0,10,10",
                                        "Currency 2",
                                        "Please enter a currency code"
                                    ],
                                    "type": "input"
                                }
                            ],
                            "margin": "10,0,0,0"
                        },
                        {
                            "components": [
                                {
                                    "component_properties": [
                                        "button1",
                                        "20,0,0,0",
                                        "Submit",
                                        "center",
                                        "input_field",
                                        "input1,input2",
                                        "send_inputs",
                                        "input1,input2",
                                        "#000000"
                                    ],
                                    "type": "button"
                                }
                            ],
                            "margin": "0,0,0,0"
                        }
                    ],
                    "bottom_section_can_expand": "1",
                    "bottom_section_can_open": "1",
                    "bottom_sheet_color": "#ffffff",
                    "center_top_section_data": "1",
                    "draggable_sheet_max_height": "0.4",
                    "id": "1",
                    "top_section": [
                        {
                            "components": [
                                {
                                    "component_properties": [
                                        "text1",
                                        "0,0,0,0",
                                        "Exchange rate",
                                        "center",
                                        "20",
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0,0,0,0"
                        }
                    ]
                }
            ]
        },
            {
                "constraint_name": "Pause",
                "view": [
                    {
                        "bg_color": "#ffffff",
                        "bottom_section": [
                            {
                                "components": [
                                    {
                                        "component_properties": [
                                            "input1",
                                            "1,0,0,0",
                                            "Duration",
                                            "Please enter a duration"
                                        ],
                                        "type": "input"
                                    },
                                    {
                                        "component_properties": [
                                            "button1",
                                            "0,0,0,0",
                                            "Submit",
                                            "center",
                                            "input_field",
                                            "input1",
                                            "send_inputs",
                                            "input1",
                                            "#000000"
                                        ],
                                        "type": "button"
                                    }
                                ],
                                "margin": "10,0,0,0"
                            }
                        ],
                        "bottom_section_can_expand": "1",
                        "bottom_section_can_open": "1",
                        "bottom_sheet_color": "#ffffff",
                        "center_top_section_data": "1",
                        "draggable_sheet_max_height": "0.3",
                        "id": "1",
                        "top_section": [
                            {
                                "components": [
                                    {
                                        "component_properties": [
                                            "text1",
                                            "0,0,0,0",
                                            "Pause",
                                            "center",
                                            "30",
                                            "#000000"
                                        ],
                                        "type": "text"
                                    }
                                ],
                                "margin": "0,0,0,0"
                            }
                        ]
                    }
                ]
        },
            {
                "constraint_name": "Product description",
                "view": [
                    {
                        "bg_color": "#ffffff",
                        "bottom_section": [
                            {
                                "components": [
                                    {
                                        "component_properties": [
                                            "text6",
                                            "0,0,0,0",
                                            "-",
                                            "left",
                                            "1",
                                            "#000000"
                                        ],
                                        "type": "text"
                                    }
                                ],
                                "margin": "0,0,0,0"
                            }
                        ],
                        "bottom_section_can_expand": "0",
                        "bottom_section_can_open": "0",
                        "bottom_sheet_color": "#ffffff",
                        "center_top_section_data": "0",
                        "draggable_sheet_max_height": "0.1",
                        "id": "1",
                        "top_section": [
                            {
                                "components": [
                                    {
                                        "component_properties": [
                                            "text1",
                                            "40,0,30,0",
                                            "Product description constraint",
                                            "left",
                                            "20",
                                            "#000000"
                                        ],
                                        "type": "text"
                                    }
                                ],
                                "margin": "0,0,0,0"
                            },
                            {
                                "components": [
                                    {
                                        "component_properties": [
                                            "text2",
                                            "0,0,0,0",
                                            "{Product name}",
                                            "left",
                                            "25",
                                            "#000000"
                                        ],
                                        "type": "text"
                                    },
                                ],
                                "margin": "40,0,30,0"
                            },
                            {
                                "components": [
                                    {
                                        "component_properties": [
                                            "text3",
                                            "5,0,30,0",
                                            "Product name",
                                            "left",
                                            "15",
                                            "#000000"
                                        ],
                                        "type": "text"
                                    },
                                ],
                                "margin": "0,0,0,0"
                            },
                            {
                                "components": [
                                    {
                                        "component_properties": [
                                            "text4",
                                            "30,0,0,0",
                                            "{Product description}",
                                            "left",
                                            "25",
                                            "#000000"
                                        ],
                                        "type": "text"
                                    },
                                ],
                                "margin": "0,0,30,0"
                            },
                            {
                                "components": [
                                    {
                                        "component_properties": [
                                            "text7",
                                            "0,0,0,0",
                                            "Product description",
                                            "left",
                                            "15",
                                            "#000000"
                                        ],
                                        "type": "text"
                                    },
                                ],
                                "margin": "5,0,30,0"
                            }
                        ]
                    }
                ]
        }]
        constraint_view = input("~constraint view index: ")
        selected_constraint_view: dict = views[int(constraint_view)-1]
    else:
        selected_constraint_view = constraint_view

    result = perform_network_action(
        f"http://localhost:8000/constraint_view/{constraint_name}", "post", data={"view": jsonpickle.encode(selected_constraint_view)})
    if result["result"] == "success":
        print(f"> [{constraint_name}]'s view set")
    else:
        print("An error occured")


def create_user():
    global my_user
    user_name = input("~enter name: ")
    my_user = perform_network_action(
        "http://localhost:8000/create/"+str(user_name), "get")
    print(
        f">[SERVER] User created with name: {my_user['name']}, ID: {my_user['id']}")
    return my_user


def create_task():
    task_name = input("~enter task name: ")
    task_desc = input("~enter task desc: ")
    stage_group_id = input("~enter stage group id: ")
    task_id = perform_network_action("http://localhost:8000/create_task",
                                     "post", {"task_name": task_name, "task_desc": task_desc, "stage_group_id": stage_group_id})

    print(
        f">[SERVER] Task with name: {task_name}, desc: {task_desc}, ID: {task_id}")


def create_stage_group():
    addr = "http://localhost:8000/stage_group"
    stages = []
    while True:
        stage_name = input("~enter stage name ('x' to quit): ")
        if stage_name != "x":
            selected_constraints = []
            while True:
                constraints = input(
                    f"enter the constraints for Stage '{stage_name}' ('x' to quit): ")
                if constraints != "x":
                    selected_constraints.append(constraints)

                else:
                    break
            stages.append({"stage_name": stage_name,
                           "constraints": selected_constraints})
        else:
            break

    response = perform_network_action(
        addr, "post", json.dumps({"stages": stages}))
    if response["result"] == "fail":
        print(f"\n>Stage group could not be created \n>{response['msg']}")
    elif response["result"] == "success":
        print(f"StageGroup with ID: {response['msg']}")


def modify_stage_group():
    addr = "http://localhost:8000/stage_group"
    stage_id = input("~enter stage group id: ")


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

        print(jsonpickle.decode(response))


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
