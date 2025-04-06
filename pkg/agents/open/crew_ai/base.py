"""
Base agent class for specialized agents.
"""
from typing import Dict, List, Optional
import logging
import json
import openai

# Get logger
logger = logging.getLogger("vox")

class BaseAgent:
    def __init__(
        self,
        name: str,
        role: str,
        goal: str,
        backstory: str,
        model: str = "gpt-4o",
    ):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.model = model
        
        logger.info(f"Initializing agent: {self.name}")
        logger.debug(
            "Agent parameters:\n"
            f"Name: {self.name}\n"
            f"Role: {self.role}\n"
            f"Goal: {self.goal}\n"
            f"Backstory: {self.backstory}\n"
            f"Model: {self.model}"
        )

    def execute_task(self, task: str, context: Optional[Dict] = None, output_format: Optional[str] = None) -> Dict:
        """Execute a specific task with given context."""
        logger.info(f"Agent {self.name} executing task: {task[:100]}...")
        
        messages = self._build_messages(task, context)
        logger.debug(f"Agent {self.name} messages: {json.dumps(messages, indent=2)}")

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                response_format={"type": "json_object"} if output_format == "json" else None
            )
            
            logger.debug(f"Agent {self.name} response: {json.dumps(response.choices[0].message.content[:500], indent=2)}")
            
            return {
                "status": "success",
                "output": response.choices[0].message.content
            }
            
        except Exception as e:
            logger.error(f"Agent {self.name} error: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _build_messages(self, task: str, context: Optional[Dict] = None) -> List[Dict]:
        """Build message list for the agent."""
        logger.debug(f"Building messages for agent {self.name}")
        
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are {self.name}, {self.role}.\n"
                    f"Your goal is: {self.goal}\n"
                    f"Backstory: {self.backstory}\n"
                    "Respond based on your role and expertise."
                )
            }
        ]
        
        if context:
            logger.debug(f"Adding context to messages for agent {self.name}")
            messages.append({
                "role": "system",
                "content": f"Context: {str(context)}"
            })
        
        messages.append({
            "role": "user",
            "content": task
        })
        
        return messages 