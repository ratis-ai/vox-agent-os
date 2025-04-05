"""
Core Agent class that orchestrates planning and execution of user requests.
"""
from typing import Any, Dict, List, Optional

from .planner import Planner
from .executor import Executor

class Agent:
    """
    Core Agent class that handles:
    - Understanding user intent
    - Planning actions using tools
    - Executing plans
    - Maintaining conversation context
    """
    
    def __init__(
        self,
        model: str = "gpt-4-turbo-preview",
        memory_path: Optional[str] = None,
        tool_registry: Optional[Dict[str, Any]] = None
    ):
        self.planner = Planner(model=model)
        self.executor = Executor(tool_registry=tool_registry or {})
        self.conversation_history: List[Dict[str, str]] = []
        
    async def process_request(self, request: str) -> str:
        """Process a user request through the plan → execute → respond loop."""
        # Add request to history
        self.conversation_history.append({"role": "user", "content": request})
        
        try:
            # Generate plan
            plan = await self.planner.create_plan(
                request,
                conversation_history=self.conversation_history
            )
            
            # Execute plan
            response = await self.executor.execute_plan(plan)
            
            # Add response to history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            self.conversation_history.append({"role": "assistant", "content": error_msg})
            return error_msg
    
    def reset(self):
        """Reset the agent's conversation history."""
        self.conversation_history = [] 