# Desktop Auto - TradingView Automation# Desktop Auto - TradingView Automation# Desktop Auto Project



A Python-based desktop automation tool for capturing screenshots from multiple TradingView chart windows across multiple stock symbols.



## FeaturesA Python-based desktop automation tool for capturing screenshots from multiple TradingView chart windows.A Python project for desktop automation tasks.



- Automatically switches between 4 separate TradingView windows

- Processes multiple stock symbols from a configurable list

- Types each symbol in all 4 chart layouts## Features## Getting Started

- Captures screenshots from all chart layouts:

  1. Trend analysis

  2. Smoothed Heiken Ashi Candles

  3. Volume layout- Automatically switches between 4 separate TradingView windows### Prerequisites

  4. Volumeprofile (with extended 15s load time)

- Organizes screenshots by symbol in separate folders- Updates symbol on the first chart (Trend analysis)

- Uses Windows API for reliable window management

- Captures screenshots from all 4 chart layouts:- Python 3.8 or higher

## Prerequisites

  1. Trend analysis- VS Code with Python extension

- Windows OS (uses win32gui for window management)

- Python 3.8+  2. Smoothed Heiken Ashi Candles

- TradingView account with 4 separate chart windows open

  3. Volume layout### Installation

## Setup

  4. Volumeprofile

1. Clone the repository:

   ```bash- Saves screenshots without timestamps (overwrites previous versions)1. Clone or download this project

   git clone https://github.com/mskpairprogrammer/desktop_auto.git

   cd desktop_auto- Uses Windows API for reliable window management2. Open the project in VS Code

   ```

3. Install dependencies:

2. Create a virtual environment:

   ```bash## Prerequisites   ```bash

   python -m venv .venv

   ```   pip install -r requirements.txt



3. Activate the virtual environment:- Windows OS (uses win32gui for window management)   ```

   ```bash

   .venv\Scripts\activate- Python 3.8+4. Copy the environment template and configure:

   ```

- TradingView account with 4 separate chart windows open   ```bash

4. Install dependencies:

   ```bash   copy .env.example .env

   pip install -r requirements.txt

   ```## Setup   ```



5. Create a `.env` file based on `.env.example`:   Then edit `.env` with your specific settings.

   ```bash

   copy .env.example .env1. Clone the repository:

   ```

   ```bash### Configuration

6. Edit `.env` and set your stock symbols:

   ```   git clone https://github.com/mskpairprogrammer/desktop_auto.git

   STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL

   ```   cd desktop_autoThe project uses environment variables for configuration. Key settings in `.env`:

   You can add or remove symbols as needed, separated by commas.

   ```

## TradingView Setup

- `APP_NAME`: Application name (default: "Desktop Auto")

Open 4 separate TradingView windows with these chart layouts:

1. **Trend analysis** - Your main trend analysis chart2. Create a virtual environment:- `DEBUG`: Enable debug mode (true/false)

2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view

3. **Volume layout** - Volume-focused chart   ```bash- `AUTOMATION_DELAY`: Delay between automation actions in seconds

4. **Volumeprofile** - Volume profile analysis

   python -m venv .venv- `SCREENSHOT_DIR`: Directory for screenshot storage

The window titles must contain these keywords for the automation to find them.

   ```- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

## Usage



Run the automation script:

```bash3. Activate the virtual environment:## Usage Examples

python main.py

```   ```bash



The script will:   .venv\Scripts\activate### Simple Usage (Recommended)

1. Wait 3 seconds before starting

2. For each symbol in `STOCK_SYMBOLS`:   ``````bash

   - Switch to each of the 4 windows

   - Click center of screen for focus# Run the simple automation

   - Type the symbol

   - Press Enter4. Install dependencies:python main.py

   - Wait for chart to load (5s for Tabs 1-3, 15s for Tab 4)

   - Take screenshot and save as `screenshots/SYMBOL/SYMBOL_tab#.png`   ```bash```

3. Process all symbols sequentially

   pip install -r requirements.txt

## Screenshots Location

   ```### What the simple automation does:

Screenshots are organized by symbol in separate folders under `screenshots/`:

1. 🔄 **Alt+Tab to TradingView** (brings app to foreground)

Example with `STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL`:

```5. Create a `.env` file based on `.env.example`:2. �️ **Click center of screen** (activates chart area)

