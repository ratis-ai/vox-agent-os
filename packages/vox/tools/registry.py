"""
Tool registry for managing and executing agent tools.
"""
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel

class ToolSpec(BaseModel):
    """Specification for a tool that can be executed by the agent."""
    name: str
    description: str
    inputs: List[str]
    output: str
    auth_required: bool = False
    handler: Optional[Callable] = None

class ToolRegistry:
    """Registry for managing and executing tools."""
    
    def __init__(self):
        self._tools: Dict[str, ToolSpec] = {}
        
    def register(self, tool: ToolSpec) -> None:
        """Register a new tool."""
        self._tools[tool.name] = tool
        
    def get_tool(self, name: str) -> Optional[ToolSpec]:
        """Get a tool by name."""
        return self._tools.get(name)
        
    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
        
    async def execute_tool(self, name: str, **kwargs: Any) -> Any:
        """Execute a tool by name with given arguments."""
        tool = self.get_tool(name)
        if not tool or not tool.handler:
            raise ValueError(f"Tool {name} not found or has no handler")
            
        return await tool.handler(**kwargs)

# Example built-in tools
BUILTIN_TOOLS = [
    ToolSpec(
        name="summarize_text",
        description="Summarize a piece of text",
        inputs=["text"],
        output="summary",
        auth_required=False
    ),
    ToolSpec(
        name="search_web",
        description="Search the web for information",
        inputs=["query"],
        output="results",
        auth_required=False
    )
] 