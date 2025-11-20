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
            "name": "enable_camera_mic",
            "description": "Enable camera and microphone permissions for video conferencing apps like Zoom or Microsoft Teams when they cannot detect the camera or microphone. This opens System Settings and guides the user to enable the necessary permissions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "enum": ["Zoom", "Teams", "Microsoft Teams", "Slack", "Google Meet"],
                        "description": "The name of the application that needs camera/microphone access"
                    },
                    "permission_type": {
                        "type": "string",
                        "enum": ["camera", "microphone", "both"],
                        "description": "The type of permission to enable (camera, microphone, or both)"
                    }
                },
                "required": ["app_name", "permission_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "clear_chrome_cookies",
            "description": "Clear Chrome cookies for a specific domain to fix SSO (Single Sign-On) login loops. Common for corporate authentication issues where users get stuck in redirect loops with Microsoft, Okta, or Google SSO.",
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "The domain to clear cookies for (e.g., 'login.microsoftonline.com', 'accounts.google.com', 'okta.com')"
                    }
                },
                "required": ["domain"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reset_outlook_profile",
            "description": "Reset Microsoft Outlook profile to fix 'Loading Profile' or 'Stuck Syncing' issues. This creates a fresh Outlook profile while backing up the old one.",
            "parameters": {
                "type": "object",
                "properties": {
                    "backup": {
                        "type": "boolean",
                        "description": "Whether to backup the old profile before resetting (default: true)"
                    }
                },
                "required": []
            }
        }
    }
]

def call_tool(tool_name, tool_parameters):
    """Execute a tool by calling its corresponding shell script."""
    import subprocess
    
    script_dir = os.path.join(os.path.dirname(__file__), "scripts")
    
    if tool_name == "enable_camera_mic":
        script_path = os.path.join(script_dir, "enable_camera_mic.sh")
        app_name = tool_parameters.get("app_name", "Zoom")
        permission_type = tool_parameters.get("permission_type", "both")
        args = [script_path, app_name, permission_type]
        
    elif tool_name == "clear_chrome_cookies":
        script_path = os.path.join(script_dir, "clear_chrome_cookies.sh")
        domain = tool_parameters.get("domain", "")
        args = [script_path, domain]
        
    elif tool_name == "reset_outlook_profile":
        script_path = os.path.join(script_dir, "reset_outlook_profile.sh")
        backup = tool_parameters.get("backup", True)
        backup_flag = "true" if backup else "false"
        args = [script_path, backup_flag]
        
    else:
        return f"Unknown tool: {tool_name}"
    
    try:
        # Execute the shell script
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr if result.stderr else 'Script failed'}"
            
    except FileNotFoundError:
        return f"Error: Script not found at {script_path}"
    except subprocess.TimeoutExpired:
        return "Error: Script execution timed out"
    except Exception as e:
        return f"Error executing script: {str(e)}"

def chat_loop():
    messages = []
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages.append({
            "role": "system",
            "content": """You are Joshua, a helpful IT support agent. Help users with common IT issues:
            
1. Camera/Microphone Issues: When users can't access camera or mic in Zoom/Teams, use enable_camera_mic tool
2. SSO Login Loops: When users are stuck in infinite login redirects with corporate SSO, use clear_chrome_cookies tool
3. Outlook Loading Issues: When Outlook is stuck on "Loading Profile" or won't sync, use reset_outlook_profile tool

Be friendly, ask clarifying questions if needed, and explain what you're doing."""
        })


    while True:
        user_input = input("You: ")
    
        if user_input == "exit":
            break
        elif user_input == "clear":
            messages = []
            continue
        elif user_input == "help":
            print("\n=== IT Support Agent - Help ===")
            print("Commands: exit, clear, help")
            print("\nAvailable tools:")
            print("  - enable_camera_mic: Fix camera/microphone for Zoom, Teams, etc.")
            print("  - clear_chrome_cookies: Fix SSO login loops")
            print("  - reset_outlook_profile: Fix Outlook stuck loading/syncing")
            print("\nExample requests:")
            print("  • 'Zoom can't detect my camera'")
            print("  • 'I'm stuck in a login loop with Microsoft SSO'")
            print("  • 'Outlook is stuck on Loading Profile'\n")
            continue


        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            tools=tools_registry,
            messages=messages[-5:],
            tool_choice="auto"
        )



        assistant_message = response.choices[0].message
        if assistant_message == None:
            print(f"Assistant: {response}")
            break

        if assistant_message.tool_calls:
            # Add the assistant's message with tool calls to history
            messages.append(assistant_message)
            
            # If there's a text response along with tool calls, show it
            if assistant_message.content:
                print(f"\nJoshua: {assistant_message.content}")
            
            # Process each tool call
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_parameters = json.loads(tool_call.function.arguments)
                
                print(f"\n🔧 Executing: {tool_name}")
                print(f"   Parameters: {tool_parameters}")
                
                tool_response = call_tool(tool_name, tool_parameters)
                print(f"\n{tool_response}")
                
                # Add tool response to messages with tool_call_id
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": tool_response
                })
            
            # Get final response after tool execution
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            final_message = final_response.choices[0].message.content
            messages.append({"role": "assistant", "content": final_message})
            print(f"\nJoshua: {final_message}")

        else:
            # No tool calls, just a regular text response
            text_response = assistant_message.content
            messages.append({"role": "assistant", "content": text_response})
            print(f"\nJoshua: {text_response}")


if __name__ == "__main__":
    chat_loop()
