import json
import jsonpickle
import requests
import websockets
import asyncio

my_user = None
my_pipeline_id = None
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

views = [{"constraint_name": "Exchange rate", "view": [{"id": "1", "bg_color": "#ffffff", "bottom_section_can_expand": "1", "bottom_section_can_open": "1", "bottom_sheet_color": "#ffffff", "center_top_section_data": "1", "draggable_sheet_max_height": 0.2, "top_section": [{"components": [{"component_properties": ["constraint_name", "0.0,0.0,0.0,0.0", "Exchange rate constraint", "center", 25.0, "#000000"], "type":"text"}], "margin":"0.0,0.0,0.0,0.0"}, {"components": [{"component_properties": ["constraint_description", "0.0,0.0,20.0,20.0", "Calculate the exchange rate between two currencies.", "center", 16.0, "#000000"], "type":"text"}], "margin":"5.0,0.0,0.0,0.0"}], "bottom_section":[{"components": [{"component_properties": ["currency1", "0.0,0.0,20.0,10.0", "Currency 1", "Please enter a currency"], "type":"input"}, {"component_properties": ["currency2", "0.0,0.0,20.0,10.0", "Currency 2", "Please enter a currency"], "type":"input"}], "margin":"0.0,0.0,0.0,0.0"}, {"components": [{"type": "button", "component_properties": ["submit_btn", "0.0,0.0,0.0,0.0", "Submit", "center", {"commandName": "cv", "success": {"commandName": "iec", "success": {"commandName": "cv", "success": {"commandName": "sdtwss", "success": {"commandName": "tp", "success": None, "failure": None, "usePrevResult": False, "value": ["success"]}, "failure":{"commandName": "tp", "success": None, "failure": None, "usePrevResult": False, "value": ["fail"]}, "usePrevResult":True, "value":["{0}"]}, "failure":None, "usePrevResult":False, "value":["currency1", "currency2"]}, "failure":None, "usePrevResult":False, "value":["{0}", None]}, "failure":None, "usePrevResult":False, "value":["currency1", "currency2"]}, None]}], "margin":"0.0,0.0,0.0,0.0"}]}]},
         {"constraint_name": "Pause", "view": [{"id": "1", "bg_color": "#ffffff", "bottom_section_can_expand": "1", "bottom_section_can_open": "1", "bottom_sheet_color": "#ffffff", "center_top_section_data": "1", "draggable_sheet_max_height": 0.125, "top_section": [{"components": [{"component_properties": ["constraint_name", "0.0,0.0,0.0,0.0", "Pause constraint", "center", 25.0, "#000000"], "type":"text"}], "margin":"0.0,0.0,0.0,0.0"}, {"components": [{"component_properties": ["constraint_description", "0.0,0.0,0.0,0.0", "Halts the stage for a given duration.", "center", 16.0, "#000000"], "type":"text"}], "margin":"5.0,0.0,0.0,0.0"}], "bottom_section":[{"components": [{"component_properties": ["duration", "0.0,0.0,20.0,10.0", "Duration", "Please enter a duration"], "type":"input"}, {
             "type": "button", "component_properties": ["submit_btn", "0.0,0.0,0.0,0.0", "Submit", "center", {"commandName": "cv", "success": {"commandName": "iec", "success": {"commandName": "cv", "success": {"commandName": "sdtwss", "success": {"commandName": "tp", "success": None, "failure": None, "usePrevResult": False, "value": ["success"]}, "failure":{"commandName": "tp", "success": None, "failure": None, "usePrevResult": False, "value": ["fail"]}, "usePrevResult":True, "value":["{0}"]}, "failure":None, "usePrevResult":False, "value":["duration"]}, "failure":None, "usePrevResult":False, "value":["{0}", None]}, "failure":None, "usePrevResult":False, "value":["duration"]}, None]}], "margin":"0.0,0.0,0.0,0.0"}]}]},
         {
    "constraint_name": "Product description",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                        {
                            "components": [
                                {
                                    "component_properties": [
                                        "ID",
                                        "0.0,0.0,0.0,0.0",
                                        "https://images.unsplash.com/photo-1540319585560-a4fcf1810366?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2250&q=80",
                                        250,
                                        200,
                                        True
                                    ],
                                    "type": "image"
                                }
                            ],
                            "margin": "0.0,30.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "",
                                        "0.0,0.0,20.0,0.0",
                                        "{Product name}",
                                        "left",
                                        25,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "",
                                        "0.0,0.0,20.0,0.0",
                                        "{Product description}",
                                        "left",
                                        20,
                                        "#37474F"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "10.0,0.0,0.0,0.0"
                        }
            ],
            "bottom_section": []
        }
    ]
},
    {
    "constraint_name": "Chat",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "0",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                {
                  "components": [
                      {
                          "component_properties": [
                              "",
                              "30.0,0.0,30.0,30.0",
                              "Chat test",
                              "left",
                              20,
                              "#000000"
                          ],
                          "type": "text"
                      }
                  ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "type": "list",
                            "component_properties": [
                                "chat",
                                "0.0,0.0,0.0,0.0",
                                [],
                                [
                                    {
                                        "component_properties": [
                                            "",
                                            "0.0,0.0,30.0,0.0",
                                            "",
                                            "left",
                                            14,
                                            "#000000"
                                        ],
                                        "type": "text"
                                    },
                                    {
                                        "component_properties": [
                                            "",
                                            "0.0,0.0,0.0,30.0",
                                            "",
                                            "right",
                                            14,
                                            "#000000"
                                        ],
                                        "type": "text"
                                    }
                                ]
                            ]
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "ID",
                                "0.0,0.0,0.0,0.0",
                                "hintText",
                                "errorText"
                            ],
                            "type": "input"
                        },
                        {
                            "type": "button",
                            "component_properties": [
                                "send_user",
                                "0.0,0.0,0.0,0.0",
                                "send user",
                                "left",
                                {
                                    "commandName": "cv",
                                    "success": {
                                        "commandName": "sld",
                                        "success": None,
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [
                                            "user",
                                            "{0}"
                                        ]
                                    },
                                    "failure": None,
                                    "usePrevResult": False,
                                    "value": [
                                        "ID"
                                    ]
                                },
                                None
                            ]
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                }
            ],
            "bottom_section": [],
            "top_view_command": [
                {
                    "commandName": "ltcca",
                    "success": {
                        "commandName": "sev",
                        "success": {
                            "commandName": "gev",
                            "success": {
                                "commandName": "pmc",
                                "success": {
                                    "commandName": "eq",
                                    "success": {
                                        "commandName": "gev",
                                        "success": {
                                            "commandName": "pmc",
                                            "success": {
                                                "commandName": "adtlc",
                                                "success": None,
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [
                                                    "chat",
                                                    [None, "{0}"]
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                ["data", "msg"],
                                                "{0}"
                                            ]
                                        },
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [["user_val"], False]
                                    },
                                    "failure": {
                                        "commandName": "gev",
                                        "success": {
                                            "commandName": "pmc",
                                            "success": {
                                                "commandName": "adtlc",
                                                "success": None,
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [
                                                    "chat",
                                                    ["{0}", None]
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                ["data", "msg"],
                                                "{0}"
                                            ]
                                        },
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [["user_val"], False]
                                    },
                                    "usePrevResult": False,
                                    "value": ["{0}", "user"]
                                },
                                "failure": None,
                                "usePrevResult": False,
                                "value": [
                                    ["data", "sender"],
                                    "{0}"
                                ]
                            },
                            "failure": None,
                            "usePrevResult": False,
                            "value": [["user_val"], False]
                        },
                        "failure": None,
                        "usePrevResult": False,
                        "value": ["user_val", "{0}", False]
                    },
                    "failure": None,
                    "usePrevResult": False,
                    "value": [None, "Chat"]
                }
            ],
            "bottom_view_command": None
        }
    ]
},
    {
    "constraint_name": "Order confirmation",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                        {
                            "components": [
                                {
                                    "component_properties": [
                                        "",
                                        "0.0,0.0,20.0,0.0",
                                        "Order confirmation",
                                        "left",
                                        25,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "",
                                        "0.0,0.0,20.0,20.0",
                                        "Click the button below to order the product",
                                        "left",
                                        20,
                                        "#37474F"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "10.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "type": "button",
                                    "component_properties": [
                                        "confirm_btn",
                                        "0.0,0.0,20.0,0.0",
                                        "Order",
                                        "left",
                                        {
                                            "commandName": "sdtwss",
                                            "success": None,
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [True]
                                        },
                                        None
                                    ]
                                }
                            ],
                            "margin": "10.0,0.0,0.0,0.0"
                        }
            ],
            "bottom_section": []
        }
    ]
},
    {
    "constraint_name": "Product link",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                        {
                            "components": [
                                {
                                    "component_properties": [
                                        "",
                                        "0.0,0.0,30.0,30.0",
                                        "{Link header}",
                                        "left",
                                        25,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "",
                                        "5.0,0.0,30.0,30.0",
                                        "{Link description}",
                                        "left",
                                        18,
                                        "#37474F"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "type": "button",
                                    "component_properties": [
                                        "",
                                        "0.0,0.0,20.0,0.0",
                                        "{Link btn name}",
                                        "left",
                                        {
                                            "commandName": "lu",
                                            "success": {
                                                "commandName": "sdtwss",
                                                "success": None,
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [True]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                "{Link url}"
                                            ]
                                        },
                                        None
                                    ]
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        }
            ],
            "bottom_section": []
        }
    ]
},
    {
    "constraint_name": "Password",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                {
                  "components": [
                      {
                          "component_properties": [
                              "",
                              "0.0,0.0,30.0,30.0",
                              "Password",
                              "center",
                              25,
                              "#000000"
                          ],
                          "type": "text"
                      }
                  ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "",
                                "5.0,0.0,30.0,30.0",
                                "Please enter the required password",
                                "center",
                                18,
                                "#37474F"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "password",
                                "20.0,0.0,30.0,30.0",
                                "Password",
                                "Please enter the password"
                            ],
                            "type": "input"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "type": "button",
                            "component_properties": [
                                "verify_btn",
                                "20.0,0.0,0.0,30.0",
                                "Verify",
                                "right",
                                {
                                    "commandName": "cv",
                                    "success": {
                                        "commandName": "sdtwss",
                                        "success": None,
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [
                                            "{0}"
                                        ]
                                    },
                                    "failure": None,
                                    "usePrevResult": False,
                                    "value": [
                                        "password"
                                    ]
                                },
                                None
                            ]
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                }
            ],
            "bottom_section": []
        }
    ]
},
    {
    "constraint_name": "Time range",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                {
                  "components": [
                      {
                          "component_properties": [
                              "",
                              "0.0,0.0,30.0,30.0",
                              "Time range",
                              "left",
                              25,
                              "#000000"
                          ],
                          "type": "text"
                      }
                  ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "",
                                "5.0,0.0,30.0,30.0",
                                "You can continue when within the time range specified below.",
                                "left",
                                18,
                                "#37474F"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "",
                                "20.0,0.0,30.0,30.0",
                                "12:30 TO 14:00",
                                "left",
                                16,
                                "#37474F"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "",
                                "5.0,0.0,30.0,30.0",
                                "Time",
                                "left",
                                16,
                                "#37474F"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "",
                                "50.0,0.0,30.0,30.0",
                                "{start_day}",
                                "left",
                                16,
                                "#37474F"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "",
                                "5.0,0.0,30.0,30.0",
                                "Start day",
                                "left",
                                16,
                                "#37474F"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                }
            ],
            "bottom_section": []
        }
    ]
},
    {
    "constraint_name": "Product description_config",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                        {
                            "components": [
                                {
                                    "component_properties": [
                                        "text1",
                                        "0.0,0.0,30.0,0.0",
                                        "Product description",
                                        "left",
                                        25,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "text2",
                                        "5.0,0.0,0.0,0.0",
                                        "Enter your product description details",
                                        "left",
                                        18,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,30.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "text3",
                                        "50.0,0.0,30.0,0.0",
                                        "The name of your product",
                                        "left",
                                        18,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "input1",
                                        "5.0,0.0,0.0,0.0",
                                        "Product name",
                                        "Please enter the product name"
                                    ],
                                    "type": "input"
                                }
                            ],
                            "margin": "0.0,0.0,30.0,30.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "text4",
                                        "50.0,0.0,30.0,0.0",
                                        "The description of your product",
                                        "left",
                                        18,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "input2",
                                        "5.0,0.0,0.0,0.0",
                                        "Product description",
                                        "Please describe your product"
                                    ],
                                    "type": "input"
                                }
                            ],
                            "margin": "0.0,0.0,30.0,30.0"
                        },
                {
                            "components": [
                                {
                                    "type": "button",
                                    "component_properties": [
                                        "complete_btn",
                                        "0.0,0.0,0.0,0.0",
                                        "Save",
                                        "right",
                                        {
                                            "commandName": "cv",
                                            "success": {
                                                "commandName": "sevtl",
                                                "success": {
                                                    "commandName": "cv",
                                                    "success": {
                                                        "commandName": "sevtl",
                                                        "success": None,
                                                        "failure": None,
                                                        "usePrevResult": False,
                                                        "value": ["config_inputs", "{0}", False]
                                                    },
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": ["input2"]
                                                },
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": ["config_inputs", "{0}", False]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                "input1",
                                            ]
                                        },
                                        None
                                    ]
                                }
                            ],
                            "margin": "40.0,0.0,0.0,30.0"
                        }
            ],
            "bottom_section": []
        }
    ]
},
    {
    "constraint_name": "Select constraint_config",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "0",
            "draggable_sheet_max_height": 0.1,
            "top_section": [
                        {
                            "components": [
                                {
                                    "component_properties": [
                                        "toptext1",
                                        "0.0,0.0,0.0,0.0",
                                        "Select constraints for your task",
                                        "left",
                                        25,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "40.0,0.0,30.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "toptext2",
                                        "0.0,0.0,0.0,0.0",
                                        "The constraints you select will be part of your task",
                                        "left",
                                        18,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "10.0,0.0,30.0,30.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "toptext3",
                                        "0.0,0.0,0.0,0.0",
                                        "Stages:",
                                        "left",
                                        16,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "30.0,0.0,30.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "type": "dropdown",
                                    "component_properties": [
                                        "dropdown",
                                        "0.0,0.0,30.0,50.0",
                                        None,
                                        [
                                            "Pending",
                                            "Active",
                                            "Complete"
                                        ],
                                        "Pending",
                                        {
                                            "commandName": "cv",
                                            "success": {
                                                "commandName": "tp",
                                                "success": None,
                                                "failure": None,
                                                "usePrevResult": True,
                                                "value": [
                                                    "dropdown"
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                "dropdown"
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "toptext4",
                                        "0.0,0.0,0.0,0.0",
                                        "Available constraints:",
                                        "left",
                                        16,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "30.0,0.0,30.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "type": "list",
                                    "component_properties": [
                                        "list",
                                        "0.0,0.0,0.0,0.0",
                                        [
                                            [
                                                "Exchange rate"
                                            ],
                                            [
                                                "Pause"
                                            ],
                                            [
                                                "Product description"
                                            ],
                                            [
                                                "Order confirmation"
                                            ],
                                            [
                                                "Product link"
                                            ],
                                            [
                                                "Password"
                                            ],
                                            [
                                                "Time range"
                                            ],
                                            [
                                                "Chat"
                                            ],
                                            [
                                                "Delivery"
                                            ]
                                        ],
                                        [
                                            {
                                                "type": "list_tile",
                                                "component_properties": [
                                                    "constraint_component",
                                                    "0.0,0.0,20.0,0.0",
                                                    16,
                                                    0,
                                                    "d",
                                                    "",
                                                    "left",
                                                    {
                                                        "commandName": "gcld",
                                                        "success": {
                                                            "commandName": "gcfl",
                                                            "success": {
                                                                "commandName": "cv",
                                                                "success": {
                                                                    "commandName": "sev",
                                                                    "success": {
                                                                        "commandName": "icr",
                                                                        "success": {
                                                                            "commandName": "gev",
                                                                            "success": {
                                                                                "commandName": "scd",
                                                                                "success": {
                                                                                    "commandName": "sev",
                                                                                    "success": {
                                                                                        "commandName": "gev",
                                                                                        "success": {
                                                                                            "commandName": "smkvtk",
                                                                                            "success": {
                                                                                                "commandName": "gev",
                                                                                                "success": {
                                                                                                    "commandName": "gev",
                                                                                                    "success": {
                                                                                                        "commandName": "smkvtk",
                                                                                                        "success": {
                                                                                                            "commandName": "cv",
                                                                                                            "success": {
                                                                                                                "commandName": "sev",
                                                                                                                "success": {
                                                                                                                    "commandName": "gev",
                                                                                                                    "success": {
                                                                                                                        "commandName": "gev",
                                                                                                                        "success": {
                                                                                                                            "commandName": "sevtl",
                                                                                                                            "success": None,
                                                                                                                            "failure": None,
                                                                                                                            "usePrevResult": False,
                                                                                                                            "value": [
                                                                                                                                "{1}",
                                                                                                                                "{0}",
                                                                                                                                False
                                                                                                                            ]
                                                                                                                        },
                                                                                                                        "failure": None,
                                                                                                                        "usePrevResult": False,
                                                                                                                        "value": [
                                                                                                                            [
                                                                                                                                "{0}",
                                                                                                                                "current_stage"
                                                                                                                            ],
                                                                                                                            False
                                                                                                                        ]
                                                                                                                    },
                                                                                                                    "failure": None,
                                                                                                                    "usePrevResult": False,
                                                                                                                    "value": [
                                                                                                                        [
                                                                                                                            "name"
                                                                                                                        ],
                                                                                                                        True
                                                                                                                    ]
                                                                                                                },
                                                                                                                "failure": None,
                                                                                                                "usePrevResult": False,
                                                                                                                "value": [
                                                                                                                    "current_stage",
                                                                                                                    "{0}",
                                                                                                                    False
                                                                                                                ]
                                                                                                            },
                                                                                                            "failure": None,
                                                                                                            "usePrevResult": False,
                                                                                                            "value": [
                                                                                                                "dropdown"
                                                                                                            ]
                                                                                                        },
                                                                                                        "failure": None,
                                                                                                        "usePrevResult": False,
                                                                                                        "value": [
                                                                                                            "{0}",
                                                                                                            [
                                                                                                                [
                                                                                                                    "constraint_name",
                                                                                                                    "{0}"
                                                                                                                ],
                                                                                                                [
                                                                                                                    "config_inputs",
                                                                                                                    "{1}"
                                                                                                                ]
                                                                                                            ],
                                                                                                            False
                                                                                                        ]
                                                                                                    },
                                                                                                    "failure": None,
                                                                                                    "usePrevResult": False,
                                                                                                    "value": [
                                                                                                        [
                                                                                                            "name",
                                                                                                            "{0}"
                                                                                                        ],
                                                                                                        True
                                                                                                    ]
                                                                                                },
                                                                                                "failure": None,
                                                                                                "usePrevResult": False,
                                                                                                "value": [
                                                                                                    [
                                                                                                        "name"
                                                                                                    ],
                                                                                                    True
                                                                                                ]
                                                                                            },
                                                                                            "failure": None,
                                                                                            "usePrevResult": False,
                                                                                            "value": [
                                                                                                "{0}",
                                                                                                [
                                                                                                    [
                                                                                                        "config_inputs",
                                                                                                        "{1}"
                                                                                                    ]
                                                                                                ],
                                                                                                True
                                                                                            ]
                                                                                        },
                                                                                        "failure": None,
                                                                                        "usePrevResult": False,
                                                                                        "value": [
                                                                                            [
                                                                                                "name",
                                                                                                "config_value"
                                                                                            ],
                                                                                            True
                                                                                        ]
                                                                                    },
                                                                                    "failure": None,
                                                                                    "usePrevResult": False,
                                                                                    "value": [
                                                                                        "config_value",
                                                                                        "{0}",
                                                                                        True
                                                                                    ]
                                                                                },
                                                                                "failure": None,
                                                                                "usePrevResult": False,
                                                                                "value": [
                                                                                    "{0}",
                                                                                    "ds"
                                                                                ]
                                                                            },
                                                                            "failure": None,
                                                                            "usePrevResult": False,
                                                                            "value": [
                                                                                [
                                                                                    "name"
                                                                                ],
                                                                                True
                                                                            ]
                                                                        },
                                                                        "failure": {
                                                                            "commandName": "gev",
                                                                            "success": {
                                                                                "commandName": "smkvtk",
                                                                                "success": {
                                                                                    "commandName": "gev",
                                                                                    "success": {
                                                                                        "commandName": "gev",
                                                                                        "success": {
                                                                                            "commandName": "smkvtk",
                                                                                            "success": {
                                                                                                "commandName": "cv",
                                                                                                "success": {
                                                                                                    "commandName": "sev",
                                                                                                    "success": {
                                                                                                        "commandName": "gev",
                                                                                                        "success": {
                                                                                                            "commandName": "gev",
                                                                                                            "success": {
                                                                                                                "commandName": "sevtl",
                                                                                                                "success": None,
                                                                                                                "failure": None,
                                                                                                                "usePrevResult": False,
                                                                                                                "value": [
                                                                                                                    "{1}",
                                                                                                                    "{0}",
                                                                                                                    False
                                                                                                                ]
                                                                                                            },
                                                                                                            "failure": None,
                                                                                                            "usePrevResult": False,
                                                                                                            "value": [
                                                                                                                [
                                                                                                                    "{0}",
                                                                                                                    "current_stage"
                                                                                                                ],
                                                                                                                False
                                                                                                            ]
                                                                                                        },
                                                                                                        "failure": None,
                                                                                                        "usePrevResult": False,
                                                                                                        "value": [
                                                                                                            [
                                                                                                                "name"
                                                                                                            ],
                                                                                                            True
                                                                                                        ]
                                                                                                    },
                                                                                                    "failure": None,
                                                                                                    "usePrevResult": False,
                                                                                                    "value": [
                                                                                                        "current_stage",
                                                                                                        "{0}",
                                                                                                        False
                                                                                                    ]
                                                                                                },
                                                                                                "failure": None,
                                                                                                "usePrevResult": False,
                                                                                                "value": [
                                                                                                    "dropdown"
                                                                                                ]
                                                                                            },
                                                                                            "failure": None,
                                                                                            "usePrevResult": False,
                                                                                            "value": [
                                                                                                "{0}",
                                                                                                [
                                                                                                    [
                                                                                                        "constraint_name",
                                                                                                        "{0}"
                                                                                                    ],
                                                                                                    [
                                                                                                        "config_inputs",
                                                                                                        "{1}"
                                                                                                    ]
                                                                                                ],
                                                                                                False
                                                                                            ]
                                                                                        },
                                                                                        "failure": None,
                                                                                        "usePrevResult": False,
                                                                                        "value": [
                                                                                            [
                                                                                                "name",
                                                                                                "{0}"
                                                                                            ],
                                                                                            True
                                                                                        ]
                                                                                    },
                                                                                    "failure": None,
                                                                                    "usePrevResult": False,
                                                                                    "value": [
                                                                                        [
                                                                                            "name"
                                                                                        ],
                                                                                        True
                                                                                    ]
                                                                                },
                                                                                "failure": None,
                                                                                "usePrevResult": False,
                                                                                "value": [
                                                                                    "{0}",
                                                                                    [
                                                                                        [
                                                                                            "config_inputs",
                                                                                            None
                                                                                        ]
                                                                                    ],
                                                                                    True
                                                                                ]
                                                                            },
                                                                            "failure": None,
                                                                            "usePrevResult": False,
                                                                            "value": [
                                                                                [
                                                                                    "name"
                                                                                ],
                                                                                True
                                                                            ]
                                                                        },
                                                                        "usePrevResult": False,
                                                                        "value": [
                                                                            "{0}"
                                                                        ]
                                                                    },
                                                                    "failure": None,
                                                                    "usePrevResult": False,
                                                                    "value": [
                                                                        "name",
                                                                        "{0}",
                                                                        True
                                                                    ]
                                                                },
                                                                "failure": None,
                                                                "usePrevResult": False,
                                                                "value": [
                                                                    "{0}"
                                                                ]
                                                            },
                                                            "failure": None,
                                                            "usePrevResult": False,
                                                            "value": [
                                                                "list",
                                                                "{0}",
                                                                "{1}"
                                                            ]
                                                        },
                                                        "failure": None,
                                                        "usePrevResult": False,
                                                        "value": []
                                                    },
                                                    {
                                                        "commandName": "gcld",
                                                        "success": {
                                                            "commandName": "gcfl",
                                                            "success": {
                                                                "commandName": "cv",
                                                                "success": {
                                                                    "commandName": "sev",
                                                                    "success": {
                                                                        "commandName": "gev",
                                                                        "success": {
                                                                            "commandName": "rcfs",
                                                                            "success": None,
                                                                            "failure": None,
                                                                            "usePrevResult": False,
                                                                            "value": [
                                                                                "{0}",
                                                                                "{1}"
                                                                            ]
                                                                        },
                                                                        "failure": None,
                                                                        "usePrevResult": False,
                                                                        "value": [
                                                                            [
                                                                                "selected_option",
                                                                                "current_stage"
                                                                            ],
                                                                            False
                                                                        ]
                                                                    },
                                                                    "failure": None,
                                                                    "usePrevResult": False,
                                                                    "value": [
                                                                        "selected_option",
                                                                        "{0}",
                                                                        False
                                                                    ]
                                                                },
                                                                "failure": None,
                                                                "usePrevResult": False,
                                                                "value": [
                                                                    "{0}"
                                                                ]
                                                            },
                                                            "failure": None,
                                                            "usePrevResult": False,
                                                            "value": [
                                                                "list",
                                                                "{0}",
                                                                "{1}"
                                                            ]
                                                        },
                                                        "failure": None,
                                                        "usePrevResult": False,
                                                        "value": [
                                                            ""
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    ]
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "type": "button",
                                    "component_properties": [
                                        "complete",
                                        "0.0,0.0,0.0,0.0",
                                        "Complete",
                                        "right",
                                        {
                                            "commandName": "gev",
                                            "success": {
                                                "commandName": "smkvtk",
                                                "success": {
                                                    "commandName": "gev",
                                                    "success": {
                                                        "commandName": "smkvtk",
                                                        "success": {
                                                            "commandName": "gev",
                                                            "success": {
                                                                "commandName": "smkvtk",
                                                                "success": {
                                                                    "commandName": "gev",
                                                                    "success": {
                                                                        "commandName": "sevtl",
                                                                        "success": {
                                                                            "commandName": "gev",
                                                                            "success": {
                                                                                "commandName": "sevtl",
                                                                                "success": {
                                                                                    "commandName": "gev",
                                                                                    "success": {
                                                                                        "commandName": "sevtl",
                                                                                        "success": {
                                                                                            "commandName": "gev",
                                                                                            "success": {
                                                                                                "commandName": "srd",
                                                                                                "success": {
                                                                                                    "commandName": "sev",
                                                                                                    "success": {
                                                                                                        "commandName": "gev",
                                                                                                        "success": {
                                                                                                            "commandName": "eq",
                                                                                                            "success": {
                                                                                                                "commandName": "sdc",
                                                                                                                "success": None,
                                                                                                                "failure": None,
                                                                                                                "usePrevResult": False,
                                                                                                                "value": [
                                                                                                                    "Registration",
                                                                                                                    "An error occured"
                                                                                                                ]
                                                                                                            },
                                                                                                            "failure": {
                                                                                                                "commandName": "gev",
                                                                                                                "success": {
                                                                                                                    "commandName": "sdc",
                                                                                                                    "success": None,
                                                                                                                    "failure": None,
                                                                                                                    "usePrevResult": False,
                                                                                                                    "value": [
                                                                                                                        "Registration success",
                                                                                                                        "c {0}"
                                                                                                                    ]
                                                                                                                },
                                                                                                                "failure": None,
                                                                                                                "usePrevResult": False,
                                                                                                                "value": [
                                                                                                                    [
                                                                                                                        "reg_result"
                                                                                                                    ],
                                                                                                                    False
                                                                                                                ]
                                                                                                            },
                                                                                                            "usePrevResult": False,
                                                                                                            "value": [
                                                                                                                "{0}",
                                                                                                                ""
                                                                                                            ]
                                                                                                        },
                                                                                                        "failure": None,
                                                                                                        "usePrevResult": False,
                                                                                                        "value": [
                                                                                                            [
                                                                                                                "reg_result"
                                                                                                            ],
                                                                                                            False
                                                                                                        ]
                                                                                                    },
                                                                                                    "failure": None,
                                                                                                    "usePrevResult": False,
                                                                                                    "value": [
                                                                                                        "reg_result",
                                                                                                        "{0}",
                                                                                                        False
                                                                                                    ]
                                                                                                },
                                                                                                "failure": {
                                                                                                    "commandName": "sdc",
                                                                                                    "success": None,
                                                                                                    "failure": None,
                                                                                                    "usePrevResult": False,
                                                                                                    "value": [
                                                                                                        "Registration",
                                                                                                        "An error occured"
                                                                                                    ]
                                                                                                },
                                                                                                "usePrevResult": False,
                                                                                                "value": [
                                                                                                    "{0}"
                                                                                                ]
                                                                                            },
                                                                                            "failure": None,
                                                                                            "usePrevResult": False,
                                                                                            "value": [
                                                                                                [
                                                                                                    "stages"
                                                                                                ],
                                                                                                False
                                                                                            ]
                                                                                        },
                                                                                        "failure": None,
                                                                                        "usePrevResult": False,
                                                                                        "value": [
                                                                                            "stages",
                                                                                            "{0}",
                                                                                            False
                                                                                        ]
                                                                                    },
                                                                                    "failure": None,
                                                                                    "usePrevResult": False,
                                                                                    "value": [
                                                                                        [
                                                                                            "Complete_data"
                                                                                        ],
                                                                                        False
                                                                                    ]
                                                                                },
                                                                                "failure": None,
                                                                                "usePrevResult": False,
                                                                                "value": [
                                                                                    "stages",
                                                                                    "{0}",
                                                                                    False
                                                                                ]
                                                                            },
                                                                            "failure": None,
                                                                            "usePrevResult": False,
                                                                            "value": [
                                                                                [
                                                                                    "Active_data"
                                                                                ],
                                                                                False
                                                                            ]
                                                                        },
                                                                        "failure": None,
                                                                        "usePrevResult": False,
                                                                        "value": [
                                                                            "stages",
                                                                            "{0}",
                                                                            False
                                                                        ]
                                                                    },
                                                                    "failure": None,
                                                                    "usePrevResult": False,
                                                                    "value": [
                                                                        [
                                                                            "Pending_data"
                                                                        ],
                                                                        False
                                                                    ]
                                                                },
                                                                "failure": None,
                                                                "usePrevResult": False,
                                                                "value": [
                                                                    "Complete_data",
                                                                    [
                                                                        [
                                                                            "stage_name",
                                                                            "Complete"
                                                                        ],
                                                                        [
                                                                            "constraints",
                                                                            "{0}"
                                                                        ]
                                                                    ],
                                                                    False
                                                                ]
                                                            },
                                                            "failure": None,
                                                            "usePrevResult": False,
                                                            "value": [
                                                                [
                                                                    "Complete"
                                                                ],
                                                                False
                                                            ]
                                                        },
                                                        "failure": None,
                                                        "usePrevResult": False,
                                                        "value": [
                                                            "Active_data",
                                                            [
                                                                [
                                                                    "stage_name",
                                                                    "Active"
                                                                ],
                                                                [
                                                                    "constraints",
                                                                    "{0}"
                                                                ]
                                                            ],
                                                            False
                                                        ]
                                                    },
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": [
                                                        [
                                                            "Active"
                                                        ],
                                                        False
                                                    ]
                                                },
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [
                                                    "Pending_data",
                                                    [
                                                        [
                                                            "stage_name",
                                                            "Pending"
                                                        ],
                                                        [
                                                            "constraints",
                                                            "{0}"
                                                        ]
                                                    ],
                                                    False
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                [
                                                    "Pending"
                                                ],
                                                False
                                            ]
                                        },
                                        None
                                    ]
                                }
                            ],
                            "margin": "50.0,0.0,0.0,30.0"
                        }
            ],
            "bottom_section": []
        }
    ]
},
    {
    "constraint_name": "Create task_config",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                        {
                            "components": [
                                {
                                    "component_properties": [
                                        "",
                                        "0.0,0.0,30.0,0.0",
                                        "Create task",
                                        "left",
                                        25,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "",
                                        "5.0,0.0,30.0,30.0",
                                        "Complete the form to create a task",
                                        "left",
                                        18,
                                        "#263238"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "task_name",
                                        "30.0,0.0,30.0,30.0",
                                        "Task name",
                                        "Please enter the task name"
                                    ],
                                    "type": "input"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "task_desc",
                                        "30.0,0.0,30.0,30.0",
                                        "Task description",
                                        "Please enter the task description"
                                    ],
                                    "type": "input"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "text2",
                                        "30.0,0.0,30.0,30.0",
                                        "Click the button below, complete the form, copy the code and paste it below",
                                        "left",
                                        15,
                                        "#263238"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "type": "button",
                                    "component_properties": [
                                        "btn",
                                        "0.0,0.0,30.0,0.0",
                                        "Create stage group",
                                        "left",
                                        {
                                            "commandName": "scd",
                                            "success": None,
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                "Select constraint",
                                                ""
                                            ]
                                        },
                                        None
                                    ]
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "stage_group_id",
                                        "20.0,0.0,30.0,30.0",
                                        "Stage group ID",
                                        "Please enter the stage group ID"
                                    ],
                                    "type": "input"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "type": "button",
                                    "component_properties": [
                                        "complete",
                                        "20.0,0.0,0.0,30.0",
                                        "Create",
                                        "right",
                                        {
                                            "commandName": "cv",
                                            "success": {
                                                "commandName": "strd",
                                                "success": {
                                                    "commandName": "sdc",
                                                    "success": None,
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": [
                                                        "Registration success",
                                                        "{0}"
                                                    ]
                                                },
                                                "failure": {
                                                    "commandName": "sdc",
                                                    "success": None,
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": [
                                                        "Registration",
                                                        "An error occured"
                                                    ]
                                                },
                                                "usePrevResult": False,
                                                "value": [
                                                    "{0}",
                                                    "{1}",
                                                    "{2}"
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                "task_name",
                                                "task_desc",
                                                "stage_group_id"
                                            ]
                                        },
                                        None
                                    ]
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        }
            ],
            "bottom_section": []
        }
    ]
},
    {
    "constraint_name": "Product link_config",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                        {
                            "components": [
                                {
                                    "component_properties": [
                                        "",
                                        "0.0,0.0,30.0,30.0",
                                        "Product link constraint",
                                        "left",
                                        25,
                                        "#000000"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "",
                                        "5.0,0.0,30.0,30.0",
                                        "This constraint enables you to provide a link for your customer",
                                        "left",
                                        18,
                                        "#37474F"
                                    ],
                                    "type": "text"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "link_name",
                                        "20.0,0.0,30.0,30.0",
                                        "Link name",
                                        "Please enter the link name"
                                    ],
                                    "type": "input"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "link_description",
                                        "20.0,0.0,30.0,30.0",
                                        "Link description",
                                        "Please enter the link description"
                                    ],
                                    "type": "input"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "link_btn_name",
                                        "20.0,0.0,30.0,30.0",
                                        "Link button name",
                                        "Please enter the link button's name"
                                    ],
                                    "type": "input"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "component_properties": [
                                        "link_btn_url",
                                        "20.0,0.0,30.0,30.0",
                                        "Link button URL",
                                        "Please enter the link button's URL"
                                    ],
                                    "type": "input"
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        },
                {
                            "components": [
                                {
                                    "type": "button",
                                    "component_properties": [
                                        "save_btn",
                                        "20.0,0.0,0.0,30.0",
                                        "Save",
                                        "right",
                                        {
                                            "commandName": "cv",
                                            "success": {
                                                "commandName": "sevtl",
                                                "success": {
                                                    "commandName": "cd",
                                                    "success": None,
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": []
                                                },
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [
                                                    "config_inputs",
                                                    ["{0}", "{1}", "{2}", "{3}"],
                                                    False
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                "link_name",
                                                "link_description",
                                                "link_btn_name",
                                                "link_btn_url"
                                            ]
                                        },
                                        None
                                    ]
                                }
                            ],
                            "margin": "0.0,0.0,0.0,0.0"
                        }
            ],
            "bottom_section": []
        }
    ],

},
    {
    "constraint_name": "Password_config",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                {
                  "components": [
                      {
                          "component_properties": [
                              "",
                              "0.0,0.0,30.0,30.0",
                              "Password",
                              "left",
                              25,
                              "#000000"
                          ],
                          "type": "text"
                      }
                  ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "",
                                "5.0,0.0,30.0,30.0",
                                "Please enter a phrase/word for your password",
                                "left",
                                18,
                                "#37474F"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "password",
                                "20.0,0.0,30.0,30.0",
                                "Password",
                                "Please enter the password"
                            ],
                            "type": "input"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "type": "button",
                            "component_properties": [
                                "save_btn",
                                "20.0,0.0,0.0,30.0",
                                "Save",
                                "right",
                                {
                                    "commandName": "cv",
                                    "success": {
                                        "commandName": "sevtl",
                                        "success": None,
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [
                                            "config_inputs",
                                            "{0}",
                                            False
                                        ]
                                    },
                                    "failure": None,
                                    "usePrevResult": False,
                                    "value": [
                                        "password"
                                    ]
                                },
                                None
                            ]
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                }
            ],
            "bottom_section": []
        }
    ]
},
    {
    "constraint_name": "Time range_config",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.7,
            "top_section": [
                {
                  "components": [
                      {
                          "component_properties": [
                              "",
                              "0.0,0.0,30.0,30.0",
                              "Time range",
                              "left",
                              25,
                              "#000000"
                          ],
                          "type": "text"
                      }
                  ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "",
                                "5.0,0.0,30.0,30.0",
                                "You can continue when within the time range specified below.",
                                "left",
                                18,
                                "#37474F"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "time_range",
                                "20.0,0.0,30.0,30.0",
                                "Select the time range",
                                "left",
                                16,
                                "#F44336"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "type": "button",
                            "component_properties": [
                                "start_time_btn",
                                "0.0,0.0,30.0,0.0",
                                "Select time",
                                "left",
                                {
                                    "commandName": "stpd",
                                    "success": {
                                        "commandName": "smv",
                                        "success": {
                                            "commandName": "stpd",
                                            "success": {
                                                "commandName": "smv",
                                                "success": {
                                                    "commandName": "gev",
                                                    "success": {
                                                        "commandName": "stcv",
                                                        "success": None,
                                                        "failure": None,
                                                        "usePrevResult": False,
                                                        "value": [
                                                            [
                                                                "{0}",
                                                                ":",
                                                                "{1}",
                                                                "{2}",
                                                                " TO ",
                                                                "{3}",
                                                                ":",
                                                                "{4}",
                                                                "{5}"
                                                            ],
                                                            "time_range"
                                                        ]
                                                    },
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": [
                                                        [
                                                            "start_hour",
                                                            "start_min",
                                                            "start_period",
                                                            "end_hour",
                                                            "end_min",
                                                            "end_period"
                                                        ],
                                                        True
                                                    ]
                                                },
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [
                                                    [
                                                        [
                                                            "end_hour",
                                                            "{0}"
                                                        ],
                                                        [
                                                            "end_min",
                                                            "{1}"
                                                        ],
                                                        [
                                                            "end_period",
                                                            "{2}"
                                                        ]
                                                    ],
                                                    True
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": []
                                        },
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [
                                            [
                                                [
                                                    "start_hour",
                                                    "{0}"
                                                ],
                                                [
                                                    "start_min",
                                                    "{1}"
                                                ],
                                                [
                                                    "start_period",
                                                    "{2}"
                                                ]
                                            ],
                                            True
                                        ]
                                    },
                                    "failure": None,
                                    "usePrevResult": False,
                                    "value": []
                                },
                                None
                            ]
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "day_range",
                                "20.0,0.0,30.0,30.0",
                                "Select the day range",
                                "left",
                                16,
                                "#F44336"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "type": "button",
                            "component_properties": [
                                "start_time_btn",
                                "0.0,0.0,30.0,0.0",
                                "Select day",
                                "left",
                                {
                                    "commandName": "sdfsc",
                                    "success": {
                                        "commandName": "sev",
                                        "success": {
                                            "commandName": "sdfsc",
                                            "success": {
                                                "commandName": "sev",
                                                "success": {
                                                    "commandName": "gev",
                                                    "success": {
                                                        "commandName": "stcv",
                                                        "success": None,
                                                        "failure": None,
                                                        "usePrevResult": False,
                                                        "value": [
                                                            [
                                                                "{0}",
                                                                " TO ",
                                                                "{1}"
                                                            ],
                                                            "day_range"
                                                        ]
                                                    },
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": [
                                                        [
                                                            "start_day",
                                                            "end_day"
                                                        ],
                                                        True
                                                    ]
                                                },
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [
                                                    "end_day",
                                                    "{0}",
                                                    True
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                "Select the end day",
                                                [
                                                    "Monday",
                                                    "Tuesday",
                                                    "Wednesday",
                                                    "Thursday",
                                                    "Friday",
                                                    "Saturday",
                                                    "Sunday"
                                                ]
                                            ]
                                        },
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [
                                            "start_day",
                                            "{0}",
                                            True
                                        ]
                                    },
                                    "failure": None,
                                    "usePrevResult": False,
                                    "value": [
                                        "Select the start day",
                                        [
                                            "Monday",
                                            "Tuesday",
                                            "Wednesday",
                                            "Thursday",
                                            "Friday",
                                            "Saturday",
                                            "Sunday"
                                        ]
                                    ]
                                },
                                None
                            ]
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "type": "button",
                            "component_properties": [
                                "save",
                                "20.0,0.0,0.0,30.0",
                                "Save",
                                "right",
                                {
                                    "commandName": "gev",
                                    "success": {
                                        "commandName": "sevtl",
                                        "success": None,
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [
                                            "config_inputs",
                                            [
                                                "{0}",
                                                "{1}",
                                                "{2}",
                                                "{3}",
                                                "{4}",
                                                "{5}"
                                            ],
                                            False
                                        ]
                                    },
                                    "failure": None,
                                    "usePrevResult": False,
                                    "value": [
                                        [
                                            "start_hour",
                                            "start_min",
                                            "end_hour",
                                            "end_min",
                                            "start_day",
                                            "end_day"
                                        ],
                                        True
                                    ]
                                },
                                None
                            ]
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                }
            ],
            "bottom_section": []
        }
    ]
},
    {
    "constraint_name": "Delivery",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.12,
            "top_section": [
                {
                  "components": [
                      {
                          "component_properties": [
                              "",
                              "0.0,0.0,30.0,30.0",
                              "Delivery status",
                              "left",
                              20,
                              "#000000"
                          ],
                          "type": "text"
                      }
                  ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "ID",
                                "5.0,0.0,30.0,30.0",
                                "Track the status of the task real-time.",
                                "left",
                                16,
                                "#616161"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "started",
                                "30.0,0.0,30.0,30.0",
                                "Started",
                                "left",
                                16,
                                "#F44336"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "started_msg",
                                "5.0,0.0,30.0,30.0",
                                "-",
                                "left",
                                14,
                                "#616161"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "preping",
                                "30.0,0.0,30.0,0.0",
                                "Preparing",
                                "left",
                                16,
                                "#F44336"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "preping_msg",
                                "5.0,0.0,30.0,30.0",
                                "-",
                                "left",
                                14,
                                "#616161"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "en_route",
                                "30.0,0.0,30.0,0.0",
                                "En-route",
                                "left",
                                16,
                                "#F44336"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "en_route_msg",
                                "5.0,0.0,30.0,30.0",
                                "-",
                                "left",
                                14,
                                "#616161"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "delivered",
                                "30.0,0.0,30.0,0.0",
                                "Delivered",
                                "left",
                                16,
                                "#F44336"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "delivered_msg",
                                "5.0,0.0,30.0,30.0",
                                "-",
                                "left",
                                14,
                                "#616161"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                }
            ],
            "bottom_section": [],
            "top_view_command": [
                {
                    "commandName": "ltcca",
                    "success": {
                        "commandName": "sev",
                        "success": {
                            "commandName": "gev",
                            "success": {
                                "commandName": "pmc",
                                "success": {
                                    "commandName": "eq",
                                    "success": {
                                        "commandName": "ctc",
                                        "success": {
                                            "commandName": "gev",
                                            "success": {
                                                "commandName": "pmc",
                                                "success": {
                                                    "commandName": "stcv",
                                                    "success": None,
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": [
                                                        ["{0}"],
                                                        "started_msg"
                                                    ]
                                                },
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [
                                                    ["data", "msg"],
                                                    "{0}"
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                ["status"],
                                                False
                                            ]
                                        },
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": ["started", "#4CAF50"]
                                    },
                                    "failure": {
                                        "commandName": "gev",
                                        "success": {
                                            "commandName": "pmc",
                                            "success": {
                                                "commandName": "eq",
                                                "success": {
                                                    "commandName": "ctc",
                                                    "success": {
                                                        "commandName": "gev",
                                                        "success": {
                                                            "commandName": "pmc",
                                                            "success": {
                                                                "commandName": "stcv",
                                                                "success": None,
                                                                "failure": None,
                                                                "usePrevResult": False,
                                                                "value": [
                                                                    ["{0}"],
                                                                    "preping_msg"
                                                                ]
                                                            },
                                                            "failure": None,
                                                            "usePrevResult": False,
                                                            "value": [
                                                                ["data", "msg"],
                                                                "{0}"
                                                            ]
                                                        },
                                                        "failure": None,
                                                        "usePrevResult": False,
                                                        "value": [
                                                            ["status"],
                                                            False
                                                        ]
                                                    },
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": ["preping", "#4CAF50"]
                                                },
                                                "failure": {
                                                    "commandName": "gev",
                                                    "success": {
                                                        "commandName": "pmc",
                                                        "success": {
                                                            "commandName": "eq",
                                                            "success": {
                                                                "commandName": "ctc",
                                                                "success": {
                                                                    "commandName": "gev",
                                                                    "success": {
                                                                        "commandName": "pmc",
                                                                        "success": {
                                                                            "commandName": "stcv",
                                                                            "success": None,
                                                                            "failure": None,
                                                                            "usePrevResult": False,
                                                                            "value": [
                                                                                ["{0}"],
                                                                                "en_route_msg"
                                                                            ]
                                                                        },
                                                                        "failure": None,
                                                                        "usePrevResult": False,
                                                                        "value": [
                                                                            ["data",
                                                                                "msg"],
                                                                            "{0}"
                                                                        ]
                                                                    },
                                                                    "failure": None,
                                                                    "usePrevResult": False,
                                                                    "value": [
                                                                        ["status"],
                                                                        False
                                                                    ]
                                                                },
                                                                "failure": None,
                                                                "usePrevResult": False,
                                                                "value": ["en_route", "#4CAF50"]
                                                            },
                                                            "failure": {
                                                                "commandName": "gev",
                                                                "success": {
                                                                    "commandName": "pmc",
                                                                    "success": {
                                                                        "commandName": "eq",
                                                                        "success": {
                                                                            "commandName": "ctc",
                                                                            "success": {
                                                                                "commandName": "gev",
                                                                                "success": {
                                                                                    "commandName": "pmc",
                                                                                    "success": {
                                                                                        "commandName": "stcv",
                                                                                        "success": None,
                                                                                        "failure": None,
                                                                                        "usePrevResult": False,
                                                                                        "value": [
                                                                                            ["{0}"],
                                                                                            "delivered_msg"
                                                                                        ]
                                                                                    },
                                                                                    "failure": None,
                                                                                    "usePrevResult": False,
                                                                                    "value": [
                                                                                        ["data",
                                                                                         "msg"],
                                                                                        "{0}"
                                                                                    ]
                                                                                },
                                                                                "failure": None,
                                                                                "usePrevResult": False,
                                                                                "value": [
                                                                                    ["status"],
                                                                                    False
                                                                                ]
                                                                            },
                                                                            "failure": None,
                                                                            "usePrevResult": False,
                                                                            "value": ["delivered", "#4CAF50"]
                                                                        },
                                                                        "failure": None,
                                                                        "usePrevResult": False,
                                                                        "value": ["{0}", "done"]
                                                                    },
                                                                    "failure": None,
                                                                    "usePrevResult": False,
                                                                    "value": [
                                                                        ["data",
                                                                            "stage"],
                                                                        "{0}"
                                                                    ]
                                                                },
                                                                "failure": None,
                                                                "usePrevResult": False,
                                                                "value": [
                                                                    ["status"],
                                                                    False
                                                                ]
                                                            },
                                                            "usePrevResult": False,
                                                            "value": ["{0}", "en_route"]
                                                        },
                                                        "failure": None,
                                                        "usePrevResult": False,
                                                        "value": [
                                                            ["data", "stage"],
                                                            "{0}"
                                                        ]
                                                    },
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": [
                                                        ["status"],
                                                        False
                                                    ]
                                                },
                                                "usePrevResult": False,
                                                "value": ["{0}", "prep"]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                ["data", "stage"],
                                                "{0}"
                                            ]
                                        },
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [
                                            ["status"],
                                            False
                                        ]
                                    },
                                    "usePrevResult": False,
                                    "value": ["{0}", "start"]
                                },
                                "failure": None,
                                "usePrevResult": False,
                                "value": [
                                    ["data", "stage"],
                                    "{0}"
                                ]
                            },
                            "failure": None,
                            "usePrevResult": False,
                            "value": [
                                ["status"],
                                False
                            ]
                        },
                        "failure": None,
                        "usePrevResult": False,
                        "value": ["status", "{0}", False]
                    },
                    "failure": None,
                    "usePrevResult": False,
                    "value": []
                },
            ],
            "bottom_view_command": None
        }
    ]
},
    {
    "constraint_name": "Chat_admin",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "1",
            "bottom_section_can_open": "1",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "0",
            "draggable_sheet_max_height": 0.12,
            "top_section": [
                {
                  "components": [
                      {
                          "component_properties": [
                              "",
                              "30.0,0.0,30.0,30.0",
                              "Admin Chat test",
                              "left",
                              20,
                              "#000000"
                          ],
                          "type": "text"
                      }
                  ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "type": "list",
                            "component_properties": [
                                "chat",
                                "0.0,0.0,0.0,0.0",
                                [],
                                [
                                    {
                                        "component_properties": [
                                            "",
                                            "0.0,0.0,30.0,0.0",
                                            "",
                                            "left",
                                            14,
                                            "#000000"
                                        ],
                                        "type": "text"
                                    },
                                    {
                                        "component_properties": [
                                            "",
                                            "0.0,0.0,0.0,30.0",
                                            "",
                                            "right",
                                            14,
                                            "#000000"
                                        ],
                                        "type": "text"
                                    }
                                ]
                            ]
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
            ],
            "bottom_section": [
                {
                    "components": [
                        {
                            "component_properties": [
                                "ID",
                                "0.0,0.0,0.0,0.0",
                                "hintText",
                                "errorText"
                            ],
                            "type": "input"
                        },
                        {
                            "type": "button",
                            "component_properties": [
                                "send_user",
                                "0.0,0.0,0.0,0.0",
                                "send admin",
                                "center",
                                {
                                    "commandName": "cv",
                                    "success": {
                                        "commandName": "sld",
                                        "success": None,
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [
                                            "admin",
                                            "{0}",
                                            None,
                                            "Chat"
                                        ]
                                    },
                                    "failure": None,
                                    "usePrevResult": False,
                                    "value": [
                                        "ID"
                                    ]
                                },
                                None
                            ]
                        },
                        {
                            "type": "button",
                            "component_properties": [
                                "complete",
                                "0.0,0.0,0.0,0.0",
                                "complete",
                                "center",
                                {
                                    "commandName": "cv",
                                    "success": {
                                        "commandName": "sld",
                                        "success": None,
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [
                                            "complete",
                                            "{0}"
                                        ]
                                    },
                                    "failure": None,
                                    "usePrevResult": False,
                                    "value": [
                                        "ID"
                                    ]
                                },
                                None
                            ]
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                }
            ],

            "top_view_command": [
                {
                    "commandName": "ltcca",
                    "success": {
                        "commandName": "sev",
                        "success": {
                            "commandName": "gev",
                            "success": {
                                "commandName": "pmc",
                                "success": {
                                    "commandName": "eq",
                                    "success": {
                                        "commandName": "gev",
                                        "success": {
                                            "commandName": "pmc",
                                            "success": {
                                                "commandName": "adtlc",
                                                "success": None,
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [
                                                    "chat",
                                                    ["{0}", None]
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                ["data", "msg"],
                                                "{0}"
                                            ]
                                        },
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [["admin_val"], False]
                                    },
                                    "failure": {
                                        "commandName": "gev",
                                        "success": {
                                            "commandName": "pmc",
                                            "success": {
                                                "commandName": "adtlc",
                                                "success": None,
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [
                                                    "chat",
                                                    [None, "{0}"]
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                ["data", "msg"],
                                                "{0}"
                                            ]
                                        },
                                        "failure": None,
                                        "usePrevResult": False,
                                        "value": [["admin_val"], False]
                                    },
                                    "usePrevResult": False,
                                    "value": ["{0}", "user"]
                                },
                                "failure": None,
                                "usePrevResult": False,
                                "value": [
                                    ["data", "sender"],
                                    "{0}"
                                ]
                            },
                            "failure": None,
                            "usePrevResult": False,
                            "value": [["admin_val"], False]
                        },
                        "failure": None,
                        "usePrevResult": False,
                        "value": ["admin_val", "{0}", False]
                    },
                    "failure": None,
                    "usePrevResult": False,
                    "value": [None, "Chat"]
                }
            ],
            "bottom_view_command": None
        }
    ]
},
    {
    "constraint_name": "Delivery_admin",
    "view": [
        {
            "id": "1",
            "bg_color": "#ffffff",
            "bottom_section_can_expand": "0",
            "bottom_section_can_open": "0",
            "bottom_sheet_color": "#ffffff",
            "center_top_section_data": "1",
            "draggable_sheet_max_height": 0.12,
            "top_section": [
                {
                  "components": [
                      {
                          "component_properties": [
                              "",
                              "0.0,0.0,30.0,30.0",
                              "Delivery status",
                              "left",
                              20,
                              "#000000"
                          ],
                          "type": "text"
                      }
                  ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "ID",
                                "5.0,0.0,30.0,30.0",
                                "Set the current status",
                                "left",
                                16,
                                "#616161"
                            ],
                            "type": "text"
                        }
                    ],
                    "margin": "0.0,0.0,0.0,0.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "current_stage",
                                "0.0,0.0,0.0,0.0",
                                "Not started",
                                "left",
                                15,
                                "#000000"
                            ],
                            "type": "text"
                        },
                        {
                            "component_properties": [
                                "ID",
                                "0.0,0.0,15.0,0.0",
                                "Status message",
                                "Please enter a status message"
                            ],
                            "type": "input"
                        }
                    ],
                    "margin": "30.0,0.0,30.0,30.0"
                },
                {
                    "components": [
                        {
                            "component_properties": [
                                "next_status",
                                "0.0,0.0,30.0,0.0",
                                "Next stage: Stage",
                                "left",
                                14,
                                "#757575"
                            ],
                            "type": "text"
                        },
                        {
                            "type": "button",
                            "component_properties": [
                                "update",
                                "0.0,0.0,0.0,30.0",
                                "UPDATE",
                                "right",
                                {
                                    "commandName": "gev",
                                    "success": {
                                        "commandName": "eq",
                                        "success": {
                                            "commandName": "sev",
                                            "success": {
                                                "commandName": "sld",
                                                "success": None,
                                                "failure": None,
                                                "usePrevResult": False,
                                                "value": [
                                                    "start",
                                                    "custom msg",
                                                    None,
                                                    "Delivery"
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                "status",
                                                "started",
                                                False
                                            ]
                                        },
                                        "failure": {
                                            "commandName": "gev",
                                            "success": {
                                                "commandName": "eq",
                                                "success": {
                                                    "commandName": "sev",
                                                    "success": {
                                                        "commandName": "sld",
                                                        "success": None,
                                                        "failure": None,
                                                        "usePrevResult": False,
                                                        "value": [
                                                            "prep",
                                                            "custom msg",
                                                            None,
                                                            "Delivery"
                                                        ]
                                                    },
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": [
                                                        "status",
                                                        "prep",
                                                        False
                                                    ]
                                                },
                                                "failure": {
                                                    "commandName": "gev",
                                                    "success": {
                                                        "commandName": "eq",
                                                        "success": {
                                                            "commandName": "sev",
                                                            "success": {
                                                                "commandName": "sld",
                                                                "success": None,
                                                                "failure": None,
                                                                "usePrevResult": False,
                                                                "value": [
                                                                    "en_route",
                                                                    "custom msg",
                                                                    None,
                                                                    "Delivery"
                                                                ]
                                                            },
                                                            "failure": None,
                                                            "usePrevResult": False,
                                                            "value": [
                                                                "status",
                                                                "en_route",
                                                                False
                                                            ]
                                                        },
                                                        "failure": {
                                                            "commandName": "gev",
                                                            "success": {
                                                                "commandName": "eq",
                                                                "success": {
                                                                    "commandName": "sev",
                                                                    "success": {
                                                                        "commandName": "sld",
                                                                        "success": None,
                                                                        "failure": None,
                                                                        "usePrevResult": False,
                                                                        "value": [
                                                                            "done",
                                                                            "custom msg",
                                                                            None,
                                                                            "Delivery"
                                                                        ]
                                                                    },
                                                                    "failure": None,
                                                                    "usePrevResult": False,
                                                                    "value": [
                                                                        "status",
                                                                        "done",
                                                                        False
                                                                    ]
                                                                },
                                                                "failure": {
                                                                    "commandName": "gev",
                                                                    "success": {
                                                                        "commandName": "eq",
                                                                        "success": None,
                                                                        "failure": None,
                                                                        "usePrevResult": False,
                                                                        "value": [
                                                                            "{0}",
                                                                            "done"
                                                                        ]
                                                                    },
                                                                    "failure": None,
                                                                    "usePrevResult": False,
                                                                    "value": [
                                                                        [
                                                                            "status"
                                                                        ],
                                                                        False
                                                                    ]
                                                                },
                                                                "usePrevResult": False,
                                                                "value": [
                                                                    "{0}",
                                                                    "en_route"
                                                                ]
                                                            },
                                                            "failure": None,
                                                            "usePrevResult": False,
                                                            "value": [
                                                                [
                                                                    "status"
                                                                ],
                                                                False
                                                            ]
                                                        },
                                                        "usePrevResult": False,
                                                        "value": [
                                                            "{0}",
                                                            "prep"
                                                        ]
                                                    },
                                                    "failure": None,
                                                    "usePrevResult": False,
                                                    "value": [
                                                        [
                                                            "status"
                                                        ],
                                                        False
                                                    ]
                                                },
                                                "usePrevResult": False,
                                                "value": [
                                                    "{0}",
                                                    "started"
                                                ]
                                            },
                                            "failure": None,
                                            "usePrevResult": False,
                                            "value": [
                                                [
                                                    "status"
                                                ],
                                                False
                                            ]
                                        },
                                        "usePrevResult": False,
                                        "value": [
                                            "{0}",
                                            None
                                        ]
                                    },
                                    "failure": None,
                                    "usePrevResult": False,
                                    "value": [
                                        [
                                            "status"
                                        ],
                                        False
                                    ]
                                },
                                None
                            ]
                        }
                    ],
                    "margin": "20.0,0.0,0.0,0.0"
                }
            ],
            "bottom_section": [],
            "top_view_command": [],
            "bottom_view_command": None
        }
    ]
}


]


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
    elif command == "sacv":  # set all views for constraint
        set_all_constraint_views()
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
    else:
        print(f"Unrecognized command: {command}")


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
                "~can the bottom sheet open (1-True, 0-False): ")
            if bottom_section_can_open == "1" or bottom_section_can_open == "0":
                break

        while True:
            bottom_section_can_expand = input(
                "~can the bottom section expand (1-True, 0-False): ")
            if bottom_section_can_expand == "1" or bottom_section_can_expand == "0":
                break
        while True:
            center_top_section_data = input(
                "~should the top section view be centered (1-True, 0-False): ")
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

        constraint_view = input("~constraint view index: ")
        selected_constraint_view: dict = views[int(constraint_view)-1]
    else:
        selected_constraint_view = constraint_view

    result = perform_network_action(
        f"http://constraint-rest-server.herokuapp.com/constraint_view/{constraint_name}", "post", data={"view": jsonpickle.encode(selected_constraint_view)})
    if result["result"] == "success":
        print(f"> [{constraint_name}]'s view set")
    else:
        print("An error occured")


