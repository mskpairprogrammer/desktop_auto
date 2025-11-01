"""
Shared utility functions for the desktop_auto project
"""
import base64
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Constants
SCREENSHOTS_DIR = "screenshots"
COMBINED_ANALYSIS_FILENAME = "combined_analysis_latest.txt"
MULTI_PROVIDER_HTML_FILENAME = "multi_provider_analysis.html"

# Chart window identifiers
WINDOW_TREND_ANALYSIS = "trend analysis"
WINDOW_HEIKEN_ASHI = "Smoothed Heiken Ashi Candles"
WINDOW_VOLUME_LAYOUT = "volume layout"
WINDOW_VOLUME_PROFILE = "volumeprofile"
WINDOW_SYMBOLIK = "workspace"


def encode_image_to_base64(image_path: str) -> str:
    """
    Encode an image file to base64 string with data URI
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded image as data URI
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        IOError: If image cannot be read
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        
        # Determine the MIME type based on file extension
        file_ext = os.path.splitext(image_path)[1].lower()
        if file_ext == '.png':
            mime_type = 'image/png'
        elif file_ext in ['.jpg', '.jpeg']:
            mime_type = 'image/jpeg'
        elif file_ext == '.gif':
            mime_type = 'image/gif'
        elif file_ext == '.webp':
            mime_type = 'image/webp'
        else:
            mime_type = 'image/png'  # Default to PNG
        
        image_data_uri = f"data:{mime_type};base64,{base64_image}"
        return image_data_uri
        
    except IOError as e:
        logger.error(f"Error reading image {image_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error encoding image {image_path}: {e}")
        raise


def sanitize_for_logging(text: str, sensitive_patterns: Optional[list] = None) -> str:
    """
    Sanitize text for logging by redacting sensitive information
    
    Args:
        text: Text to sanitize
        sensitive_patterns: List of patterns to redact (default: API keys, passwords)
        
    Returns:
        Sanitized text with sensitive info redacted
    """
    if not text:
        return text
    
    import re
    
    if sensitive_patterns is None:
        sensitive_patterns = [
            r'pplx-[a-zA-Z0-9]+',  # Perplexity API key
            r'sk-ant-[a-zA-Z0-9\-]+',  # Anthropic API key
            r'AIza[a-zA-Z0-9\-_]+',  # Google API key
            r'password["\']?\s*[:=]\s*["\']?[^"\'\s]+',  # Passwords
            r'api[_-]?key["\']?\s*[:=]\s*["\']?[^"\'\s]+',  # Generic API keys
        ]
    
    sanitized = text
    for pattern in sensitive_patterns:
        sanitized = re.sub(pattern, '[REDACTED]', sanitized, flags=re.IGNORECASE)
    
    return sanitized


def get_base_dir() -> str:
    """
    Get the base directory for the application
    Works for both script and frozen executable modes
    
    Returns:
        Absolute path to the base directory
    """
    import sys
    
    if getattr(sys, 'frozen', False):
        # Running as EXE
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))


def ensure_directory_exists(directory: str) -> None:
    """
    Ensure a directory exists, creating it if necessary
    
    Args:
        directory: Path to directory
        
    Raises:
        OSError: If directory cannot be created
    """
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        raise
