"""
Build script to create executable for Desktop Auto
Run this with: python build_executable.py
"""
import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--name=DesktopAuto',
    f'--add-data={os.path.join(current_dir, ".env")};.',
    '--hidden-import=perplexity_analysis',
    '--hidden-import=pywin32',
    '--hidden-import=win32gui',
    '--hidden-import=win32con',
    '--hidden-import=openai',
    '--hidden-import=pytz',
    '--collect-all=openai',
    '--noconfirm',
    # Remove '--windowed' to keep console window for logs
])

print("\n✅ Executable created in 'dist' folder!")
print("📄 Don't forget to copy your .env file to the same directory as the .exe")