def set_all_constraint_views():
    print("Setting constraint views...")
    for i in range(len(views)):
        name = views[i]["constraint_name"]
        view = views[i]

        result = perform_network_action(
            f"http://constraint-rest-server.herokuapp.com/constraint_view/{name}", "post", data={"view": jsonpickle.encode(view)})
    if result["result"] == "success":
        print(f">Constraint view's set<")
    else:
        print("An error occured")


def create_user():
    global my_user
    user_name = input("~enter name: ")
    my_user = perform_network_action(
        "http://constraint-rest-server.herokuapp.com/create/"+str(user_name), "get")
    print(
        f">[SERVER] User created with name: {my_user['name']}, ID: {my_user['id']}")
    return my_user


def create_task():
    task_name = input("~enter task name: ")
    task_desc = input("~enter task desc: ")
    stage_group_id = input("~enter stage group id: ")
    task_id = perform_network_action("http://constraint-rest-server.herokuapp.com/create_task",
                                     "post", {"task_name": task_name, "task_desc": task_desc, "stage_group_id": stage_group_id})

    print(
        f">[SERVER] Task with name: {task_name}, desc: {task_desc}, ID: {task_id}")


def create_stage_group():
    addr = "http://constraint-rest-server.herokuapp.com/stage_group"
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
    addr = "http://constraint-rest-server.herokuapp.com/stage_group"
    stage_id = input("~enter stage group id: ")


async def create_pipe():
    global my_user, my_pipeline_id

    if my_user == None:
        print("A user has not been created")
        return

    addr = "ws://constraint-rest-server.herokuapp.com:5000/create_pipeline"
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

    addr = "ws://constraint-rest-server.herokuapp.com:5000/start"
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

    addr = "ws://constraint-rest-server.herokuapp.com:5000/start_constraint"
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

    addr = "ws://constraint-rest-server.herokuapp.com:5000/stop_pipeline"
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
