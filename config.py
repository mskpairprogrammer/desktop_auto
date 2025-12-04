"""Configuration constants for desktop_auto project"""
import os
import sys
from dotenv import load_dotenv

# Determine project root - always points to desktop_auto folder
# regardless of whether running as script or frozen executable
if hasattr(sys, 'frozen'):
    # Running as frozen executable - go up from dist folder to project root
    _PROJECT_ROOT = os.path.dirname(os.path.dirname(sys.executable))
else:
    # Running as script
    _PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Load .env file from project root (single source of truth)
_env_path = os.path.join(_PROJECT_ROOT, '.env')
load_dotenv(_env_path)

# Screen coordinates for different operations
# Note: These are read from .env for easy adjustment per screen resolution
class Coordinates:
    """Screen coordinate constants - read from .env"""
    # TradingView focus click (far right middle)
    TRADINGVIEW_FOCUS_X = int(os.getenv('TRADINGVIEW_FOCUS_X', '2523'))
    TRADINGVIEW_FOCUS_Y = int(os.getenv('TRADINGVIEW_FOCUS_Y', '714'))
    
    # TradingView center click
    TRADINGVIEW_CENTER_X = int(os.getenv('TRADINGVIEW_CENTER_X', '1280'))
    TRADINGVIEW_CENTER_Y = int(os.getenv('TRADINGVIEW_CENTER_Y', '800'))
    
    # Symbolik focus click (far right edge area)
    SYMBOLIK_FOCUS_X = int(os.getenv('SYMBOLIK_FOCUS_X', '1900'))
    SYMBOLIK_FOCUS_Y = int(os.getenv('SYMBOLIK_FOCUS_Y', '390'))


# Default configuration values
class Defaults:
    """Default configuration values - read from .env"""
    WINDOW_SETTLE_DELAY = float(os.getenv('WINDOW_SETTLE_DELAY', '3.0'))
    FOCUS_CLICK_DELAY = float(os.getenv('FOCUS_CLICK_DELAY', '1.5'))
    CHART_LOAD_DELAY_TABS_1_3 = float(os.getenv('CHART_LOAD_DELAY_TAB1_3', '7.0'))
    CHART_LOAD_DELAY_TAB_4 = float(os.getenv('CHART_LOAD_DELAY_TAB4', '20.0'))
    SYMBOLIK_WAIT_DELAY = float(os.getenv('SYMBOLIK_WAIT_DELAY', '10.0'))
    SYMBOLIK_REFRESH_WAIT = float(os.getenv('SYMBOLIK_REFRESH_WAIT', '5.0'))
    SYMBOLIK_MATCH_CONFIDENCE = float(os.getenv('SYMBOLIK_MATCH_CONFIDENCE', '0.8'))
    EMAIL_ALERT_THRESHOLD = int(os.getenv('EMAIL_ALERT_THRESHOLD', '60'))
    CAPTURE_INTERVAL_SECONDS = int(os.getenv('CAPTURE_INTERVAL_SECONDS', '3600'))
    CAPTURE_START_TIME = os.getenv('CAPTURE_START_TIME', '09:30')
    CAPTURE_STOP_TIME = os.getenv('CAPTURE_STOP_TIME', '16:00')
    CAPTURE_TIMEZONE = os.getenv('CAPTURE_TIMEZONE', 'US/Eastern')


# File and directory names
class Paths:
    """Path constants"""
    # Use standalone data folder in parent directory for both executable and source code
    # This ensures both write to the same location regardless of where they're run from
    if hasattr(sys, 'frozen'):
        # Running as frozen executable - go up from dist folder
        _script_dir = os.path.dirname(sys.executable)  # dist folder
        BASE_DIR = os.path.dirname(_script_dir)  # desktop_auto folder
        PROJECT_ROOT = BASE_DIR  # Project root (desktop_auto folder)
    else:
        # Running as script
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # desktop_auto folder
        PROJECT_ROOT = BASE_DIR
    
    # Create data folder in parent directory of project
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
    
    SCREENSHOTS_DIR = os.path.join(DATA_DIR, "screenshots")
    STOCK_SYMBOLS_FILE = os.path.join(DATA_DIR, "stock_symbols.txt")
    LOG_FILE = "desktop_auto.log"
    ENV_FILE = os.path.join(PROJECT_ROOT, ".env")  # Always read from project root
    COMBINED_ANALYSIS_FILE = "combined_analysis_latest.txt"
    MULTI_PROVIDER_HTML_FILE = "multi_provider_analysis.html"


# Window title keywords for automation
class Windows:
    """Window title constants - read from .env"""
    TRADINGVIEW_TREND_ANALYSIS = os.getenv('TRADINGVIEW_WINDOW1', 'trend analysis')
    TRADINGVIEW_HEIKEN_ASHI = os.getenv('TRADINGVIEW_WINDOW2', 'Smoothed Heiken Ashi Candles')
    TRADINGVIEW_VOLUME_LAYOUT = os.getenv('TRADINGVIEW_WINDOW3', 'volume layout')
    TRADINGVIEW_VOLUME_PROFILE = os.getenv('TRADINGVIEW_WINDOW4', 'volumeprofile')
    SYMBOLIK = os.getenv('SYMBOLIK_WINDOW', 'workspace')


# Screenshot filename patterns
class Screenshots:
    """Screenshot filename patterns - read from .env (use .format(symbol=symbol))"""
    TAB1 = os.getenv('SCREENSHOT_NAME_TAB1', '{symbol}_luxoalgo.png')
    TAB2 = os.getenv('SCREENSHOT_NAME_TAB2', '{symbol}_heiken.png')
    TAB3 = os.getenv('SCREENSHOT_NAME_TAB3', '{symbol}_volume_layout.png')
    TAB4 = os.getenv('SCREENSHOT_NAME_TAB4', '{symbol}_rvol.png')
    SYMBOLIK = os.getenv('SCREENSHOT_NAME_SYMBOLIK', '{symbol}_symbolik.png')


# API configuration
class API:
    """API configuration constants - read from .env"""
    PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
    # Model names can be overridden via environment variables
    PERPLEXITY_MODEL = os.getenv('PERPLEXITY_MODEL', 'sonar')
    CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')
    GOOGLE_AI_MODEL = os.getenv('GOOGLE_AI_MODEL', 'gemini-3-pro-preview')
    
    # Retry configuration - read from .env
    MAX_RETRY_ATTEMPTS = int(os.getenv('API_MAX_RETRY_ATTEMPTS', '5'))
    RETRY_BASE_DELAY = float(os.getenv('API_RETRY_BASE_DELAY', '1.0'))
    
    # Request configuration - read from .env
    MAX_TOKENS = int(os.getenv('API_MAX_TOKENS', '4000'))
    TEMPERATURE = float(os.getenv('API_TEMPERATURE', '0.2'))


# SMTP configuration
class SMTP:
    """SMTP configuration constants - read from .env"""
    DEFAULT_SERVER = os.getenv('SMTP_DEFAULT_SERVER', 'smtp.gmail.com')
    DEFAULT_PORT = int(os.getenv('SMTP_DEFAULT_PORT', '587'))
