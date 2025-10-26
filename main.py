#!/usr/bin/env python3
"""
Desktop Auto Project - TradingView Automation for 4 Separate Windows
"""
import pyautogui
import time
import os
from datetime import datetime
from dotenv import load_dotenv

try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

# Load environment variables
load_dotenv()


def bring_window_to_front(window_title_keyword):
    """Find and bring a window to foreground by title keyword."""
    if not WIN32_AVAILABLE:
        print("❌ win32gui not available")
        return False
    
    try:
        window_hwnd = None
        
        def enum_callback(hwnd, _):
            nonlocal window_hwnd
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if window_title_keyword.lower() in title.lower():
                    window_hwnd = hwnd
                    print(f"✅ Found window: {title}")
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
            
            print(f"✅ Window maximized and brought to foreground")
            return True
        else:
            print(f"❌ Window with '{window_title_keyword}' not found")
            return False
            
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return False


def process_window(window_title, tab_num, symbol, folder, window_settle_delay, focus_click_delay, chart_load_delay):
    """Process a single TradingView window."""
    print(f"\n🎯 Tab {tab_num}: Bringing '{window_title}' window to foreground...")
    if not bring_window_to_front(window_title):
        print(f"❌ Window not found. Skipping tab {tab_num}.")
        return False
    
    # Wait for window to settle
    time.sleep(window_settle_delay)
    
    # Click to ensure focus
    pyautogui.click(1280, 800)
    time.sleep(focus_click_delay)
    
    # Type symbol directly
    print(f"⌨️  Typing: {symbol}")
    pyautogui.write(symbol.lower(), interval=0.1)
    
    # Press Enter
    print("✅ Pressing Enter...")
    pyautogui.press('enter')
    
    # Wait for chart to load
    print(f"⏳ Waiting {chart_load_delay} seconds for chart to load...")
    time.sleep(chart_load_delay)
    
    # Take screenshot
    print(f"📸 Taking screenshot for Tab {tab_num}...")
    filename = f"{symbol}_tab{tab_num}.png"
    filepath = os.path.join(folder, filename)
    
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"✅ Saved: {filepath}")
    return True


def process_symbolik(symbol, folder, symbolik_wait_delay):
    """Process symbolik.com navigation and screenshot."""
    
    print(f"\n🌐 Tab 5: Processing symbolik.com for {symbol}...")
    
    # Bring browser window to front
    if not bring_window_to_front("workspace"):
        print("  ⚠️  Please open the browser with 'workspace' in the title")
        return False
    
    # Wait for window to settle
    time.sleep(2)
    
    # Click in the center to focus
    print(f"  🖱️  Clicking to focus...")
    pyautogui.click(1280, 800)
    time.sleep(1)
    
    # Type the symbol with .bz suffix in the search/input field
    symbol_query = f"{symbol.lower()}.bz"
    print(f"  ⌨️  Typing symbol: {symbol_query}")
    pyautogui.write(symbol_query, interval=0.1)
    time.sleep(0.5)
    
    # Wait for dropdown to appear and select first item
    print(f"  ⬇️  Selecting from dropdown...")
    time.sleep(1)  # Wait for dropdown to appear
    pyautogui.press('down')  # Select first item in dropdown
    time.sleep(0.3)
    
    # Press Enter
    print(f"  ✅ Pressing Enter...")
    pyautogui.press('enter')
    
    # Wait for page to load
    print(f"⏳ Waiting {symbolik_wait_delay} seconds for page to load...")
    time.sleep(symbolik_wait_delay)
    
    # Take screenshot
    print(f"📸 Taking screenshot for Symbolik.com...")
    filename = f"{symbol}_symbolik.png"
    filepath = os.path.join(folder, filename)
    
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"✅ Saved: {filepath}")
    return True



def main():
    """Main function."""
    print("\n⏰ Starting in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    try:
        # Get stock symbols from .env
        symbols_str = os.getenv('STOCK_SYMBOLS', 'QBTS')
        symbols = [s.strip() for s in symbols_str.split(',')]
        
        # Get timing parameters from .env
        tradingview_enabled = os.getenv('TRADINGVIEW_ENABLED', 'True').lower() == 'true'
        window_settle_delay = float(os.getenv('WINDOW_SETTLE_DELAY', '3.0'))
        focus_click_delay = float(os.getenv('FOCUS_CLICK_DELAY', '1.5'))
        chart_load_delay_tabs1_3 = float(os.getenv('CHART_LOAD_DELAY_TAB1_3', '5.0'))
        chart_load_delay_tab4 = float(os.getenv('CHART_LOAD_DELAY_TAB4', '15.0'))
        symbolik_enabled = os.getenv('SYMBOLIK_ENABLED', 'True').lower() == 'true'
        symbolik_wait_delay = float(os.getenv('SYMBOLIK_WAIT_DELAY', '5.0'))
        
        print(f"\n📊 Processing {len(symbols)} symbols: {', '.join(symbols)}")
        
        for symbol in symbols:
            print(f"\n{'='*60}")
            print(f"Processing symbol: {symbol}")
            print(f"{'='*60}")
            
            # Create screenshot folder
            folder = f"screenshots/{symbol}"
            os.makedirs(folder, exist_ok=True)
            
            # Process TradingView windows if enabled
            if tradingview_enabled:
                # Tab 1: Trend analysis window - Type symbol
                print("\n🎯 Tab 1: Bringing 'Trend analysis' window to foreground...")
                if not bring_window_to_front('trend analysis'):
                    print("❌ Failed. Please make sure TradingView is open.")
                    return
                
                # Wait for window to settle
                time.sleep(window_settle_delay)
                
                # Click center to ensure window is fully focused
                pyautogui.click(1280, 800)
                time.sleep(focus_click_delay)
                
                # Type symbol directly
                print(f"⌨️  Typing: {symbol}")
                pyautogui.write(symbol.lower(), interval=0.1)
                
                # Press Enter
                print("✅ Pressing Enter...")
                pyautogui.press('enter')
                
                # Wait for chart to load
                print(f"⏳ Waiting {chart_load_delay_tabs1_3} seconds for chart to load...")
                time.sleep(chart_load_delay_tabs1_3)
                
                # Take screenshot for tab 1
                print(f"📸 Taking screenshot for Tab 1...")
                filename = f"{symbol}_tab1.png"
                filepath = os.path.join(folder, filename)
                
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
                print(f"✅ Saved: {filepath}")
                
                # Process remaining windows
                process_window('Smoothed Heiken Ashi Candles', 2, symbol, folder, 
                              window_settle_delay, focus_click_delay, chart_load_delay_tabs1_3)
                process_window('volume layout', 3, symbol, folder,
                              window_settle_delay, focus_click_delay, chart_load_delay_tabs1_3)
                process_window('volumeprofile', 4, symbol, folder,
                              window_settle_delay, focus_click_delay, chart_load_delay_tab4)
            
            # Process symbolik.com if enabled
            if symbolik_enabled:
                process_symbolik(symbol, folder, symbolik_wait_delay)
            
            print(f"\n✅ Completed processing {symbol}!")
        
        print("\n✅ DONE! All symbols and windows processed.")
        
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
