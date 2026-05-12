"""Tool registry and base tool class"""
from typing import Dict, Any, Callable, Optional
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class Tool(ABC):
    """Base class for all MCP tools"""

    def __init__(self, name: str, description: str, required_params: list = None):
        self.name = name
        self.description = description
        self.required_params = required_params or []

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary format"""
        return {
            "name": self.name,
            "description": self.description,
            "required_params": self.required_params
        }

class ToolRegistry:
    """Registry for all available tools"""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        """Register a new tool"""
        self.tools[tool.name] = tool
        logger.info(f"Tool registered: {tool.name}")

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)

    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        """List all available tools"""
        return {name: tool.to_dict() for name, tool in self.tools.items()}

    async def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool by name"""
        tool = self.get_tool(name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool not found: {name}"
            }

        try:
            result = await tool.execute(**kwargs)
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            logger.error(f"Tool execution error ({name}): {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Global registry instance
tool_registry = ToolRegistry()
