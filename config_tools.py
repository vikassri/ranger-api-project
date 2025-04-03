base_url = "https://ccycloud.cdpy.root.comops.site:6182/service/public/v2/api/policy"
user_url = "https://ccycloud.cdpy.root.comops.site:6182/service/xusers/users/userName"

columns_dict = {
    "get_policy_by_id": "id",
    "delete_policy_by_id":"id",
    "get_users": "user",
    "delete_users":"user",
    "create_hive_policy": "name"
}

tools = [ {
                "type": "function",
                "function": {
                    "name": "get_policy_by_id",
                    "description": "Get the list of all the policies",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "id of the policy, of policy number",
                            }},
                        "Required": ["id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_policy_by_id",
                    "description": "Delete the policy by id",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "id of the policy, of policy number",
                            }},
                        "Required": ["id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_users",
                    "description": "Get the price by its name",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user": {
                                "type": "string",
                                "description": "name of user, e.g. vikas",
                            }},
                        "Required": ["user"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_users",
                    "description": "Get the price by its name",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user": {
                                "type": "string",
                                "description": "name of user, e.g. vikas",
                            }},
                        "Required": ["user"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "create_hive_policy",
                    "description": "Get the price by its name",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "name of policy, like access:Extenal Database",
                            },
                            "database": {
                                "type": "string",
                                "description": "name of database, like test, default",
                            },
                            "tables": {
                                "type": "string",
                                "description": "name of tables, like all, test",
                            },
                            "access": {
                                "type": "string",
                                "description": "Access of policy, like read, write, all",
                            },
                            "group": {
                                "type": "string",
                                "description": "Groups of policy, like public",
                            },
                            },
                        "Required": ["name","database","access"],
                    },
                },
            },
]