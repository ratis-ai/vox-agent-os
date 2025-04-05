"""
Transcription service using OpenAI's Whisper API.
"""
from pathlib import Path
import openai
from rich.console import Console

console = Console()

class WhisperTranscriber:
    def __init__(self, api_key: str = None):
        """Initialize transcriber with optional API key."""
        if api_key:
            openai.api_key = api_key
    
    def transcribe(self, audio_path: Path) -> str:
        """Transcribe audio file using Whisper API."""
        console.print("[bold yellow]🎯 Transcribing audio...[/bold yellow]")
        
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            console.print(f"[bold green]✓ Transcribed:[/bold green] {transcript}")
            return transcript
            
        except Exception as e:
            console.print(f"[bold red]Error transcribing audio:[/bold red] {str(e)}")
            raise 