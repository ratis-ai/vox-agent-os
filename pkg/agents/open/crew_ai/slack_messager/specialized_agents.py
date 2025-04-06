"""
Specialized agents for Slack messaging.
"""
from pkg.agents.open.crew_ai.base import BaseAgent
from pkg.tools.open.slack_messager import SlackMessagerTool
from typing import Dict
import os

class SlackParserAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SlackParser",
            role="Slack Message Parser",
            goal="Parse Slack messages and validate format",
            backstory="Expert at parsing and validating Slack messages"
        )

class SlackMessagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SlackMessenger",
            role="Slack Communication Specialist",
            goal="Send messages to Slack channels accurately",
            backstory="Expert at formatting and sending messages to Slack channels"
        )
        self.slack_tool = SlackMessagerTool(api_key=os.getenv('COMPOSIO_API_KEY'))
        
    def send_message(self, channel: str, message: str) -> Dict:
        """Send a message to a Slack channel."""
        try:
            result = self.slack_tool.send_message(channel, message)
            return {
                "status": "success",
                "message": f"Message sent to #{channel}",
                "response": result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

class SlackCoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SlackCoordinator",
            role="Slack Task Coordinator",
            goal="Coordinate Slack messaging tasks",
            backstory="Expert at parsing and validating Slack message requests"
        )
