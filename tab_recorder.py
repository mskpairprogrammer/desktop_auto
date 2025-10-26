#!/usr/bin/env python3
"""
Record tab switching actions in TradingView
"""
from pynput import mouse, keyboard
import json
import time

actions = []
start_time = time.time()

def on_click(x, y, button, pressed):
    """Record mouse clicks."""
    if pressed:
        timestamp = time.time() - start_time
        actions.append({
            'type': 'click',
            'x': x,
            'y': y,
            'timestamp': timestamp
        })
        print(f"Click at ({x}, {y})")

def on_press(key):
    """Record key presses."""
    timestamp = time.time() - start_time
    
    try:
        # Regular key
        actions.append({
            'type': 'key',
            'key': key.char,
            'timestamp': timestamp
        })
        print(f"Key: {key.char}")
    except AttributeError:
        # Special key
        key_name = str(key).replace('Key.', '')
        actions.append({
            'type': 'key',
            'key': key_name,
            'timestamp': timestamp
        })
        print(f"Key: {key_name}")
        
        # Stop recording on ESC
        if key == keyboard.Key.esc:
            print("\n✅ Recording stopped")
            return False

def main():
    print("="*60)
    print("TAB SWITCHING RECORDER")
    print("="*60)
    print("\nInstructions:")
    print("1. Switch to TradingView window")
    print("2. Navigate through all 4 tabs (however you normally do it)")
    print("3. Press ESC when done")
    print("\n⏰ Starting in 3 seconds...\n")
    
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🔴 RECORDING... (Press ESC to stop)\n")
    
    # Start listeners
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press)
    
    mouse_listener.start()
    keyboard_listener.start()
    
    keyboard_listener.join()
    mouse_listener.stop()
    
    # Save actions
    with open('tab_actions.json', 'w') as f:
        json.dump(actions, f, indent=2)
    
    print(f"\n📁 Saved {len(actions)} actions to tab_actions.json")

if __name__ == "__main__":
    main()
