from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletionMessage, ChatCompletion   
from functions import *

def connector(key, user, password, ranger_host, prompt):
    """
    Get Api key and prompt
    """
    if not key or not prompt or not user or not password:
        raise ValueError("Error: Please Provide the Required Details OpenApi Key, User, Password, Prompt")
    
    client = OpenAI(api_key=key)
    os.environ["user"] = user
    os.environ["pass"] = password
    os.environ["host"] = ranger_host
    def run_conversation(main_request: str, tools) -> str:
        """
        Step 1: send the conversation and available functions to the model
        """
        messages = [{"role": "user", "content": main_request}]  # user's message
        tools = tools

        # First Request
        response: ChatCompletion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message: ChatCompletionMessage = response.choices[0].message
        print("* First Response: ", dict(response_message))

        tool_calls = response_message.tool_calls
        if tool_calls is None:
            return response_message.content
        print("* First Reponse Tool Calls: ", list(tool_calls))

        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = functions  
            messages.append(response_message)  # extend conversation with assistant's reply

            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                column_name = get_column(function_to_call.__name__)  # Get the column dynamically
                function_args_dict = {column_name: function_args.get(get_column(function_to_call.__name__))}  # Store key-value pair
                function_response = function_to_call(
                        **function_args_dict  # put location from prompt into location
                    )
                messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )  # extend conversation with function response

            print("* Second Request Messages: ", list(messages))
            second_response: ChatCompletion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )  # get a new response from the model where it can see the function response
            print("* Second Response: ", dict(second_response))
            return second_response.choices[0].message.content
        
    chat_result = run_conversation(prompt, tools)
    return chat_result