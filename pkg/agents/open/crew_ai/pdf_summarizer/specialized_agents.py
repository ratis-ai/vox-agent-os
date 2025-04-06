"""
Specialized agents for different tasks.
"""
from pkg.agents.open.crew_ai.base import BaseAgent
from pkg.tools.open.summarize import summarize_text
from pkg.tools.open.pdf_reader import read_pdf
from typing import Dict
from pprint import pprint

class FinderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Finder",
            role="Document Finder",
            goal="Finds the full path to a document based on approximate name",
            backstory="Expert at finding documents from approximate names."
        )

class ReaderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Reader",
            role="Document Analysis Specialist",
            goal="Extract and understand content from documents",
            backstory="Expert at reading and processing various document formats"
        )
        
    def read_document(self, filepath: str) -> Dict:
        """Read and process a document."""
        result = read_pdf(filepath)
        return result

class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Summarizer",
            role="Content Summarization Expert",
            goal="Create concise, accurate summaries",
            backstory="Specialized in distilling complex information into clear summaries"
        )
        
    def summarize(self, text: str) -> Dict:
        """Summarize given text."""
        return summarize_text(text)

class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Coordinator",
            role="Task Coordinator",
            goal="Coordinate tasks between specialized agents",
            backstory="Expert at breaking down requests and orchestrating agent collaboration"
        ) 