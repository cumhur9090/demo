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


tools_registry = [
    {
        "type": "function",
        "function": {
            "name": "mail",
            "description": "Send an email or diagnose email access issues",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address to send to or diagnose"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["send", "diagnose", "reset_password"],
                        "description": "The action to perform"
                    }
                },
                "required": ["email", "action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "settings",
            "description": "Change a computer setting",
            "parameters": {
                "type": "object",
                "properties": {
                    "setting": {
                        "type": "string",
                        "description": "The setting to change"
                    },
                    "value": {
                        "type": "string",
                        "description": "The new value for the setting"
                    }
                },
                "required": ["setting", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "slack",
            "description": "Send a message to a Slack channel or user",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to send"
                    },
                    "recipient": {
                        "type": "string",
                        "description": "The channel or user to send to"
                    }
                },
                "required": ["message"]
            }
        }
    }
]

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
    messages.append({
            "role": "system",
            "content": "You are a helpful IT support agent. Help users with email, settings, and Slack issues. Use the available tools to assist them."
        })


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


        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            tools=tools_registry,
            messages=messages[-5:],
            tool_choice="auto"
        )



        assistant_message = response.choices[0].message.content
  
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.name
                tool_parameters = tool_call.arguments
                tool_response = call_tool(tool_name, tool_parameters)
                messages.append({"role": "tool", "content": tool_response})
                print(f"Tool: {tool_name} Response: {tool_response}")

            
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages[-10:]
            )
            messages.append({"role": "assistant", "content": final_response.choices[0].message.content})
            print(f"Final response: {final_response.choices[0].message.content}")

        else:
            messages.append({"role": "assistant", "content": assistant_message.content})
            print(f"Assistant: {assistant_message.content}")


if __name__ == "__main__":
    chat_loop()
