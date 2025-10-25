#!/usr/bin/env python3
"""
Desktop Auto Project - TradingView Automation from Recorded Actions
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
                    return False
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


def main():
    """Main function."""
    print("\n⏰ Starting in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    try:
        # Tab 1: Trend analysis window
        print("\n🎯 Tab 1: Bringing 'Trend analysis' window to foreground...")
        if not bring_window_to_front('trend analysis'):
            print("❌ Failed. Please make sure TradingView is open.")
            return
        
        # Get symbol from .env
        symbol = os.getenv('DEFAULT_SYMBOL', 'SNAP')
        
        # Click on symbol search field (from your recording: 1674, 1568)
        print(f"\n🖱️  Clicking on symbol search field...")
        pyautogui.click(1674, 1568)
        time.sleep(0.5)
        
        # Type symbol
        print(f"⌨️  Typing: {symbol}")
        pyautogui.write(symbol.lower(), interval=0.1)
        
        # Press Enter
        print("✅ Pressing Enter...")
        pyautogui.press('enter')
        
        # Wait for chart to load
        print("⏳ Waiting 5 seconds for chart to load...")
        time.sleep(5)
        
        # Create screenshot folder
        folder = f"screenshots/{symbol}"
        os.makedirs(folder, exist_ok=True)
        
        # Take screenshot for tab 1
        print(f"📸 Taking screenshot for Tab 1...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_tab1_{timestamp}.png"
        filepath = os.path.join(folder, filename)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        print(f"✅ Saved: {filepath}")
        
        # Tab 2: Volumeprofile window
        print(f"\n🎯 Tab 2: Bringing 'Volumeprofile' window to foreground...")
        if not bring_window_to_front('volumeprofile'):
            print("❌ Volumeprofile window not found. Skipping tab 2.")
        else:
            # Wait for window to fully render
            print(f"⏳ Waiting for window to load...")
            time.sleep(2)
            
            # Click on center to ensure focus
            print(f"🖱️  Clicking to ensure focus...")
            pyautogui.click(1280, 800)
            time.sleep(1)
            
            # Take screenshot for tab 2
            print(f"📸 Taking screenshot for Tab 2...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_tab2_{timestamp}.png"
            filepath = os.path.join(folder, filename)
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            print(f"✅ Saved: {filepath}")
        
        # Navigate to 2nd tab by clicking on it
        print(f"\n� Clicking on tab 2 at (171, 470)...")
        pyautogui.click(171, 470)
        time.sleep(2)
        
        print("\n✅ DONE!")
        
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
