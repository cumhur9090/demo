"""Base client configuration."""

from typing import List, Dict, Any, Optional
from tools.tools import ToolRegistry


class ClientConfig:
    """Base configuration for a client."""
    
    def __init__(
        self,
        client_name: str,
        client_id: str,
        allowed_tools: List[str],
        agent_name: str = "Joshua",
        agent_role: str = "IT Support Specialist",
        custom_instructions: str = "",
        tool_overrides: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize client configuration.
        
        Args:
            client_name: Display name of the client company
            client_id: Unique identifier
            allowed_tools: List of tool names this client can use
            agent_name: Name of the agent
            agent_role: Role description
            custom_instructions: Client-specific instructions
            tool_overrides: Custom parameters for specific tools
        """
        self.client_name = client_name
        self.client_id = client_id
        self.allowed_tools = allowed_tools
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.custom_instructions = custom_instructions
        self.tool_overrides = tool_overrides or {}
    
    def get_tool_registry(self) -> ToolRegistry:
        """Build and return tool registry with client-specific tools."""
        from tools.definitions import camera_mic, chrome_cookies, outlook_profile
        import os
        
        registry = ToolRegistry()
        script_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
        
        # Register all available tools
        all_tools = {
            "enable_camera_mic": camera_mic.get_tool(script_dir),
            "clear_chrome_cookies": chrome_cookies.get_tool(script_dir),
            "reset_outlook_profile": outlook_profile.get_tool(script_dir)
        }
        
        # Only register allowed tools
        for tool_name in self.allowed_tools:
            if tool_name in all_tools:
                tool = all_tools[tool_name]
                
                # Apply client-specific overrides
                if tool_name in self.tool_overrides:
                    self._apply_overrides(tool, self.tool_overrides[tool_name])
                
                registry.register(tool)
        
        return registry
    
    def _apply_overrides(self, tool, overrides: Dict[str, Any]):
        """Apply client-specific overrides to a tool."""
        for key, value in overrides.items():
            if hasattr(tool, key):
                setattr(tool, key, value)

