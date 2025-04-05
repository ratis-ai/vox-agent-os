"""
Text-to-speech module using system commands.
"""
import subprocess
from rich.console import Console

console = Console()

def speak(text: str):
    """Use macOS say command for TTS."""
    try:
        subprocess.run(["say", text])
    except Exception as e:
        console.print(f"[bold red]Error speaking:[/bold red] {str(e)}")
