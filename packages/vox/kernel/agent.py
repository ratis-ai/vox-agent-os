"""
Core Agent class that orchestrates multi-agent execution.
"""
import logging
from typing import Optional, Tuple
from rich.console import Console
from rich.prompt import Prompt
from vox.agents.crew_ai.pdf_summarizer.pdf_summarizer_crew import PDFCrew
from vox.agents.crew_ai.slack_messager.slack_messager_crew import SlackCrew
from pprint import pprint

logger = logging.getLogger("vox")
console = Console()

class Agent:
    def __init__(
        self,
        model: str = "gpt-4",
        memory_path: Optional[str] = None
    ):
        self.model = model
        logger.debug(f"Initialized Agent with model: {model}")

    def show_menu(self) -> str:
        """Display menu and get user choice"""
        console.print("\n[bold blue]Available Commands:[/bold blue]")
        console.print("1. Summarize a PDF")
        console.print("2. Send a message to Slack")
        console.print("3. Exit")
        
        choice = Prompt.ask("\n[bold green]Choose an option[/bold green]", choices=["1", "2", "3"])
        return choice

    def get_command_input(self, choice: str) -> str:
        """Get appropriate input based on user choice"""
        if choice == "1":
            return Prompt.ask("[bold yellow]Enter the name of the PDF to summarize[/bold yellow]")
        elif choice == "2":
            channel = Prompt.ask("[bold yellow]Enter Slack channel[/bold yellow] (with #)")
            message = Prompt.ask("[bold yellow]Enter your message[/bold yellow]")
            return f"Send a Slack message to {channel}: {message}"
        return ""

    def process_request(self, defaults: dict = {}) -> str:
        """Process a request using the appropriate crew."""
        try:
            # Check for defaults
            request = ""
            if defaults:
                request = defaults.get("request", "")
                choice = defaults.get("choice", "")
                if choice == "2":
                    channel = defaults.get("channel", "")
                    message = defaults.get("message", "")
                    request = f"Send a Slack message to {channel}: {message}"
                    print("Applying defaults:")
                    pprint(defaults)

            else:
                # Always show menu first
                choice = self.show_menu()
                
                if choice == "3":
                    return "Goodbye!"
                
                # Get input based on choice
                request = self.get_command_input(choice)
            
            if not request:
                return "Invalid input"

            # Route to appropriate crew
            if choice == "1":
                self.pdf_crew = PDFCrew()
                response = self.pdf_crew.process_request(request)
            elif choice == "2":
                self.slack_crew = SlackCrew()
                response = self.slack_crew.process_request(request)
            else:
                response = "Invalid command type"

            logger.debug(f"Generated response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg 