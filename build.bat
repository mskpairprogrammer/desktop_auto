@echo off
REM Build script for Desktop Auto executable

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable...
python build_executable.py

echo.
echo ========================================
echo Build complete!
echo Executable location: dist\DesktopAuto.exe
echo ========================================
echo.
echo IMPORTANT: Copy your .env file to the dist folder before running the executable
pause
