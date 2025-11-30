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
    # Security: Do NOT bundle .env file - users must place it next to the executable
    '--hidden-import=trading_analysis',
    '--hidden-import=ai_analysis',
    '--hidden-import=config',
    '--hidden-import=utils',
    '--hidden-import=openai',
    '--hidden-import=anthropic',
    '--hidden-import=google.generativeai',
    '--hidden-import=pytz',
    '--hidden-import=PIL',
    '--collect-all=openai',
    '--noconfirm',
    # Remove '--windowed' to keep console window for logs
])

print("\n✅ Executable created in 'dist' folder!")
print("=" * 60)
print("⚠️  IMPORTANT SECURITY NOTICE:")
print("📄 You MUST copy your .env file to the same directory as the .exe")
print("   The .env file is NOT bundled for security reasons")
print("=" * 60)
