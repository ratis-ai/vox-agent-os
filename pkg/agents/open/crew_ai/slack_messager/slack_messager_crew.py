"""
Crew management for Slack messaging coordination.
"""
import os
import json
import logging
from dotenv import load_dotenv
from pkg.tools.open.slack_messager import SlackMessagerTool

logger = logging.getLogger("vox")

class SlackCrew:
    def __init__(self):
        load_dotenv()
        logger.debug("Initializing SlackCrew")
        self.slack_tool = SlackMessagerTool(api_key=os.getenv('COMPOSIO_API_KEY'))
        logger.debug("SlackCrew initialization complete")
    
    def process_request(self, request: str) -> str:
        """Process a Slack message request."""
        try:
            logger.info(f"Processing Slack request: {request}")
            
            # Parse the message request
            try:
                channel_part = request.split("to #")[1].split(":")[0].strip()
                message_part = request.split(":")[1].strip()
                
                message_data = {
                    "channel": channel_part,
                    "message": message_part
                }
                logger.debug(f"Parsed message data: {json.dumps(message_data, indent=2)}")
                
            except Exception as e:
                error_msg = "Invalid message format. Please use: Send a Slack message to #channel: message"
                logger.error(f"Message parsing failed: {str(e)}")
                return error_msg
            
            # Execute the messaging task
            logger.debug("Attempting to send message via SlackTool")
            result = self.slack_tool.send_message(
                channel=message_data["channel"],
                text=message_data["message"]
            )
            logger.debug(f"Slack tool result: {json.dumps(result, indent=2)}")
            
            return f"Message sent to #{message_data['channel']}"
            
        except Exception as e:
            error_msg = f"Error processing Slack request: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg 