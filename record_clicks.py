#!/usr/bin/env python3
"""
Mouse Click Recorder - Capture mouse click coordinates
Press ESC to stop recording
"""
import pyautogui
import time
from pynput import mouse, keyboard
import sys

class ClickRecorder:
    def __init__(self):
        self.clicks = []
        self.running = True
        print("Mouse Click Recorder Started!")
        print("Instructions:")
        print("- Click anywhere to record coordinates")
        print("- Press ESC to stop recording")
        print("- Coordinates will be displayed immediately")
        print("-" * 50)
        
    def on_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            print(f"Click recorded: X={x}, Y={y}")
            self.clicks.append((x, y))
            
    def on_key_press(self, key):
        try:
            if key == keyboard.Key.esc:
                print("\n" + "="*50)
                print("Recording stopped!")
                print(f"Total clicks recorded: {len(self.clicks)}")
                print("\nCoordinates summary:")
                for i, (x, y) in enumerate(self.clicks, 1):
                    print(f"  Click {i}: X={x}, Y={y}")
                
                if self.clicks:
                    print(f"\nMost recent coordinates: ({self.clicks[-1][0]}, {self.clicks[-1][1]})")
                    print("Copy this for your code:")
                    print(f"pyautogui.click({self.clicks[-1][0]}, {self.clicks[-1][1]})")
                
                self.running = False
                return False
        except AttributeError:
            pass
            
    def start_recording(self):
        # Start mouse listener
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()
        
        # Start keyboard listener
        keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        keyboard_listener.start()
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nRecording interrupted")
        
        mouse_listener.stop()
        keyboard_listener.stop()

if __name__ == "__main__":
    try:
        recorder = ClickRecorder()
        recorder.start_recording()
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Install with: pip install pynput")
    except Exception as e:
        print(f"Error: {e}")