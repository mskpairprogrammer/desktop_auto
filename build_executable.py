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
    # Add local modules as data files so they can be found
    f'--add-data={os.path.join(current_dir, "config.py")};.',
    f'--add-data={os.path.join(current_dir, "utils.py")};.',
    f'--add-data={os.path.join(current_dir, "ai_analysis.py")};.',
    f'--add-data={os.path.join(current_dir, "trading_analysis.py")};.',
    # Hidden imports for local and external modules
    '--hidden-import=trading_analysis',
    '--hidden-import=ai_analysis',
    '--hidden-import=config',
    '--hidden-import=utils',
    '--hidden-import=openai',
    '--hidden-import=anthropic',
    '--hidden-import=google.generativeai',
    '--hidden-import=pytz',
    '--hidden-import=PIL',
    '--hidden-import=dotenv',
    '--collect-all=openai',
    '--noconfirm',
    # Remove '--windowed' to keep console window for logs
])

print("\n✅ Executable created in 'dist' folder!")
print("=" * 60)
print("The executable will use the .env file from the project root:")
print(f"   {os.path.join(current_dir, '.env')}")
print("No need to copy .env - it reads from the project folder.")
print("=" * 60)
