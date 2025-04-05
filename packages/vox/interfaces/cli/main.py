"""
CLI interface for Vox Agent OS.
"""
import asyncio
import os
import subprocess
import logging
from typing import Optional
from pathlib import Path

import typer
import openai
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv, find_dotenv

from vox.utils.logging import setup_logger
from vox.voice.recorder import VoiceRecorder
from vox.voice.transcriber import WhisperTranscriber
from vox.voice.speaker import speak
from vox.kernel.agent import Agent

# Initialize logger
logger = setup_logger()
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
    logger.info("Starting voice command session")
    
    try:
        api_key = setup_environment()
        
        # Initialize agent
        agent = Agent()
        
        # Record audio
        recorder = VoiceRecorder()
        console.print("[bold yellow]🎤 Recording...[/bold yellow] Press Ctrl+C to stop")
        recorder.record(duration)
        audio_path = recorder.save()
        
        try:
            # Transcribe
            transcriber = WhisperTranscriber(api_key=api_key)
            console.print("[bold yellow]🎯 Transcribing audio...[/bold yellow]")
            text = transcriber.transcribe(audio_path)
            console.print(f"[bold green]✓ Transcribed:[/bold green] {text}")
            
            # Process with agent
            response = agent.process_request(text)
            
            # Output response
            console.print(f"\n[bold purple]Agent[/bold purple]: {response}\n")
            speak(response)
            
        finally:
            if audio_path.exists():
                audio_path.unlink()
    
    except Exception as e:
        logger.error(f"Error in voice command session: {str(e)}", exc_info=True)
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
    
    while True:
        try:
            request = Prompt.ask("[bold green]You[/bold green]")
            
            if request.lower() == "exit":
                console.print("[yellow]Goodbye![/yellow]")
                break
                
            with console.status("[bold yellow]Thinking...[/bold yellow]"):
                # Process the request synchronously
                response = agent.process_request(request)
            
            console.print(f"\n[bold purple]Agent[/bold purple]: {response}\n")
            
        except Exception as e:
            handle_api_error(e)
            if isinstance(e, (openai.AuthenticationError, openai.RateLimitError)):
                break
            # For other errors, continue the chat loop
            continue

if __name__ == "__main__":
    app() 