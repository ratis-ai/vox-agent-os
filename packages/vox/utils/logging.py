"""
Logging configuration for the application.
"""
import logging
from pathlib import Path
from typing import Optional

def setup_logger(log_file: Optional[str] = "run.log") -> logging.Logger:
    """Configure and return the application logger."""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("vox")
    logger.setLevel(logging.DEBUG)
    
    # Create formatter for file logging
    file_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_dir / log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Add only file handler (no console handler)
    logger.addHandler(file_handler)
    
    # Prevent logging from propagating to root logger
    logger.propagate = False
    
    return logger 