"""
Executor module for running tools and handling their results.
"""
from typing import Any, Dict, Optional

from ..tools.summarize import summarize_text

class Executor:
    """
    Executor class that:
    - Manages tool registry
    - Executes tools
    - Handles results and errors
    """
    
    def __init__(self, tool_registry: Optional[Dict[str, Any]] = None):
        self.tools = {
            "summarize_text": summarize_text
        }
        if tool_registry:
            self.tools.update(tool_registry)
    
    async def execute_plan(self, plan: Dict) -> str:
        """Execute a plan and return the result."""
        if plan["status"] != "success":
            return f"Failed to create plan: {plan.get('error', 'unknown error')}"
        
        # For MVP, we just execute summarize_text if the plan contains it
        if "summarize" in plan["plan"].lower():
            try:
                # Extract text to summarize (simple heuristic for MVP)
                text = plan["plan"].lower().split("summarize", 1)[1].strip()
                result = await self.tools["summarize_text"](text)
                
                if result["status"] == "success":
                    return result["summary"]
                else:
                    return f"Failed to summarize: {result.get('error', 'unknown error')}"
                    
            except Exception as e:
                return f"Error executing plan: {str(e)}"
        
        return "I can only understand summarization requests for now." 