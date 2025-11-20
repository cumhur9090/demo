"""
Main entry point for IT Support Agent with client selection.
"""

import os
from dotenv import load_dotenv

from agent import ITAgent
from clients import acmecorp, healthsync, faststart

load_dotenv()

# Client registry
CLIENTS = {
    "acmecorp": acmecorp.get_config(),
    "healthsync": healthsync.get_config(),
    "faststart": faststart.get_config()
}


def main():
    """Main chat loop with client selection."""
    
    print("=" * 60)
    print("IT SUPPORT AGENT - Multi-Client Demo")
    print("=" * 60)
    
    # Select client
    print("\nAvailable clients:")
    client_list = list(CLIENTS.keys())
    for idx, client_id in enumerate(client_list, 1):
        config = CLIENTS[client_id]
        print(f"  {idx}. {config.client_name} ({config.agent_name})")
        print(f"     Tools: {', '.join(config.allowed_tools)}")
    
    while True:
        try:
            choice = input("\nSelect client (1-3): ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(client_list):
                client_id = client_list[choice_idx]
                config = CLIENTS[client_id]
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a number.")
    
    print(f"\n{'=' * 60}")
    print(f"{config.client_name} IT Support")
    print(f"Agent: {config.agent_name}")
    print(f"{'=' * 60}")
    print("\nCommands: 'help', 'clear', 'exit'")
    print("Start chatting below:\n")
    
    # Initialize agent
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key.")
        return
    
    agent = ITAgent(
        client_config=config,
        api_key=api_key
    )
    
    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print(f"\n{config.agent_name}: Goodbye! Have a great day.")
                break
            
            elif user_input.lower() == "help":
                print(f"\n=== {config.client_name} Help ===")
                print("Commands: help, clear, exit")
                print(f"\n(Admin View) Available tools for {config.client_name}:")
                for tool_name in config.allowed_tools:
                    tool = agent.tool_registry.get(tool_name)
                    if tool:
                        print(f"  • {tool.name}: {tool.description}")
                print()
                continue
            
            elif user_input.lower() == "clear":
                agent.clear_history()
                print(f"\n{config.agent_name}: Chat history cleared!\n")
                continue
            
            # Process message
            result = agent.process(user_input)
            
            if result["type"] == "text":
                print(f"\n{config.agent_name}: {result['message']}\n")
            
            elif result["type"] == "tool_execution":
                # Show tool execution
                for tool_result in result["tool_results"]:
                    print(f"\n🔧 Executing: {tool_result['tool']}")
                    print(f"   Arguments: {tool_result['arguments']}")
                    if tool_result["result"]["success"]:
                        print(f"\n{tool_result['result']['output']}")
                    else:
                        print(f"\n❌ Error: {tool_result['result']['error']}")
                
                # Show final message
                print(f"\n{config.agent_name}: {result['message']}\n")
            
            elif result["type"] == "error":
                print(f"\n❌ {result['message']}\n")
        
        except KeyboardInterrupt:
            print(f"\n\n{config.agent_name}: Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}\n")


if __name__ == "__main__":
    main()
