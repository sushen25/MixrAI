import os
import json
import openai

from django.db import connection
from mixr.constants import TOOLS
from termcolor import colored


class AiInterface:
    def __init__(self):
        self.SEED = 42

        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.conversation_history = []

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation_history.append(message)

    def display_conversation(self, detailed=False):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }
        for message in self.conversation_history:
            print(
                colored(
                    f"{message['role']}: {message['content']}\n\n",
                    role_to_color[message["role"]],
                )
            )
    
    # Chat completion requests
    def chat_completion_request(self, messages, tools=None, tool_choice=None):
        # TODO: System messageai
        # You are a professional bartender skilled in the art of making cocktails. You are chatting with a customer who wants to make a cocktail. The customer says:
        
        return self.client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            seed=self.SEED,
            tools=TOOLS,
        )
    
    def chat_completion_with_function_execution(messages):
        pass


    def send_message(self):
        messages = [
            {"role": "system", "content": "Answer the user's question about cocktails by querying the Django database."},
            {"role": "user", "content": "What are some cocktails I can serve in a Collins glass?"},
            # {"role": "user", "content": "I have the following ingredients: Lime Vodka, Apple Juice, Soda water, Lemonade, Orange Juice, Ginger Ale, Fruit Punch, Rum and Ice what are the cocktails I can make?"},
        ]

        chat_response = self.chat_completion_request(messages)
        print("1 ------------------")
        print(chat_response)
        print("2 ------------------")

        assistant_message = chat_response.choices[0].message
        messages.append({"role": "assistant", "content": assistant_message.tool_calls[0].function.name})

        if chat_response.choices[0].finish_reason == "tool_calls":
            results = self.execute_function_call(assistant_message)
            print("FUNCTION EXECUTION RESULTS: ", results)
            messages.append({"role": "tool", "tool_call_id": assistant_message.tool_calls[0].id, "name": assistant_message.tool_calls[0].function.name, "content": results})
        print("3 ------------------")
        self.pretty_print_conversation(messages)

    # Database functions
    def ask_database(self, query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            try:
                rows = cursor.fetchall()
                results = str(rows)
            except Exception as e:
                results = f"query failed with error: {e}"

        return results

    def execute_function_call(self, message):
        function_name = message.tool_calls[0].function.name
        if function_name == "ask_database":
            query = message.tool_calls[0].function.arguments
            print("QUERY: ", query)
            query = json.loads(query)["query"]
            print("QUERY: ", query)
            results = self.ask_database(query)
        else:
            results = f"Error: function {function_name} does not exist"
        return results


    def pretty_print_conversation(self, messages):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "tool": "magenta",
        }
        
        for message in messages:
            if message["role"] == "system":
                print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
            elif message["role"] == "user":
                print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
            elif message["role"] == "assistant" and message.get("function_call"):
                print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
            elif message["role"] == "assistant" and not message.get("function_call"):
                print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
            elif message["role"] == "tool":
                print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

