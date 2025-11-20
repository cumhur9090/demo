"""
Tool registry and base classes for IT support tools.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import subprocess
import os


@dataclass
class ToolParameter:
    """Defines a tool parameter."""
    name: str
    type: str
    description: str
    required: bool = True
    enum: Optional[List[str]] = None
    default: Any = None


@dataclass
class Tool:
    """Represents an IT support tool."""
    name: str
    description: str
    category: str  # e.g., "permissions", "authentication", "email"
    script_path: str
    parameters: List[ToolParameter] = field(default_factory=list)
    requires_admin: bool = False
    risk_level: str = "low"  # low, medium, high
    
    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling format."""
        properties = {}
        required = []
        
        for param in self.parameters:
            prop = {
                "type": param.type,
                "description": param.description
            }
            if param.enum:
                prop["enum"] = param.enum
            
            properties[param.name] = prop
            if param.required:
                required.append(param.name)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }
    
    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool's script."""
        # Build command arguments
        args = [self.script_path]
        for param in self.parameters:
            if param.name in arguments:
                args.append(str(arguments[param.name]))
            elif param.default is not None:
                args.append(str(param.default))
        
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else ""
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }


class ToolRegistry:
    """Manages available tools."""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool):
        """Register a tool."""
        self.tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_by_category(self, category: str) -> List[Tool]:
        """Get all tools in a category."""
        return [t for t in self.tools.values() if t.category == category]
    
    def to_openai_format(self, tool_names: List[str] = None) -> List[Dict]:
        """Convert tools to OpenAI format. If tool_names specified, only those."""
        if tool_names:
            tools = [self.tools[name] for name in tool_names if name in self.tools]
        else:
            tools = list(self.tools.values())
        
        return [tool.to_openai_format() for tool in tools]


