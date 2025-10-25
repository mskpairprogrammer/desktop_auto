#!/usr/bin/env python3
"""
Complete Screen Navigation Recorder
Records mouse movements, clicks, and keyboard actions
"""
from pynput import mouse, keyboard
import json
import time

actions = []
start_time = time.time()
last_mouse_pos = None

def on_move(x, y):
    """Record significant mouse movements."""
    global last_mouse_pos
    # Only record if moved significantly (more than 50 pixels)
    if last_mouse_pos is None or \
       abs(x - last_mouse_pos[0]) > 50 or \
       abs(y - last_mouse_pos[1]) > 50:
        timestamp = time.time() - start_time
        actions.append({
            'type': 'move',
            'x': x,
            'y': y,
            'timestamp': timestamp
        })
        last_mouse_pos = (x, y)
        print(f"Move to ({x}, {y})")

def on_click(x, y, button, pressed):
    """Record mouse clicks."""
    if pressed:
        timestamp = time.time() - start_time
        actions.append({
            'type': 'click',
            'x': x,
            'y': y,
            'button': str(button),
            'timestamp': timestamp
        })
        print(f"Click {button} at ({x}, {y})")

def on_scroll(x, y, dx, dy):
    """Record scroll events."""
    timestamp = time.time() - start_time
    actions.append({
        'type': 'scroll',
        'x': x,
        'y': y,
        'dx': dx,
        'dy': dy,
        'timestamp': timestamp
    })
    print(f"Scroll at ({x}, {y}): dx={dx}, dy={dy}")

def on_press(key):
    """Record key presses."""
    timestamp = time.time() - start_time
    
    try:
        # Regular key
        key_name = key.char
        actions.append({
            'type': 'key',
            'key': key_name,
            'timestamp': timestamp
        })
        print(f"Key: {key_name}")
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
    print("COMPLETE SCREEN NAVIGATION RECORDER")
    print("="*60)
    print("\nThis will record:")
    print("  • Mouse movements (significant changes)")
    print("  • Mouse clicks")
    print("  • Mouse scrolls")
    print("  • Keyboard input")
    print("\nInstructions:")
    print("1. Perform your complete workflow in TradingView")
    print("2. Press ESC when done")
    print("\n⏰ Starting in 5 seconds...\n")
    
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🔴 RECORDING... (Press ESC to stop)\n")
    
    # Start listeners
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )
    keyboard_listener = keyboard.Listener(on_press=on_press)
    
    mouse_listener.start()
    keyboard_listener.start()
    
    keyboard_listener.join()
    mouse_listener.stop()
    
    # Save actions
    filename = 'screen_navigation.json'
    with open(filename, 'w') as f:
        json.dump(actions, f, indent=2)
    
    print(f"\n📁 Saved {len(actions)} actions to {filename}")
    
    # Analyze what was recorded
    print("\n📊 Analysis:")
    moves = [a for a in actions if a['type'] == 'move']
    clicks = [a for a in actions if a['type'] == 'click']
    scrolls = [a for a in actions if a['type'] == 'scroll']
    keys = [a for a in actions if a['type'] == 'key']
    
    print(f"   Mouse movements: {len(moves)}")
    print(f"   Clicks: {len(clicks)}")
    if clicks:
        print("   Click positions:")
        for click in clicks[:10]:  # Show first 10
            print(f"      - ({click['x']}, {click['y']}) [{click['button']}]")
        if len(clicks) > 10:
            print(f"      ... and {len(clicks) - 10} more")
    
    print(f"   Scrolls: {len(scrolls)}")
    print(f"   Key presses: {len(keys)}")
    if keys:
        key_sequence = [k['key'] for k in keys[:20]]
        print(f"   First keys: {key_sequence}")

if __name__ == "__main__":
    main()
