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


def process_window(window_title, tab_num, symbol, folder, wait_time=5):
    """Process a single TradingView window."""
    print(f"\n🎯 Tab {tab_num}: Bringing '{window_title}' window to foreground...")
    if not bring_window_to_front(window_title):
        print(f"❌ Window not found. Skipping tab {tab_num}.")
        return False
    
    # Wait for window to settle
    time.sleep(3)
    
    # Click to ensure focus
    pyautogui.click(1280, 800)
    time.sleep(1.5)
    
    # Type symbol directly
    print(f"⌨️  Typing: {symbol}")
    pyautogui.write(symbol.lower(), interval=0.1)
    
    # Press Enter
    print("✅ Pressing Enter...")
    pyautogui.press('enter')
    
    # Wait for chart to load
    print(f"⏳ Waiting {wait_time} seconds for chart to load...")
    time.sleep(wait_time)
    
    # Take screenshot
    print(f"📸 Taking screenshot for Tab {tab_num}...")
    filename = f"{symbol}_tab{tab_num}.png"
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
        # Get symbol from .env
        symbol = os.getenv('DEFAULT_SYMBOL', 'SNAP')
        
        # Create screenshot folder
        folder = f"screenshots/{symbol}"
        os.makedirs(folder, exist_ok=True)
        
        # Tab 1: Trend analysis window - Type symbol
        print("\n🎯 Tab 1: Bringing 'Trend analysis' window to foreground...")
        if not bring_window_to_front('trend analysis'):
            print("❌ Failed. Please make sure TradingView is open.")
            return
        
        # Wait for window to settle
        time.sleep(3)
        
        # Click center to ensure window is fully focused
        pyautogui.click(1280, 800)
        time.sleep(1)
        
        # Type symbol directly
        print(f"⌨️  Typing: {symbol}")
        pyautogui.write(symbol.lower(), interval=0.1)
        
        # Press Enter
        print("✅ Pressing Enter...")
        pyautogui.press('enter')
        
        # Wait for chart to load
        print("⏳ Waiting 5 seconds for chart to load...")
        time.sleep(5)
        
        # Take screenshot for tab 1
        print(f"📸 Taking screenshot for Tab 1...")
        filename = f"{symbol}_tab1.png"
        filepath = os.path.join(folder, filename)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        print(f"✅ Saved: {filepath}")
        
        # Process remaining windows
        process_window('Smoothed Heiken Ashi Candles', 2, symbol, folder)
        process_window('volume layout', 3, symbol, folder)
        process_window('volumeprofile', 4, symbol, folder, wait_time=15)
        
        print("\n✅ DONE! All 4 windows processed.")
        
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
