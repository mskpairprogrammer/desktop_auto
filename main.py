#!/usr/bin/env python3
"""
Desktop Auto Project - TradingView Automation for 4 Separate Windows
"""
import pyautogui
import time
import os
import sys
from datetime import datetime, time as dt_time
from dotenv import load_dotenv

try:
    import pytz
    PYTZ_AVAILABLE = True
except ImportError:
    log("⚠️ pytz not available. Install with: pip install pytz")
    PYTZ_AVAILABLE = False

try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

try:
    from perplexity_analysis import PerplexityAnalyzer, EmailAlertManager
    PERPLEXITY_AVAILABLE = True
except ImportError:
    log("⚠️ Perplexity analysis module not available. Install with: pip install openai")
    PERPLEXITY_AVAILABLE = False

# Load environment variables
load_dotenv()


def log(message):
    """Print message with timestamp and save to log file with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")
    
    # Write to log file with timestamp
    try:
        # Get the directory where the script/executable is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            script_dir = os.path.dirname(os.path.abspath(__file__))
        
        log_file = os.path.join(script_dir, 'desktop_auto.log')
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        # Don't let logging errors break the main program
        print(f"Warning: Could not write to log file: {e}")


def load_stock_symbols():
    """Load stock symbols from stock_symbols.txt file"""
    try:
        # Get the directory where the script/executable is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            script_dir = os.path.dirname(os.path.abspath(__file__))
        
        symbols_file = os.path.join(script_dir, 'stock_symbols.txt')
        
        with open(symbols_file, 'r') as f:
            symbols = [line.strip() for line in f.readlines() if line.strip()]
        if not symbols:
            log("⚠️ No symbols found in stock_symbols.txt, using default QBTS")
            return ['QBTS']
        log(f"📊 Loaded {len(symbols)} symbols from stock_symbols.txt: {', '.join(symbols)}")
        return symbols
    except FileNotFoundError:
        log("⚠️ stock_symbols.txt not found, falling back to STOCK_SYMBOLS env var")
        symbols_str = os.getenv('STOCK_SYMBOLS', 'QBTS')
        return [s.strip() for s in symbols_str.split(',')]
    except Exception as e:
        log(f"⚠️ Error reading stock_symbols.txt: {e}, using default QBTS")
        return ['QBTS']


def is_within_market_hours():
    """Check if current time is within configured market hours."""
    schedule_enabled = os.getenv('SCHEDULE_ENABLED', 'False').lower() == 'true'
    
    if not schedule_enabled:
        return True  # Always run if scheduling is disabled
    
    if not PYTZ_AVAILABLE:
        log("⚠️ pytz not available - cannot check market hours. Running anyway.")
        return True
    
    try:
        # Get timezone and market hours from env
        timezone_str = os.getenv('CAPTURE_TIMEZONE', 'US/Eastern')
        start_time_str = os.getenv('CAPTURE_START_TIME', '09:30')
        stop_time_str = os.getenv('CAPTURE_STOP_TIME', '16:00')
        
        # Parse timezone
        tz = pytz.timezone(timezone_str)
        current_time = datetime.now(tz)
        
        # Parse start and stop times
        start_hour, start_min = map(int, start_time_str.split(':'))
        stop_hour, stop_min = map(int, stop_time_str.split(':'))
        
        start_time = dt_time(start_hour, start_min)
        stop_time = dt_time(stop_hour, stop_min)
        
        current_time_only = current_time.time()
        
        # Check if within market hours
        if start_time <= current_time_only <= stop_time:
            return True
        else:
            return False
            
    except Exception as e:
        log(f"⚠️ Error checking market hours: {e}. Running anyway.")
        return True


def bring_window_to_front(window_title_keyword):
    """Find and bring a window to foreground by title keyword."""
    if not WIN32_AVAILABLE:
        log("❌ win32gui not available")
        return False
    
    try:
        window_hwnd = None
        
        def enum_callback(hwnd, _):
            nonlocal window_hwnd
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if window_title_keyword.lower() in title.lower():
                    window_hwnd = hwnd
                    log(f"✅ Found window: {title}")
            return True
        
        win32gui.EnumWindows(enum_callback, None)
        
        if window_hwnd:
            # Maximize the window
            win32gui.ShowWindow(window_hwnd, win32con.SW_MAXIMIZE)
            time.sleep(0.5)
            
            # Try to set foreground, but continue even if it fails
            try:
                win32gui.SetForegroundWindow(window_hwnd)
            except:
                pass
            
            log(f"✅ Window maximized and brought to foreground")
            return True
        else:
            log(f"❌ Window with '{window_title_keyword}' not found")
            return False
            
    except Exception as e:
        log(f"⚠️  Error: {e}")
        return False


def process_window(window_title, tab_num, symbol, folder, screenshot_name, window_settle_delay, focus_click_delay, chart_load_delay):
    """Process a single TradingView window."""
    log(f"\n🎯 Tab {tab_num}: Bringing '{window_title}' window to foreground...")
    if not bring_window_to_front(window_title):
        log(f"❌ Window not found. Skipping tab {tab_num}.")
        return False
    
    # Wait for window to settle
    time.sleep(window_settle_delay)
    
    # Click to ensure focus
    pyautogui.click(1280, 800)
    time.sleep(focus_click_delay)
    
    # Type symbol directly
    log(f"⌨️  Typing: {symbol}")
    pyautogui.write(symbol.lower(), interval=0.1)
    
    # Press Enter
    log("✅ Pressing Enter...")
    pyautogui.press('enter')
    
    # Wait for chart to load
    log(f"⏳ Waiting {chart_load_delay} seconds for chart to load...")
    time.sleep(chart_load_delay)
    
    # Take screenshot
    log(f"📸 Taking screenshot for Tab {tab_num}...")
    filename = screenshot_name.format(symbol=symbol)
    filepath = os.path.join(folder, filename)
    
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    log(f"✅ Saved: {filepath}")
    return True


def process_symbolik(symbol, folder, symbolik_wait_delay, symbolik_window, screenshot_name):
    """Process symbolik.com navigation and screenshot."""
    
    log(f"\n🌐 Tab 5: Processing symbolik.com for {symbol}...")
    
    # Bring browser window to front
    if not bring_window_to_front(symbolik_window):
        log(f"  ⚠️  Please open the browser with '{symbolik_window}' in the title")
        return False
    
    # Wait for window to settle
    time.sleep(2)
    
    # Click in the center to focus
    log(f"  🖱️  Clicking to focus...")
    pyautogui.click(1280, 800)
    time.sleep(1)
    
    # Type the symbol with .bz suffix in the search/input field
    symbol_query = f"{symbol.lower()}.bz"
    log(f"  ⌨️  Typing symbol: {symbol_query}")
    pyautogui.write(symbol_query, interval=0.1)
    time.sleep(0.5)
    
    # Wait for dropdown to appear and select first item
    log(f"  ⬇️  Selecting from dropdown...")
    time.sleep(1)  # Wait for dropdown to appear
    pyautogui.press('down')  # Select first item in dropdown
    time.sleep(0.3)
    
    # Press Enter
    log(f"  ✅ Pressing Enter...")
    pyautogui.press('enter')
    
    # Wait for page to load
    log(f"⏳ Waiting {symbolik_wait_delay} seconds for page to load...")
    time.sleep(symbolik_wait_delay)
    
    # Take screenshot
    log(f"📸 Taking screenshot for Symbolik.com...")
    filename = screenshot_name.format(symbol=symbol)
    filepath = os.path.join(folder, filename)
    
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    log(f"✅ Saved: {filepath}")
    return True



def initialize_log():
    """Initialize/clear the log file at the start of each run."""
    try:
        # Get the directory where the script/executable is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            script_dir = os.path.dirname(os.path.abspath(__file__))
        
        log_file = os.path.join(script_dir, 'desktop_auto.log')
        
        # Clear the log file by opening in write mode
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("Desktop Auto - Log Started\n")
            f.write("=" * 50 + "\n")
    except Exception as e:
        print(f"Warning: Could not initialize log file: {e}")


def main():
    """Main function."""
    initialize_log()
    log("\n⏰ Starting in 3 seconds...")
    for i in range(3, 0, -1):
        log(f"   {i}...")
        time.sleep(1)
    
    try:
        # Get stock symbols from stock_symbols.txt file
        symbols = load_stock_symbols()
        
        # Get timing parameters from .env
        tradingview_enabled = os.getenv('TRADINGVIEW_ENABLED', 'True').lower() == 'true'
        tradingview_window1 = os.getenv('TRADINGVIEW_WINDOW1', 'trend analysis')
        tradingview_window2 = os.getenv('TRADINGVIEW_WINDOW2', 'Smoothed Heiken Ashi Candles')
        tradingview_window3 = os.getenv('TRADINGVIEW_WINDOW3', 'volume layout')
        tradingview_window4 = os.getenv('TRADINGVIEW_WINDOW4', 'volumeprofile')
        window_settle_delay = float(os.getenv('WINDOW_SETTLE_DELAY', '3.0'))
        focus_click_delay = float(os.getenv('FOCUS_CLICK_DELAY', '1.5'))
        chart_load_delay_tabs1_3 = float(os.getenv('CHART_LOAD_DELAY_TAB1_3', '5.0'))
        chart_load_delay_tab4 = float(os.getenv('CHART_LOAD_DELAY_TAB4', '15.0'))
        screenshot_dir = os.getenv('SCREENSHOT_DIR', 'screenshots')
        screenshot_name_tab1 = os.getenv('SCREENSHOT_NAME_TAB1', '{symbol}_tab1.png')
        screenshot_name_tab2 = os.getenv('SCREENSHOT_NAME_TAB2', '{symbol}_tab2.png')
        screenshot_name_tab3 = os.getenv('SCREENSHOT_NAME_TAB3', '{symbol}_tab3.png')
        screenshot_name_tab4 = os.getenv('SCREENSHOT_NAME_TAB4', '{symbol}_tab4.png')
        screenshot_name_symbolik = os.getenv('SCREENSHOT_NAME_SYMBOLIK', '{symbol}_symbolik.png')
        symbolik_enabled = os.getenv('SYMBOLIK_ENABLED', 'True').lower() == 'true'
        symbolik_window = os.getenv('SYMBOLIK_WINDOW', 'workspace')
        symbolik_wait_delay = float(os.getenv('SYMBOLIK_WAIT_DELAY', '5.0'))
        
        log(f"\n📊 Processing {len(symbols)} symbols: {', '.join(symbols)}")
        
        for symbol in symbols:
            log(f"\n{'='*60}")
            log(f"Processing symbol: {symbol}")
            log(f"{'='*60}")
            
            # Create screenshot folder
            folder = f"{screenshot_dir}/{symbol}"
            os.makedirs(folder, exist_ok=True)
            
            # Process TradingView windows if enabled
            if tradingview_enabled:
                # Tab 1: Trend analysis window - Type symbol
                log(f"\n🎯 Tab 1: Bringing '{tradingview_window1}' window to foreground...")
                if not bring_window_to_front(tradingview_window1):
                    log("❌ Failed. Please make sure TradingView is open.")
                    return
                
                # Wait for window to settle
                time.sleep(window_settle_delay)
                
                # Click center to ensure window is fully focused
                pyautogui.click(1280, 800)
                time.sleep(focus_click_delay)
                
                # Type symbol directly
                log(f"⌨️  Typing: {symbol}")
                pyautogui.write(symbol.lower(), interval=0.1)
                
                # Press Enter
                log("✅ Pressing Enter...")
                pyautogui.press('enter')
                
                # Wait for chart to load
                log(f"⏳ Waiting {chart_load_delay_tabs1_3} seconds for chart to load...")
                time.sleep(chart_load_delay_tabs1_3)
                
                # Take screenshot for tab 1
                log(f"📸 Taking screenshot for Tab 1...")
                filename = screenshot_name_tab1.format(symbol=symbol)
                filepath = os.path.join(folder, filename)
                
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
                log(f"✅ Saved: {filepath}")
                
                # Process remaining windows
                process_window(tradingview_window2, 2, symbol, folder, screenshot_name_tab2,
                              window_settle_delay, focus_click_delay, chart_load_delay_tabs1_3)
                process_window(tradingview_window3, 3, symbol, folder, screenshot_name_tab3,
                              window_settle_delay, focus_click_delay, chart_load_delay_tabs1_3)
                process_window(tradingview_window4, 4, symbol, folder, screenshot_name_tab4,
                              window_settle_delay, focus_click_delay, chart_load_delay_tab4)
            
            # Process symbolik.com if enabled
            if symbolik_enabled:
                process_symbolik(symbol, folder, symbolik_wait_delay, symbolik_window, screenshot_name_symbolik)
            
            # Perform AI analysis if enabled
            perplexity_enabled = os.getenv('PERPLEXITY_ENABLED', 'False').lower() == 'true'
            if perplexity_enabled and PERPLEXITY_AVAILABLE:
                try:
                    log(f"\n🤖 Starting Perplexity AI analysis for {symbol}...")
                    
                    # Build screenshot data dictionary
                    screenshot_data = {}
                    
                    if tradingview_enabled:
                        # Map TradingView windows to analysis types
                        screenshot_data['trend_analysis'] = os.path.join(folder, screenshot_name_tab1.format(symbol=symbol))
                        screenshot_data['heiken_ashi'] = os.path.join(folder, screenshot_name_tab2.format(symbol=symbol))
                        screenshot_data['volume_layout'] = os.path.join(folder, screenshot_name_tab3.format(symbol=symbol))
                        screenshot_data['volumeprofile'] = os.path.join(folder, screenshot_name_tab4.format(symbol=symbol))
                    
                    if symbolik_enabled:
                        screenshot_data['workspace'] = os.path.join(folder, screenshot_name_symbolik.format(symbol=symbol))
                    
                    # Initialize analyzer
                    analyzer = PerplexityAnalyzer()
                    
                    # Analyze with trend alerts
                    analysis, change_analysis = analyzer.analyze_with_trend_alerts(
                        screenshot_data, folder, symbol
                    )
                    
                    # Save analysis report if successful
                    if analysis:
                        analyzer.save_combined_analysis_report(
                            screenshot_data, analysis, folder, change_analysis
                        )
                    
                except Exception as e:
                    log(f"   ⚠️ Analysis failed: {e}")
            elif perplexity_enabled and not PERPLEXITY_AVAILABLE:
                log(f"\n⚠️ Perplexity analysis is enabled but module not available. Install: pip install openai")
            
            log(f"\n✅ Completed processing {symbol}!")
        
        log("\n✅ DONE! All symbols and windows processed.")
        
    except KeyboardInterrupt:
        log("\n👋 Cancelled by user")
    except Exception as e:
        log(f"\n❌ Error: {e}")


def run_scheduled():
    """Run the automation on a schedule during market hours."""
    schedule_enabled = os.getenv('SCHEDULE_ENABLED', 'False').lower() == 'true'
    
    if not schedule_enabled:
        log("📍 Running once (SCHEDULE_ENABLED=False)")
        main()
        return
    
    # Get scheduling parameters
    interval_seconds = int(os.getenv('CAPTURE_INTERVAL_SECONDS', '3600'))
    timezone_str = os.getenv('CAPTURE_TIMEZONE', 'US/Eastern')
    start_time_str = os.getenv('CAPTURE_START_TIME', '09:30')
    stop_time_str = os.getenv('CAPTURE_STOP_TIME', '16:00')
    
    log(f"\n{'='*60}")
    log(f"🕐 SCHEDULED MODE ENABLED")
    log(f"{'='*60}")
    log(f"Market Hours: {start_time_str} - {stop_time_str} {timezone_str}")
    log(f"Interval: {interval_seconds}s ({interval_seconds//60} minutes)")
    log(f"{'='*60}\n")
    
    run_count = 0
    
    while True:
        try:
            if is_within_market_hours():
                run_count += 1
                current_time = datetime.now()
                if PYTZ_AVAILABLE:
                    tz = pytz.timezone(timezone_str)
                    current_time = datetime.now(tz)
                
                log(f"\n{'='*60}")
                log(f"🚀 RUN #{run_count} - {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                log(f"{'='*60}")
                
                main()
                
                log(f"\n⏰ Next run in {interval_seconds//60} minutes...")
                log(f"   Sleeping until {(datetime.now() + timedelta(seconds=interval_seconds)).strftime('%H:%M:%S')}")
                time.sleep(interval_seconds)
            else:
                current_time = datetime.now()
                if PYTZ_AVAILABLE:
                    tz = pytz.timezone(timezone_str)
                    current_time = datetime.now(tz)
                
                log(f"\n⏸️  Outside market hours - {current_time.strftime('%H:%M:%S %Z')}")
                log(f"   Market hours: {start_time_str} - {stop_time_str}")
                log(f"   Checking again in 5 minutes...")
                time.sleep(300)  # Check every 5 minutes when outside market hours
                
        except KeyboardInterrupt:
            log(f"\n\n👋 Stopped by user after {run_count} runs")
            break
        except Exception as e:
            log(f"\n❌ Error in scheduled run: {e}")
            log(f"   Waiting {interval_seconds//60} minutes before retry...")
            time.sleep(interval_seconds)


if __name__ == "__main__":
    from datetime import timedelta
    run_scheduled()

