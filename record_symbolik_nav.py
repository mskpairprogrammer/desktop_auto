#!/usr/bin/env python3
"""
Symbolik Website Navigation Recorder
Records mouse and keyboard actions for navigating symbolik.com
"""
import json
import time
from pynput import mouse, keyboard

actions = []
start_time = time.time()
recording = True

print("\n🎬 Symbolik.com Navigation Recorder")
print("=" * 60)
print("Instructions:")
print("1. Open your browser and go to symbolik.com")
print("2. Press SPACE to start recording")
print("3. Perform your navigation steps to search for a stock symbol")
print("4. Press ESC to stop recording")
print("=" * 60)
print("\nWaiting for SPACE to start recording...")

recording_started = False

def on_click(x, y, button, pressed):
    """Record mouse clicks"""
    if recording_started and pressed:
        elapsed = time.time() - start_time
        action = {
            'type': 'click',
            'x': x,
            'y': y,
            'button': str(button),
            'time': elapsed
        }
        actions.append(action)
        print(f"  🖱️  Click at ({x}, {y}) - {elapsed:.2f}s")

def on_type(key):
    """Record keyboard input"""
    global recording_started, recording
    
    try:
        # Start recording on SPACE
        if not recording_started and key == keyboard.Key.space:
            recording_started = True
            print("\n✅ Recording started! Perform your navigation steps...")
            print("   (Press ESC to stop)\n")
            return
        
        # Stop recording on ESC
        if key == keyboard.Key.esc:
            recording = False
            return False
        
        if recording_started:
            elapsed = time.time() - start_time
            
            # Handle special keys
            if hasattr(key, 'char') and key.char:
                action = {
                    'type': 'key',
                    'key': key.char,
                    'time': elapsed
                }
                actions.append(action)
                print(f"  ⌨️  Typed: {key.char} - {elapsed:.2f}s")
            elif key == keyboard.Key.enter:
                action = {
                    'type': 'key',
                    'key': 'enter',
                    'time': elapsed
                }
                actions.append(action)
                print(f"  ⌨️  Pressed: Enter - {elapsed:.2f}s")
            elif key == keyboard.Key.tab:
                action = {
                    'type': 'key',
                    'key': 'tab',
                    'time': elapsed
                }
                actions.append(action)
                print(f"  ⌨️  Pressed: Tab - {elapsed:.2f}s")
    except AttributeError:
        pass

# Set up listeners
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_type)

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()

# Save recorded actions
if actions:
    with open('symbolik_navigation.json', 'w') as f:
        json.dump(actions, f, indent=2)
    
    print(f"\n✅ Recording stopped!")
    print(f"📝 Saved {len(actions)} actions to symbolik_navigation.json")
    print("\nRecorded actions:")
    for i, action in enumerate(actions, 1):
        if action['type'] == 'click':
            print(f"  {i}. Click at ({action['x']}, {action['y']}) at {action['time']:.2f}s")
        else:
            print(f"  {i}. Type '{action['key']}' at {action['time']:.2f}s")
else:
    print("\n❌ No actions recorded")

mouse_listener.stop()
