"""
PR 2: Minimal Working Chat Loop
Build a simple hardcoded chat loop to prove the interaction works.

Files to modify:

demo/main.py - Basic CLI with hardcoded responses
Features:

Simple input/output loop
Hardcoded keyword matching (e.g., "password" → reset response)
Exit command to quit
Immediate demo value - can show working chat
Commit: feat: implement basic chat loop with hardcoded responses"""


import os
import dotenv
import json
from openai import OpenAI

#from demo.tools import tools

dotenv.load_dotenv()


tools_registry = {
    "mail": {
        "name": "mail",
        "description": "Send an email",
        "parameters": {
            "email": "string",
        }
    },
    "settings": {
        "name": "settings",
        "description": "Change a setting within your computer.",
        "parameters": {
            "setting": "string",
            "value": "string",
        }
    },
    "slack": {
        "name": "slack",
        "description": "Send a message to a Slack channel/user.",
        "parameters": {
            "message": "string",
        }
    }
}

def call_tool(tool_name, tool_parameters):
    if tool_name == "mail":
        return "Mail tool response"
    elif tool_name == "settings":
        return "Settings tool response"
    elif tool_name == "slack":
        return "Slack tool response"

def chat_loop():
    messages = []
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    while True:
        user_input = input("You: ")
    
        if user_input == "exit":
            break
        elif user_input == "clear":
            messages = []
            continue
        elif user_input == "help":
            print("Available commands: exit, clear, help")
            print("Available tools: mail, settings, slack")
            print("Example: I need to reset my email password. Please call the reset_password tool.")
            print("Example: I need to send an email to John Doe. Please call the send_email tool.")

            continue


        prompt = f"""You are an IT support agent. 
        
        You are given a user's request and you need to help them with their request. 
        
        If you need to use a tool, you should use the tool to help the user. 
        If you don't need to use a tool, you should respond to the user's request.

        User's request: {user_input}

        Are you confident that you can help the user with their request?

        If you are confident, respond with "Yes, I can help with that.", print which tool you will use, and then call the necessary tools to help the user.
        If you are not confident, respond with "No, I can't help with that." and ask the user to clarify their request.
        

        Explain your reasoning for your answer.

        Availalbe tools:
        {tools_registry}


        Make sure your response is a valid JSON object. Response Schema:
        {{
            "can_assist": "Yes | No",
            "reason": "Reason for your answer",
            "tool_calls": [],
            "tool_call_parameters": [],
            "response": "Yes I can help with that! Please wait while I call the necessary tools to help you." | "[Clarification request]"
        }}


        """


        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages[-5:])


        print(f"Response: {response.choices[0].message.content}")
        assistant_message = response.choices[0].message.content
        print(f"Raw response length: {len(assistant_message)}")
        print(f"First 50 chars: {repr(assistant_message[:50])}")
        print(f"Last 50 chars: {repr(assistant_message[-50:])}")
        print(f"Full response:\n{assistant_message}")
        print("=" * 50)

        # Now try to parse
        try:
            parsed_response = json.loads(assistant_message)
            print(f"Parsed response: {parsed_response}")
        except json.JSONDecodeError as e:
            print(f"JSON Error: {e}")
            print(f"Error at position: {e.pos}")
            if e.pos < len(assistant_message):
                print(f"Character at error position: {repr(assistant_message[e.pos])}")


        #response_json = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": parsed_response['response']})
        print(f"Assistant: {parsed_response}")

        if parsed_response["can_assist"] == "No":
            print(f"Assistant: {parsed_response["response"]}")
            continue

        elif parsed_response["can_assist"] == "Yes":
            print(f"Assistant: {parsed_response["response"]}")
            tool_calls = parsed_response["tool_calls"]
            tool_calls_parameters = parsed_response["tool_call_parameters"]

            for i in range(len(tool_calls)):
                tool_name = tool_calls[i]
                tool_parameters = tool_calls_parameters[i]
                tool_response = call_tool(tool_name, tool_parameters)
                messages.append({"role": "tool", "content": tool_response})
                print(f"Tool: {tool_name} Response: {tool_response}")
            continue

if __name__ == "__main__":
    chat_loop()
