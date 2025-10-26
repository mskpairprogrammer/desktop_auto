#!/usr/bin/env python3
"""
Record how you switch from tab 1 to tab 2
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
    print("TAB SWITCH RECORDER")
    print("="*60)
    print("\nInstructions:")
    print("1. TradingView should be on Tab 1")
    print("2. Switch to Tab 2 (using whatever method works)")
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
    with open('tab_switch_actions.json', 'w') as f:
        json.dump(actions, f, indent=2)
    
    print(f"\n📁 Saved {len(actions)} actions to tab_switch_actions.json")
    
    # Analyze what was done
    print("\n📊 Analysis:")
    clicks = [a for a in actions if a['type'] == 'click']
    keys = [a for a in actions if a['type'] == 'key']
    
    if clicks:
        print(f"   Clicks: {len(clicks)}")
        for click in clicks:
            print(f"      - ({click['x']}, {click['y']})")
    
    if keys:
        print(f"   Keys pressed: {[k['key'] for k in keys]}")

if __name__ == "__main__":
    main()
