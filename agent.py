"""
IT Support Agent with client-based tool access control.
"""

import os
import json
from typing import Dict, Any, Optional, List
from openai import OpenAI

from memory import ConversationMemory
from tools.tools import ToolRegistry


class ITAgent:
    """IT Support Agent with configurable tool access."""
    
    def __init__(
        self,
        client_config: 'ClientConfig',
        api_key: str,
        model: str = "gpt-4o-mini"
    ):
        """
        Initialize the agent with client-specific configuration.
        
        Args:
            client_config: Client configuration with allowed tools
            api_key: OpenAI API key
            model: Model to use
        """
        self.client_config = client_config
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.memory = ConversationMemory()
        self.tool_registry = client_config.get_tool_registry()
        
        # Build system prompt from client config
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build system prompt from client configuration."""
        base_prompt = f"""You are {self.client_config.agent_name}, an IT support agent for {self.client_config.client_name}.

Your role: {self.client_config.agent_role}

Available tools:
"""
        # Add tool descriptions
        for tool_name in self.client_config.allowed_tools:
            tool = self.tool_registry.get(tool_name)
            if tool:
                base_prompt += f"- {tool.name}: {tool.description}\n"
        
        base_prompt += f"\n{self.client_config.custom_instructions}"
        
        return base_prompt
    
    def process(self, user_message: str) -> Dict[str, Any]:
        """Process a user message and return response."""
        # Add user message to memory
        self.memory.add_user_message(user_message)
        
        # Build messages for API
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.memory.get_history())
        
        # Get allowed tools in OpenAI format
        tools = self.tool_registry.to_openai_format(
            self.client_config.allowed_tools
        )
        
        try:
            # Call OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            # Handle tool calls
            if assistant_message.tool_calls:
                return self._handle_tool_calls(assistant_message)
            else:
                # Just text response
                if assistant_message.content:
                    self.memory.add_assistant_message(assistant_message.content)
                    return {
                        "type": "text",
                        "message": assistant_message.content
                    }
                else:
                    return {
                        "type": "text",
                        "message": "I apologize, I'm having trouble responding. Please try again."
                    }
        except Exception as e:
            return {
                "type": "error",
                "message": f"Error: {str(e)}"
            }
    
    def _handle_tool_calls(self, assistant_message) -> Dict[str, Any]:
        """Handle tool execution."""
        # Add assistant's message with tool calls to memory
        self.memory.messages.append(assistant_message)
        
        results = []
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            # Permission check
            if not self._check_tool_permission(tool_name):
                result = {
                    "success": False,
                    "output": "",
                    "error": f"Tool {tool_name} not authorized for this client"
                }
            else:
                # Execute tool
                tool = self.tool_registry.get(tool_name)
                result = tool.execute(arguments)
            
            results.append({
                "tool": tool_name,
                "arguments": arguments,
                "result": result
            })
            
            # Add to memory
            self.memory.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": result["output"] if result["success"] else result["error"]
            })
        
        # Get final response
        try:
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": self.system_prompt}] + self.memory.messages
            )
            
            final_message = final_response.choices[0].message.content
            if final_message:
                self.memory.add_assistant_message(final_message)
            else:
                final_message = "Tool execution completed."
                self.memory.add_assistant_message(final_message)
            
            return {
                "type": "tool_execution",
                "tool_results": results,
                "message": final_message
            }
        except Exception as e:
            return {
                "type": "tool_execution",
                "tool_results": results,
                "message": f"Tool executed, but error getting response: {str(e)}"
            }
    
    def _check_tool_permission(self, tool_name: str) -> bool:
        """Check if tool is allowed for this client."""
        return tool_name in self.client_config.allowed_tools
    
    def clear_history(self):
        """Clear conversation history."""
        self.memory.clear()

