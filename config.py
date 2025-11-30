"""
Configuration constants for desktop_auto project
"""
import os
import sys

# Screen coordinates for different operations
# Note: These are hardcoded for specific screen resolutions and may need adjustment
class Coordinates:
    """Screen coordinate constants"""
    # TradingView focus click (far right middle)
    TRADINGVIEW_FOCUS_X = 2523
    TRADINGVIEW_FOCUS_Y = 714
    
    # TradingView center click
    TRADINGVIEW_CENTER_X = 1280
    TRADINGVIEW_CENTER_Y = 800
    
    # Symbolik focus click (far right edge area)
    SYMBOLIK_FOCUS_X = 1900
    SYMBOLIK_FOCUS_Y = 390


# Default configuration values
class Defaults:
    """Default configuration values"""
    WINDOW_SETTLE_DELAY = 3.0
    FOCUS_CLICK_DELAY = 1.5
    CHART_LOAD_DELAY_TABS_1_3 = 5.0
    CHART_LOAD_DELAY_TAB_4 = 15.0
    SYMBOLIK_WAIT_DELAY = 5.0
    SYMBOLIK_REFRESH_WAIT = 5.0
    SYMBOLIK_MATCH_CONFIDENCE = 0.8
    EMAIL_ALERT_THRESHOLD = 60
    CAPTURE_INTERVAL_SECONDS = 3600
    CAPTURE_START_TIME = "09:30"
    CAPTURE_STOP_TIME = "16:00"
    CAPTURE_TIMEZONE = "US/Eastern"


# File and directory names
class Paths:
    """Path constants"""
    # Use standalone data folder in parent directory for both executable and source code
    # This ensures both write to the same location regardless of where they're run from
    if hasattr(sys, 'frozen'):
        # Running as frozen executable - go up from dist folder
        _script_dir = os.path.dirname(sys.executable)  # dist folder
        BASE_DIR = os.path.dirname(_script_dir)  # desktop_auto folder
    else:
        # Running as script
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # desktop_auto folder
    
    # Create data folder in parent directory of project
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
    
    SCREENSHOTS_DIR = os.path.join(DATA_DIR, "screenshots")
    STOCK_SYMBOLS_FILE = os.path.join(DATA_DIR, "stock_symbols.txt")
    LOG_FILE = "desktop_auto.log"
    ENV_FILE = ".env"
    COMBINED_ANALYSIS_FILE = "combined_analysis_latest.txt"
    MULTI_PROVIDER_HTML_FILE = "multi_provider_analysis.html"


# Window title keywords for automation
class Windows:
    """Window title constants"""
    TRADINGVIEW_TREND_ANALYSIS = "trend analysis"
    TRADINGVIEW_HEIKEN_ASHI = "Smoothed Heiken Ashi Candles"
    TRADINGVIEW_VOLUME_LAYOUT = "volume layout"
    TRADINGVIEW_VOLUME_PROFILE = "volumeprofile"
    SYMBOLIK = "workspace"


# Screenshot filename patterns
class Screenshots:
    """Screenshot filename patterns (use .format(symbol=symbol))"""
    TAB1 = "{symbol}_tab1.png"
    TAB2 = "{symbol}_tab2.png"
    TAB3 = "{symbol}_tab3.png"
    TAB4 = "{symbol}_tab4.png"
    SYMBOLIK = "{symbol}_symbolik.png"


# API configuration
class API:
    """API configuration constants"""
    PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
    # Model names can be overridden via environment variables
    PERPLEXITY_MODEL = os.getenv('PERPLEXITY_MODEL', 'sonar')
    CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')
    GOOGLE_AI_MODEL = os.getenv('GOOGLE_AI_MODEL', 'gemini-3-pro-preview')
    
    # Retry configuration
    MAX_RETRY_ATTEMPTS = 5
    RETRY_BASE_DELAY = 1.0
    
    # Request configuration
    MAX_TOKENS = 4000
    TEMPERATURE = 0.2


# SMTP configuration
class SMTP:
    """SMTP configuration constants"""
    DEFAULT_SERVER = "smtp.gmail.com"
    DEFAULT_PORT = 587
