#!/usr/bin/env python3
"""
Test Symbolik.com automation step
"""
import pyautogui
import time
import os
import win32gui
import win32con

def bring_window_to_front(window_title_keyword):
    """Bring a window containing the keyword to the foreground."""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if window_title_keyword.lower() in title.lower():
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    if windows:
        hwnd, title = windows[0]
        print(f"  🔍 Found window: {title}")
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(hwnd)
        return True
    else:
        print(f"  ❌ No window found with '{window_title_keyword}' in title")
        return False

def process_symbolik(symbol, folder, symbolik_wait_delay):
    """Process symbolik.com navigation and screenshot."""
    
    print(f"\n🌐 Processing symbolik.com for {symbol}...")
    
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


if __name__ == "__main__":
    print("\n⏰ Starting in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    # Test with TSLA
    test_symbol = "TSLA"
    test_folder = f"screenshots/{test_symbol}"
    os.makedirs(test_folder, exist_ok=True)
    
    try:
        process_symbolik(test_symbol, test_folder, 5.0)
        print("\n✅ Test completed!")
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
