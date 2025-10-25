# Desktop Auto - TradingView Automation# Desktop Auto Project



A Python-based desktop automation tool for capturing screenshots from multiple TradingView chart windows.A Python project for desktop automation tasks.



## Features## Getting Started



- Automatically switches between 4 separate TradingView windows### Prerequisites

- Updates symbol on the first chart (Trend analysis)

- Captures screenshots from all 4 chart layouts:- Python 3.8 or higher

  1. Trend analysis- VS Code with Python extension

  2. Smoothed Heiken Ashi Candles

  3. Volume layout### Installation

  4. Volumeprofile

- Saves screenshots without timestamps (overwrites previous versions)1. Clone or download this project

- Uses Windows API for reliable window management2. Open the project in VS Code

3. Install dependencies:

## Prerequisites   ```bash

   pip install -r requirements.txt

- Windows OS (uses win32gui for window management)   ```

- Python 3.8+4. Copy the environment template and configure:

- TradingView account with 4 separate chart windows open   ```bash

   copy .env.example .env

## Setup   ```

   Then edit `.env` with your specific settings.

1. Clone the repository:

   ```bash### Configuration

   git clone https://github.com/mskpairprogrammer/desktop_auto.git

   cd desktop_autoThe project uses environment variables for configuration. Key settings in `.env`:

   ```

- `APP_NAME`: Application name (default: "Desktop Auto")

2. Create a virtual environment:- `DEBUG`: Enable debug mode (true/false)

   ```bash- `AUTOMATION_DELAY`: Delay between automation actions in seconds

   python -m venv .venv- `SCREENSHOT_DIR`: Directory for screenshot storage

   ```- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)



3. Activate the virtual environment:## Usage Examples

   ```bash

   .venv\Scripts\activate### Simple Usage (Recommended)

   ``````bash

# Run the simple automation

4. Install dependencies:python main.py

   ```bash```

   pip install -r requirements.txt

   ```### What the simple automation does:

1. 🔄 **Alt+Tab to TradingView** (brings app to foreground)

5. Create a `.env` file based on `.env.example`:2. �️ **Click center of screen** (activates chart area)

   ```bash3. ⌨️ **Type "QBTS"** (enters the stock symbol)

   copy .env.example .env4. ✅ **Press Enter** (confirms the symbol)

   ```5. 📸 **Take screenshot** (captures the chart)

6. 💾 **Save to folder**: `screenshots/QBTS/QBTS_timestamp.png`

6. Edit `.env` and set your default stock symbol:

   ```### Alternative Scripts

   DEFAULT_SYMBOL=SNAP```bash

   ```# Manual control version (you focus TradingView yourself)

python manual_automator.py

## TradingView Setup

# Test different click positions

Open 4 separate TradingView windows with these chart layouts:python manual_automator.py

1. **Trend analysis** - Your main trend analysis chart# Choose option 2 for position testing

2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view```

3. **Volume layout** - Volume-focused chart

4. **Volumeprofile** - Volume profile analysis### TradingView Automation Features



The window titles must contain these keywords for the automation to find them.The project includes automated TradingView desktop app interaction:



## Usage1. **Brings TradingView to foreground** (if possible)

2. **Changes stock symbol** using Ctrl+K shortcut

Run the automation script:3. **Takes screenshot** of the current chart

```bash4. **Saves screenshot** in organized folders: `screenshots/SYMBOL/`

python main.py

```### Prerequisites for TradingView Automation



The script will:- TradingView desktop application must be running

1. Wait 3 seconds before starting- The app can be in the background (Alt+Tab will bring it forward)

2. Switch to the "Trend analysis" window and type the symbol (from `.env`)- Chart should accept direct typing (most TradingView setups do)

3. Wait 7 seconds for the chart to load- Simple and reliable - no complex shortcuts needed

4. Take a screenshot and save as `screenshots/SYMBOL/SYMBOL_tab1.png`

5. Switch to each of the other 3 windows and capture screenshots### Safety Features

6. Save all screenshots without timestamps (overwrites previous runs)

- **Failsafe**: Move mouse to top-left corner to stop automation

## Screenshots Location- **Simple workflow**: Alt+Tab → Click → Type → Enter → Screenshot

- **Error handling**: Clear error messages and graceful failures

Screenshots are saved in `screenshots/SYMBOL/` where SYMBOL is the stock symbol from your `.env` file.

## Project Structure

Example:

- `screenshots/SNAP/SNAP_tab1.png````

- `screenshots/SNAP/SNAP_tab2.png`desktop_auto/

- `screenshots/SNAP/SNAP_tab3.png`├── main.py              # Main application entry point

- `screenshots/SNAP/SNAP_tab4.png`├── requirements.txt     # Python dependencies

├── README.md           # This file

## Utilities└── .github/

    └── copilot-instructions.md  # Copilot configuration

- `list_windows.py` - List all TradingView windows to verify your setup```



## Troubleshooting## Development



**Windows not found:**This project is set up for development in VS Code with Python support. The recommended extensions will be suggested when you open the project.

- Ensure all 4 TradingView windows are open

- Check that window titles contain the expected keywords## License

- Run `python list_windows.py` to see all available windows

This project is for personal use.
**Screenshots are blank or wrong timing:**
- Adjust wait times in `main.py` if charts load slower
- Increase `time.sleep()` values after window switches

**Symbol not updating:**
- Verify the click position (1674, 1568) matches your screen resolution
- Adjust coordinates in `main.py` for your setup

## Project Structure

- `main.py` - Main automation script
- `list_windows.py` - Utility to list TradingView windows
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment configuration
- `.gitignore` - Git ignore rules

## License

MIT License - feel free to use and modify for your needs.