screenshots/

├── QBTS/   ```bash3. ⌨️ **Type "QBTS"** (enters the stock symbol)

│   ├── QBTS_tab1.png

│   ├── QBTS_tab2.png   copy .env.example .env4. ✅ **Press Enter** (confirms the symbol)

│   ├── QBTS_tab3.png

│   └── QBTS_tab4.png   ```5. 📸 **Take screenshot** (captures the chart)

├── SNAP/

│   ├── SNAP_tab1.png6. 💾 **Save to folder**: `screenshots/QBTS/QBTS_timestamp.png`

│   ├── SNAP_tab2.png

│   ├── SNAP_tab3.png6. Edit `.env` and set your default stock symbol:

│   └── SNAP_tab4.png

├── TSLA/   ```### Alternative Scripts

│   └── ...

└── AAPL/   DEFAULT_SYMBOL=SNAP```bash

    └── ...

```   ```# Manual control version (you focus TradingView yourself)



## Configurationpython manual_automator.py



Edit `.env` to customize:## TradingView Setup

- `STOCK_SYMBOLS` - Comma-separated list of stock symbols to process

- `CHART_LOAD_DELAY` - Base delay for chart loading (not currently used)# Test different click positions

- `SCREENSHOT_DIR` - Base directory for screenshots

Open 4 separate TradingView windows with these chart layouts:python manual_automator.py

## Utilities

1. **Trend analysis** - Your main trend analysis chart# Choose option 2 for position testing

- `list_windows.py` - List all TradingView windows to verify your setup

2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view```

## Troubleshooting

3. **Volume layout** - Volume-focused chart

**Windows not found:**

- Ensure all 4 TradingView windows are open4. **Volumeprofile** - Volume profile analysis### TradingView Automation Features

- Check that window titles contain the expected keywords

- Run `python list_windows.py` to see all available windows



**Screenshots are blank or charts not fully loaded:**The window titles must contain these keywords for the automation to find them.The project includes automated TradingView desktop app interaction:

- Tab 4 already has 15s wait time (longer than others)

- Adjust `wait_time` parameter in `main.py` if needed

- Check your internet connection for chart data loading

## Usage1. **Brings TradingView to foreground** (if possible)

**Symbol not updating:**

- Script types directly after clicking center of screen2. **Changes stock symbol** using Ctrl+K shortcut

- If typing in wrong location, TradingView may have different UI layout

- Verify charts respond to direct typing of symbolRun the automation script:3. **Takes screenshot** of the current chart



**Mouse moved to corner / Script cancelled:**```bash4. **Saves screenshot** in organized folders: `screenshots/SYMBOL/`

- PyAutoGUI failsafe triggered

- Keep mouse away from screen corners during executionpython main.py



## How It Works```### Prerequisites for TradingView Automation



1. **Window Detection**: Uses `win32gui` to find TradingView windows by title keywords

2. **Window Focus**: Maximizes and brings each window to foreground

3. **Symbol Entry**: Clicks center, types symbol, presses EnterThe script will:- TradingView desktop application must be running

4. **Wait for Load**: Configurable wait times (5s or 15s) for chart rendering

5. **Screenshot**: Captures full screen and saves with symbol/tab naming1. Wait 3 seconds before starting- The app can be in the background (Alt+Tab will bring it forward)

6. **Multi-Symbol**: Loops through all symbols in `STOCK_SYMBOLS` list

2. Switch to the "Trend analysis" window and type the symbol (from `.env`)- Chart should accept direct typing (most TradingView setups do)

## Project Structure

3. Wait 7 seconds for the chart to load- Simple and reliable - no complex shortcuts needed

- `main.py` - Main automation script

- `list_windows.py` - Utility to list TradingView windows4. Take a screenshot and save as `screenshots/SYMBOL/SYMBOL_tab1.png`

- `requirements.txt` - Python dependencies

- `.env` - Configuration file (not committed)5. Switch to each of the other 3 windows and capture screenshots### Safety Features

- `.env.example` - Example environment configuration

- `.gitignore` - Git ignore rules6. Save all screenshots without timestamps (overwrites previous runs)



## License- **Failsafe**: Move mouse to top-left corner to stop automation



MIT License - feel free to use and modify for your needs.## Screenshots Location- **Simple workflow**: Alt+Tab → Click → Type → Enter → Screenshot


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
