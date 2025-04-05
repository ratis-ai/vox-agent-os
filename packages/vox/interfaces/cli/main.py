"""
CLI interface for Vox Agent OS.
"""
import asyncio
import os
import subprocess
from typing import Optional
from pathlib import Path

import typer
import openai
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv, find_dotenv

from ...voice.recorder import VoiceRecorder
from ...voice.transcriber import WhisperTranscriber
from ...voice.speaker import speak
from ...tools.summarize import summarize_text
from ...kernel import Agent

# Initialize console
console = Console()

def setup_environment():
    """Setup environment variables and API keys."""
    # Try to find and load .env file
    env_file = find_dotenv()
    if not env_file:
        console.print("[yellow]Warning: No .env file found. Using system environment variables.[/yellow]")
    load_dotenv(env_file)
    
    # Check for required API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print(
            "\n[bold red]Error: OPENAI_API_KEY not found[/bold red]\n"
            "Please set your OpenAI API key by either:\n"
            "1. Creating a .env file with OPENAI_API_KEY=your-key-here\n"
            "2. Setting the OPENAI_API_KEY environment variable"
        )
        raise typer.Exit(1)
    
    return api_key

def text_to_speech(text: str):
    """Use macOS say command for TTS."""
    subprocess.run(["say", text])

app = typer.Typer(help="Vox Agent OS - Voice-first agent interface")

def handle_api_error(e: Exception):
    """Handle common API errors with user-friendly messages."""
    if isinstance(e, openai.AuthenticationError):
        console.print(
            "\n[bold red]Authentication Error[/bold red]\n"
            "Your OpenAI API key is invalid. Please check your .env file."
        )
    elif isinstance(e, openai.RateLimitError):
        console.print(
            "\n[bold red]OpenAI API Quota Exceeded[/bold red]\n"
            "To fix this:\n"
            "1. Go to https://platform.openai.com/account/billing\n"
            "2. Set up billing if you haven't already\n"
            "3. Check your usage limits\n"
            "4. Add funds if needed"
        )
    else:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@app.command()
def talk(duration: Optional[float] = typer.Option(None)):
    """Record voice command and execute it."""
    api_key = setup_environment()
    openai.api_key = api_key
    
    # Initialize recorder
    recorder = VoiceRecorder(
        sample_rate=int(os.getenv("SAMPLE_RATE", "44100"))
    )
    
    try:
        # Record audio
        recorder.record(duration)
        audio_path = recorder.save()
        
        try:
            # Transcribe
            transcriber = WhisperTranscriber(api_key=api_key)
            text = transcriber.transcribe(audio_path)
            
            # Process command
            if "summarize" in text.lower():
                text_to_summarize = text.lower().split("summarize", 1)[1].strip()
                result = summarize_text(text_to_summarize)
                
                if result["status"] == "success":
                    response = f"Here's your summary: {result['summary']}"
                else:
                    response = f"Sorry, I couldn't summarize that. Error: {result.get('error', 'unknown error')}"
            else:
                response = "I can only summarize text for now. Try saying 'summarize' followed by your text."
            
            # Output response
            console.print(f"\n[bold purple]Agent[/bold purple]: {response}\n")
            speak(response)  # Speak the response
            
        finally:
            # Clean up audio file
            if audio_path.exists():
                audio_path.unlink()
    
    except Exception as e:
        handle_api_error(e)
        raise typer.Exit(1)

@app.command()
def chat(
    model: str = typer.Option("gpt-4", help="Language model to use"),
    memory: Optional[str] = typer.Option(None, help="Path to memory file"),
):
    """Start an interactive text chat session with the agent."""
    # Setup environment and API key
    api_key = setup_environment()
    openai.api_key = api_key
    
    agent = Agent(model=model, memory_path=memory)
    
    console.print("[bold blue]Vox Agent OS[/bold blue] - Text interface")
    console.print("Type 'exit' to quit\n")
    
    def chat_loop():
        while True:
            try:
                request = Prompt.ask("[bold green]You[/bold green]")
                
                if request.lower() == "exit":
                    break
                    
                with console.status("[bold yellow]Thinking...[/bold yellow]"):
                    response = agent.process_request(request)
                
                console.print(f"\n[bold purple]Agent[/bold purple]: {response}\n")
                speak(response)
                
            except Exception as e:
                handle_api_error(e)
                if isinstance(e, (openai.AuthenticationError, openai.RateLimitError)):
                    break

if __name__ == "__main__":
    app() 