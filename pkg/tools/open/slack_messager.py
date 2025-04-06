from composio_openai import ComposioToolSet, App
from typing import Optional, Dict
import logging
import json

logger = logging.getLogger("vox")

class SlackMessagerTool:
    def __init__(self, api_key: Optional[str] = None):
        logger.debug("Initializing SlackMessagerTool")
        self.toolset = ComposioToolSet(entity_id="default")
        self._setup_connection()
        logger.debug("SlackMessagerTool initialization complete")

    def _setup_connection(self):
        """Setup initial connection with Slack"""
        logger.debug("Setting up Slack connection")
        try:
            connection_request = self.toolset.initiate_connection(
                app=App.SLACK,
                entity_id="default",
            )
            # Store connection details
            self.connected_account_id = connection_request.connectedAccountId
            logger.debug(f"Connection established. Account ID: {self.connected_account_id}")
            
            # Get available tools for debugging
            tools = self.toolset.get_tools(apps=[App.SLACK])
            logger.debug(f"# Tools: {len(tools)}")
            
        except Exception as e:
            logger.error(f"Connection setup failed: {str(e)}", exc_info=True)
            raise Exception(f"Failed to setup Slack connection: {str(e)}")

    def get_channels(self) -> Dict:
        """
        Get all channels from Slack
        """
        return self.toolset.get_channels(apps=[App.SLACK])

    def send_message(self, channel: str, text: str) -> Dict:
        """
        Send a message to a Slack channel using Composio
        
        Args:
            channel (str): Channel name (with or without #)
            text (str): Message text to send
            
        Returns:
            dict: Response from Slack API
        """
        logger.debug(f"Attempting to send message to channel: {channel}")
        logger.debug(f"Message text: {text}")
        
        # Normalize channel name (ensure it has #)
        channel = f"#{channel.lstrip('#')}"
        logger.debug(f"Normalized channel name: {channel}")
        
        try:
            logger.debug("Preparing to execute Slack action")
            params = {
                'channel': channel,
                'text': text
            }
            logger.debug(f"Action parameters: {json.dumps(params, indent=2)}")
            
            # Using the correct action name from the tools list
            response = self.toolset.execute_action(
                action="SLACK_SENDS_A_MESSAGE_TO_A_SLACK_CHANNEL",
                params=params
            )
            logger.debug(f"Slack API response: {json.dumps(response, indent=2)}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}", exc_info=True)
            logger.error(f"Parameters used: {json.dumps(params, indent=2)}")
            raise Exception(f"Failed to send Slack message: {str(e)}")