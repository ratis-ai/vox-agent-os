"""
Voice recorder module for capturing audio input.
"""
import logging
import tempfile
from pathlib import Path
import sounddevice as sd
import numpy as np
import wavio
from rich.console import Console

logger = logging.getLogger("vox")
console = Console()

class VoiceRecorder:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.recording = None
        self.temp_dir = Path(tempfile.gettempdir())
        logger.debug(f"Initialized VoiceRecorder with sample rate: {sample_rate}")
        self._recording_complete = False
    
    def record(self, duration=None):
        """Record audio from microphone.
        If duration is None, records until stop_recording is called."""
        logger.info("Starting audio recording")
        console.print("[bold yellow]🎤 Recording...[/bold yellow] Press Ctrl+C to stop")
        try:
            if duration:
                logger.debug(f"Recording for fixed duration: {duration}s")
                self.recording = sd.rec(
                    int(duration * self.sample_rate),
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype=np.int16
                )
                sd.wait()
            else:
                logger.debug("Recording until interrupted")
                self.recording = sd.rec(
                    int(30 * self.sample_rate),  # Max 30 seconds
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype=np.int16
                )
                
                # Wait for Ctrl+C
                try:
                    while not self._recording_complete:
                        sd.sleep(100)
                except KeyboardInterrupt:
                    # Stop recording on first Ctrl+C
                    sd.stop()
                    self._recording_complete = True
                    logger.info("Recording stopped by user")
                
        except Exception as e:
            logger.error(f"Error during recording: {str(e)}", exc_info=True)
            console.print(f"[bold red]Recording error:[/bold red] {str(e)}")
            raise
    
    def save(self) -> Path:
        """Save recording to temporary WAV file and return path."""
        if self.recording is None:
            logger.error("No recording available to save")
            raise ValueError("No recording available")
        
        output_path = self.temp_dir / f"vox_recording_{id(self)}.wav"
        logger.debug(f"Saving recording to: {output_path}")
        
        try:
            wavio.write(
                str(output_path),
                self.recording,
                self.sample_rate,
                sampwidth=2
            )
            logger.info("Recording saved successfully")
            return output_path
            
        except Exception as e:
            logger.error(f"Error saving recording: {str(e)}", exc_info=True)
            raise 