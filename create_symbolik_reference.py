import pyautogui
import os
import time

def main():
    print("\nSymbolik Reference Image Creator")
    symbol = input("Enter the symbol (e.g., TSLA): ").strip().upper()
    if not symbol:
        print("No symbol entered. Exiting.")
        return
    print("You will select a region of the screen to use as the reference image for symbol:", symbol)
    print("Move your mouse to the top-left corner of the region and press Enter...")
    input()
    x1, y1 = pyautogui.position()
    print(f"Top-left at ({x1}, {y1})")
    print("Now move your mouse to the bottom-right corner and press Enter...")
    input()
    x2, y2 = pyautogui.position()
    print(f"Bottom-right at ({x2}, {y2})")
    left, top = min(x1, x2), min(y1, y2)
    width, height = abs(x2 - x1), abs(y2 - y1)
    print(f"Capturing region: left={left}, top={top}, width={width}, height={height}")
    time.sleep(0.5)
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    out_dir = os.path.join("screenshots")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"symbolik_ref_{symbol}.png")
    screenshot.save(out_path)
    print(f"Reference image saved to {out_path}")

if __name__ == "__main__":
    main()