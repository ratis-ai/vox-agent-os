"""
PDF reading and processing tool.
"""
import os
from pathlib import Path
from typing import Dict, Optional
import PyPDF2

def read_pdf(filepath: str) -> Dict[str, str]:
    """Read a PDF file and return its text content."""
    try:
        # Handle ~ in filepath
        filepath = os.path.expanduser(filepath)
        path = Path(filepath)
        
        if not path.exists():
            return {
                "text": "",
                "status": "error",
                "error": f"File not found: {filepath}"
            }
            
        if not path.suffix.lower() == '.pdf':
            return {
                "text": "",
                "status": "error",
                "error": "File is not a PDF"
            }
        
        text = ""
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        return {
            "text": text,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "text": "",
            "status": "error",
            "error": str(e)
        }

def find_pdf(filename: str, search_dirs: Optional[list[str]] = None) -> str:
    """Find a PDF file in common directories."""
    if not search_dirs:
        search_dirs = [
            "~/Downloads",
            "~/Documents",
            ".",
        ]
    
    # Ensure filename has .pdf extension
    if not filename.lower().endswith('.pdf'):
        filename += '.pdf'
    
    for directory in search_dirs:
        path = os.path.expanduser(os.path.join(directory, filename))
        if os.path.exists(path):
            return path
    
    return "" 