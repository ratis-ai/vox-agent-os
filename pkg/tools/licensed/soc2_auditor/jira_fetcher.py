"""
Tool for fetching and analyzing Jira tickets related to SOC 2 controls.
"""
import os
import logging
from typing import Dict, List
from jira import JIRA  # You'll need to add python-jira to dependencies

logger = logging.getLogger("vox")

class JiraFetcher:
    def __init__(self):
        self.jira = JIRA(
            server=os.getenv("JIRA_SERVER"),
            basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_TOKEN"))
        )
        
    def fetch_tickets(self, ticket_ids: List[str]) -> Dict[str, Dict]:
        """
        Fetch tickets and their implementation status.
        
        Args:
            ticket_ids: List of Jira ticket keys
            
        Returns:
            Dictionary mapping ticket IDs to their details
        """
        results = {}
        for ticket_id in ticket_ids:
            try:
                issue = self.jira.issue(ticket_id)
                results[ticket_id] = {
                    "status": issue.fields.status.name,
                    "resolution": issue.fields.resolution.name if issue.fields.resolution else None,
                    "last_updated": issue.fields.updated,
                    "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None
                }
            except Exception as e:
                logger.error(f"Error fetching ticket {ticket_id}: {str(e)}")
                results[ticket_id] = {"error": str(e)}
                
        return results 