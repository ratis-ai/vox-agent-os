"""
Crew management for coordinating multiple agents.
"""
from typing import Dict, List
import logging
import os
import json
from pkg.agents.open.crew_ai.pdf_summarizer.specialized_agents import ReaderAgent, SummarizerAgent, CoordinatorAgent, FinderAgent

# Get logger
logger = logging.getLogger("vox")

class PDFCrew:
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.agents = {
            "finder": FinderAgent(),
            "reader": ReaderAgent(),
            "summarizer": SummarizerAgent()
        }
        logger.debug(f"Crew initialized with agents: {list(self.agents.keys())}")
    
    def process_request(self, request: str) -> str:
        """Process a request using the appropriate agents."""
        try:
            logger.info(f"Processing request: {request}")
            
            # Let coordinator analyze the request
            plan = self.coordinator.execute_task(
                task=f"Plan how to handle this request: {request}",
                context={"available_agents": list(self.agents.keys())}
            )
            logger.debug(f"Coordinator plan: {json.dumps(plan, indent=2)}")
            
            if plan["status"] != "success":
                return f"Failed to create plan: {plan.get('error', 'unknown error')}"
            
            # Execute the plan using appropriate agents
            if "pdf" in request.lower():
                logger.info("Processing PDF-related request")
                # First find the document
                available_files = os.listdir(os.path.expanduser("~/Downloads"))
                logger.debug(f"Available files in Downloads: {available_files}")
                
                finder_result = self.agents["finder"].execute_task(
                    task=f"Find and return the full path to a document based on approximate name: {request}. Output a JSON object with a single key 'filename' and the value being just the filename of the document without any path prefix.",
                    context={"available_files": f"Here are all the files in the Downloads directory: {available_files}"},
                    output_format="json"
                )
                
                logger.debug("Finder result:")
                logger.debug(f"{json.dumps(finder_result, indent=2)}")
                
                if finder_result["status"] != "success":
                    error_msg = f"Failed to find document: {finder_result.get('error')}"
                    logger.error(error_msg)
                    return error_msg
                
                # Use reader agent
                path = os.path.expanduser("~/Downloads") + "/" + json.loads(finder_result["output"])["filename"]
                logger.info(f"Reading PDF from: {path}")
                
                reader_result = self.agents["reader"].read_document(path)
                logger.debug("Reader result:")
                logger.debug(f"{json.dumps(reader_result, indent=2)}")
                
                if reader_result["status"] == "success":
                    # Then summarizer agent
                    logger.info("Summarizing PDF content")
                    summary_result = self.agents["summarizer"].summarize(reader_result["text"])
                    logger.debug("Summarizer result:")
                    logger.debug(f"{json.dumps(summary_result, indent=2)}")
                    
                    return summary_result.get("summary", "Failed to summarize document")
                
                error_msg = f"Failed to read document: {reader_result.get('error')}"
                logger.error(error_msg)
                return error_msg
            
            logger.warning(f"Unknown request type: {request}")
            return "I'm sorry, I can only handle PDF summarization requests for PDFs in your ~/Downloads folder for now."
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg 