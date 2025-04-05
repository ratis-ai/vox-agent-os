"""
Core Agent class that orchestrates multi-agent execution.
"""
import logging
from typing import Optional
from packages.vox.agents.crew_ai.pdf_summarizer_crew import Crew

logger = logging.getLogger("vox")

class Agent:
    def __init__(
        self,
        model: str = "gpt-4-turbo-preview",
        memory_path: Optional[str] = None
    ):
        self.crew = Crew()
        self.model = model
        logger.debug(f"Initialized Agent with model: {model}")
        
    def process_request(self, request: str) -> str:
        """Process a request using the agent crew."""
        logger.info(f"Processing request: {request}")
        
        try:
            response = self.crew.process_request(request)
            logger.debug(f"Generated response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg 