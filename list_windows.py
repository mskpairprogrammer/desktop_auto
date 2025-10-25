#!/usr/bin/env python3
"""
List all TradingView windows
"""
try:
    import win32gui
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

def list_tradingview_windows():
    """List all TradingView windows."""
    if not WIN32_AVAILABLE:
        print("❌ win32gui not available")
        return
    
    windows = []
    
    def enum_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if 'snap' in title.lower():
                windows.append(title)
        return True
    
    win32gui.EnumWindows(enum_callback, None)
    
    print(f"\n{'='*60}")
    print(f"FOUND {len(windows)} TRADINGVIEW WINDOWS:")
    print(f"{'='*60}\n")
    
    for i, title in enumerate(windows, 1):
        print(f"{i}. {title}")
        # Try to extract window identifier
        if '/' in title:
            parts = title.split('/')
            if len(parts) >= 2:
                identifier = parts[-1].strip()
                print(f"   → Identifier: '{identifier}'")
        print()

if __name__ == "__main__":
    list_tradingview_windows()
