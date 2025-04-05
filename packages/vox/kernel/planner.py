"""
Planner module for generating execution plans using LLMs.
"""
from typing import Dict, List, Optional
import openai

class Planner:
    """
    Planner class that uses LLMs to:
    - Understand user intent
    - Generate execution plans
    - Select appropriate tools
    """
    
    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.model = model
    
    async def create_plan(
        self,
        request: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict:
        """Generate an execution plan for a user request."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant that creates execution plans. "
                    "Available tools: summarize_text(text: str) -> Dict[str, str]"
                )
            }
        ]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add the current request
        messages.append({
            "role": "user",
            "content": request
        })
        
        try:
            response = await openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            
            return {
                "plan": response.choices[0].message.content,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "plan": "",
                "status": "error",
                "error": str(e)
            } 