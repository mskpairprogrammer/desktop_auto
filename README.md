# Desktop Auto - TradingView & Symbolik Automation with AI Analysis# Desktop Auto - TradingView & Symbolik Automation with AI Analysis



A Python-based desktop automation tool for capturing screenshots from multiple TradingView chart windows and Symbolik.com, with integrated Perplexity AI analysis for trend detection and automated email alerts. Runs continuously during market hours with configurable intervals.A Python-based desktop automation tool for capturing screenshots from multiple TradingView chart windows and Symbolik.com, with integrated Perplexity AI analysis for trend detection and email alerts.



## Features## Features



### Screenshot Automation

- Automatically switches between 4 separate TradingView windows

- Processes multiple stock symbols from a configurable list- Automatically switches between 4 separate TradingView windows

- Captures screenshots from Symbolik.com browser

- Types each symbol in all chart layouts- Processes multiple stock symbols from a configurable list

- Organizes screenshots by symbol in separate folders

- Uses Windows API for reliable window management- Types each symbol in all 4 chart layouts## Features## Getting Started



### TradingView Chart Layouts- Captures screenshots from all chart layouts:

1. **Trend analysis** (Tab 1) - Luxo Algo indicators

2. **Smoothed Heiken Ashi Candles** (Tab 2)  1. Trend analysis

3. **Volume layout** (Tab 3)

4. **Volumeprofile** (Tab 4 - with extended 15s load time)  2. Smoothed Heiken Ashi Candles



### Symbolik.com Integration  3. Volume layout- Automatically switches between 4 separate TradingView windows### Prerequisites

- Automated browser window detection

- Dropdown selection for stock search  4. Volumeprofile (with extended 15s load time)

- Automatic .bz suffix handling

- Configurable wait delays- Organizes screenshots by symbol in separate folders- Updates symbol on the first chart (Trend analysis)



### Perplexity AI Analysis- Uses Windows API for reliable window management

- **Automated Screenshot Analysis**: AI analyzes all captured screenshots together

- **Trend Change Detection**: Calculates probability (0-100%) of trend changes- Captures screenshots from all 4 chart layouts:- Python 3.8 or higher

- **Prior Analysis Comparison**: Compares with previous analysis to detect changes

- **Comprehensive Reports**: Generates detailed market analysis reports## Prerequisites

- **Email Alerts**: Automatic notifications for significant trend changes

- **Confidence Levels**: very_high, high, medium, low confidence ratings  1. Trend analysis- VS Code with Python extension

- **Alert Levels**: critical, high, medium, low priority alerts

- **Customizable Threshold**: Set minimum probability for email alerts (default 35%)- Windows OS (uses win32gui for window management)



### Market Hours Scheduling (NEW!)- Python 3.8+  2. Smoothed Heiken Ashi Candles

- **Automatic Market Hours Detection**: Only runs during configured trading hours

- **Hourly Intervals**: Captures screenshots and analysis every hour (configurable)- TradingView account with 4 separate chart windows open

- **Timezone Support**: Configurable timezone (default: US/Eastern for NYSE/NASDAQ)

- **Continuous Operation**: Runs in loop, sleeping outside market hours  3. Volume layout### Installation

- **Flexible Scheduling**: Configurable start/stop times and intervals

## Setup

## Prerequisites

  4. Volumeprofile

- **Windows OS** (uses win32gui for window management)

- **Python 3.8+**1. Clone the repository:

- **TradingView account** with 4 separate chart windows open

- **Perplexity API key** (optional, for AI analysis) - Get from [Perplexity](https://www.perplexity.ai/)   ```bash- Saves screenshots without timestamps (overwrites previous versions)1. Clone or download this project

- **Gmail account** (optional, for email alerts with App Password)

   git clone https://github.com/mskpairprogrammer/desktop_auto.git

## Setup

   cd desktop_auto- Uses Windows API for reliable window management2. Open the project in VS Code

1. Clone the repository:

   ```bash   ```

   git clone https://github.com/mskpairprogrammer/desktop_auto.git

   cd desktop_auto3. Install dependencies:

   ```

2. Create a virtual environment:

2. Create and activate virtual environment:

   ```bash   ```bash## Prerequisites   ```bash

   python -m venv .venv

   .venv\Scripts\activate   python -m venv .venv

   ```

   ```   pip install -r requirements.txt

3. Install dependencies:

   ```bash

   pip install -r requirements.txt

   ```3. Activate the virtual environment:- Windows OS (uses win32gui for window management)   ```



4. Configure environment variables in `.env`:   ```bash

   ```bash

   # Required Settings   .venv\Scripts\activate- Python 3.8+4. Copy the environment template and configure:

   STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL

      ```

   # TradingView Windows (customize based on your window titles)

   TRADINGVIEW_ENABLED=True- TradingView account with 4 separate chart windows open   ```bash

   TRADINGVIEW_WINDOW1=trend analysis

   TRADINGVIEW_WINDOW2=Smoothed Heiken Ashi Candles4. Install dependencies:

   TRADINGVIEW_WINDOW3=volume layout

   TRADINGVIEW_WINDOW4=volumeprofile   ```bash   copy .env.example .env

   

   # Symbolik Settings   pip install -r requirements.txt

   SYMBOLIK_ENABLED=True

   SYMBOLIK_WINDOW=workspace   ```## Setup   ```

   

   # Perplexity AI Analysis (optional)

   PERPLEXITY_ENABLED=True

   PERPLEXITY_API_KEY=your_perplexity_api_key_here5. Create a `.env` file based on `.env.example`:   Then edit `.env` with your specific settings.

   

   # Email Alerts (optional)   ```bash

   EMAIL_USER=your_email@gmail.com

   EMAIL_PASSWORD=your_app_password_here   copy .env.example .env1. Clone the repository:

   EMAIL_TO=recipient@email.com

   SMTP_SERVER=smtp.gmail.com   ```

   SMTP_PORT=587

   EMAIL_ALERT_THRESHOLD=35   ```bash### Configuration

   

   # Scheduling Settings6. Edit `.env` and set your stock symbols:

   SCHEDULE_ENABLED=True

   CAPTURE_START_TIME=09:30   ```   git clone https://github.com/mskpairprogrammer/desktop_auto.git

   CAPTURE_STOP_TIME=16:00

   CAPTURE_TIMEZONE=US/Eastern   STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL

   CAPTURE_INTERVAL_SECONDS=3600

   ```   ```   cd desktop_autoThe project uses environment variables for configuration. Key settings in `.env`:



### Gmail App Password Setup (for Email Alerts)   You can add or remove symbols as needed, separated by commas.



1. Go to your Google Account settings   ```

2. Navigate to Security → 2-Step Verification (enable if not already)

3. Navigate to Security → App passwords## TradingView Setup

4. Generate a new app password for "Mail"

5. Copy the 16-character password to `EMAIL_PASSWORD` in `.env`- `APP_NAME`: Application name (default: "Desktop Auto")



## TradingView SetupOpen 4 separate TradingView windows with these chart layouts:



Open 4 separate TradingView windows (not tabs!) with these chart layouts:1. **Trend analysis** - Your main trend analysis chart2. Create a virtual environment:- `DEBUG`: Enable debug mode (true/false)



1. **Trend analysis** - Your main trend analysis chart2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view

2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view

3. **Volume layout** - Volume-focused chart3. **Volume layout** - Volume-focused chart   ```bash- `AUTOMATION_DELAY`: Delay between automation actions in seconds

4. **Volumeprofile** - Volume profile analysis

4. **Volumeprofile** - Volume profile analysis

The window titles must contain the keywords specified in your `.env` file for the automation to find them.

   python -m venv .venv- `SCREENSHOT_DIR`: Directory for screenshot storage

## Usage

The window titles must contain these keywords for the automation to find them.

### Scheduled Mode (Recommended)

   ```- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

Run continuously during market hours:

```bash## Usage

python main.py

```



With `SCHEDULE_ENABLED=True`, the program will:Run the automation script:

- Check if current time is within market hours (9:30 AM - 4:00 PM ET)

- Run screenshot capture and AI analysis```bash3. Activate the virtual environment:## Usage Examples

- Wait for the configured interval (default: 1 hour)

- Repeat during market hourspython main.py

- Sleep and check every 5 minutes when outside market hours

```   ```bash

### Single Run Mode



Set `SCHEDULE_ENABLED=False` in `.env` to run once and exit:

```bashThe script will:   .venv\Scripts\activate### Simple Usage (Recommended)

python main.py

```1. Wait 3 seconds before starting



## Workflow2. For each symbol in `STOCK_SYMBOLS`:   ``````bash



For each symbol in `STOCK_SYMBOLS`:   - Switch to each of the 4 windows



1. **TradingView Processing** (if enabled):   - Click center of screen for focus# Run the simple automation

   - Switches to each of the 4 windows

   - Clicks center of screen for focus   - Type the symbol

   - Types the symbol

   - Presses Enter   - Press Enter4. Install dependencies:python main.py

   - Waits for chart to load (5s for Tabs 1-3, 15s for Tab 4)

   - Takes screenshot and saves as `screenshots/SYMBOL/SYMBOL_tab#.png`   - Wait for chart to load (5s for Tabs 1-3, 15s for Tab 4)



2. **Symbolik Processing** (if enabled):   - Take screenshot and save as `screenshots/SYMBOL/SYMBOL_tab#.png`   ```bash```

   - Brings Symbolik browser window to front

   - Clicks search dropdown3. Process all symbols sequentially

   - Types symbol with .bz suffix

   - Waits for chart to load   pip install -r requirements.txt

   - Takes screenshot and saves as `screenshots/SYMBOL/SYMBOL_symbolik.png`

## Screenshots Location

3. **AI Analysis** (if enabled):

   - Encodes all screenshots to base64   ```### What the simple automation does:

   - Sends to Perplexity AI for analysis

   - Compares with prior analysis (if exists)Screenshots are organized by symbol in separate folders under `screenshots/`:

   - Calculates trend change probability

   - Generates comprehensive analysis report1. 🔄 **Alt+Tab to TradingView** (brings app to foreground)

   - Saves to `screenshots/SYMBOL/combined_analysis_latest.txt`

   - Sends email alert if probability >= thresholdExample with `STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL`:



4. **Scheduled Loop**:```5. Create a `.env` file based on `.env.example`:2. �️ **Click center of screen** (activates chart area)

   - If during market hours: waits for interval, then repeats

   - If outside market hours: checks every 5 minutesscreenshots/



## Screenshots Organization├── QBTS/   ```bash3. ⌨️ **Type "QBTS"** (enters the stock symbol)



Screenshots are organized by symbol in separate folders:│   ├── QBTS_tab1.png



```│   ├── QBTS_tab2.png   copy .env.example .env4. ✅ **Press Enter** (confirms the symbol)

screenshots/

├── QBTS/│   ├── QBTS_tab3.png

│   ├── QBTS_luxoalgo.png

│   ├── QBTS_heiken.png│   └── QBTS_tab4.png   ```5. 📸 **Take screenshot** (captures the chart)

│   ├── QBTS_volume_layout.png

│   ├── QBTS_rvol.png├── SNAP/

│   ├── QBTS_symbolik.png

│   └── combined_analysis_latest.txt│   ├── SNAP_tab1.png6. 💾 **Save to folder**: `screenshots/QBTS/QBTS_timestamp.png`

├── SNAP/

│   ├── SNAP_luxoalgo.png│   ├── SNAP_tab2.png

│   ├── SNAP_heiken.png

│   ├── SNAP_volume_layout.png│   ├── SNAP_tab3.png6. Edit `.env` and set your default stock symbol:

│   ├── SNAP_rvol.png

│   ├── SNAP_symbolik.png│   └── SNAP_tab4.png

│   └── combined_analysis_latest.txt

├── TSLA/├── TSLA/   ```### Alternative Scripts

└── AAPL/

```│   └── ...



## AI Analysis Reports└── AAPL/   DEFAULT_SYMBOL=SNAP```bash



The Perplexity AI generates detailed analysis reports including:    └── ...



### Report Structure```   ```# Manual control version (you focus TradingView yourself)

- **Market Overview**: Current price, timeframe, overall market condition

- **Key Visible Indicators**: Moving averages, oscillators, volume data, support/resistance

- **Critical Signals**: Most important actionable signals

- **Trading Decision**: Clear BUY/SELL/HOLD recommendation with rationale## Configurationpython manual_automator.py

- **Trend Change Evaluation**: Probability of trend change with confidence level



### Trend Change Analysis

```jsonEdit `.env` to customize:## TradingView Setup

{

  "send_email": true,- `STOCK_SYMBOLS` - Comma-separated list of stock symbols to process

  "alert_level": "high",

  "trend_change_probability": 75,- `CHART_LOAD_DELAY` - Base delay for chart loading (not currently used)# Test different click positions

  "confidence_level": "high",

  "summary": "Strong bullish reversal signals detected",- `SCREENSHOT_DIR` - Base directory for screenshots

  "key_changes": [

    "Price broke above resistance",Open 4 separate TradingView windows with these chart layouts:python manual_automator.py

    "Volume spike confirms momentum"

  ],## Utilities

  "probability_reasoning": "Multiple indicators align for uptrend"

}1. **Trend analysis** - Your main trend analysis chart# Choose option 2 for position testing

```

- `list_windows.py` - List all TradingView windows to verify your setup

### Email Alert Levels

- 🚨 **CRITICAL** (81%+ probability): Immediate action recommended2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view```

- ⚠️ **HIGH** (61-80% probability): Strong trend change signals

- 📊 **MEDIUM** (41-60% probability): Mixed signals, monitor closely## Troubleshooting

- 📈 **LOW** (21-40% probability): Minor changes detected

3. **Volume layout** - Volume-focused chart

## Configuration Reference

**Windows not found:**

### Scheduling Settings

```bash- Ensure all 4 TradingView windows are open4. **Volumeprofile** - Volume profile analysis### TradingView Automation Features

SCHEDULE_ENABLED=True              # Enable continuous scheduled mode

CAPTURE_START_TIME=09:30           # Market open (24-hour format HH:MM)- Check that window titles contain the expected keywords

CAPTURE_STOP_TIME=16:00            # Market close (24-hour format HH:MM)

CAPTURE_TIMEZONE=US/Eastern        # Timezone for market hours- Run `python list_windows.py` to see all available windows

CAPTURE_INTERVAL_SECONDS=3600      # Run every hour (3600 = 1 hour)

```



**Common intervals:****Screenshots are blank or charts not fully loaded:**The window titles must contain these keywords for the automation to find them.The project includes automated TradingView desktop app interaction:

- `3600` = 1 hour (recommended for market hours)

- `1800` = 30 minutes- Tab 4 already has 15s wait time (longer than others)

- `900` = 15 minutes

- `300` = 5 minutes- Adjust `wait_time` parameter in `main.py` if needed



### Screenshot Settings- Check your internet connection for chart data loading

```bash

SCREENSHOT_DIR=screenshots## Usage1. **Brings TradingView to foreground** (if possible)

SCREENSHOT_NAME_TAB1={symbol}_luxoalgo.png

SCREENSHOT_NAME_TAB2={symbol}_heiken.png**Symbol not updating:**

SCREENSHOT_NAME_TAB3={symbol}_volume_layout.png

SCREENSHOT_NAME_TAB4={symbol}_rvol.png- Script types directly after clicking center of screen2. **Changes stock symbol** using Ctrl+K shortcut

SCREENSHOT_NAME_SYMBOLIK={symbol}_symbolik.png

```- If typing in wrong location, TradingView may have different UI layout



The `{symbol}` placeholder is automatically replaced with each stock symbol.- Verify charts respond to direct typing of symbolRun the automation script:3. **Takes screenshot** of the current chart



### Timing Settings

```bash

WINDOW_SETTLE_DELAY=3.0        # Wait after bringing window to front**Mouse moved to corner / Script cancelled:**```bash4. **Saves screenshot** in organized folders: `screenshots/SYMBOL/`

FOCUS_CLICK_DELAY=1.5          # Wait after clicking to focus

CHART_LOAD_DELAY_TAB1_3=5.0    # Chart load time for tabs 1-3- PyAutoGUI failsafe triggered

CHART_LOAD_DELAY_TAB4=15.0     # Extended load time for volumeprofile

SYMBOLIK_WAIT_DELAY=10.0       # Wait for Symbolik chart to load- Keep mouse away from screen corners during executionpython main.py

```



### Enable/Disable Features

```bash## How It Works```### Prerequisites for TradingView Automation

TRADINGVIEW_ENABLED=True    # Toggle TradingView automation

SYMBOLIK_ENABLED=True       # Toggle Symbolik automation

PERPLEXITY_ENABLED=True     # Toggle AI analysis

SCHEDULE_ENABLED=True       # Toggle scheduled continuous mode1. **Window Detection**: Uses `win32gui` to find TradingView windows by title keywords

```

2. **Window Focus**: Maximizes and brings each window to foreground

## Troubleshooting

3. **Symbol Entry**: Clicks center, types symbol, presses EnterThe script will:- TradingView desktop application must be running

### Windows not found

- Ensure all 4 TradingView windows are open4. **Wait for Load**: Configurable wait times (5s or 15s) for chart rendering

- Check that window titles contain the keywords from `.env`

- Run `python list_windows.py` to see all available windows5. **Screenshot**: Captures full screen and saves with symbol/tab naming1. Wait 3 seconds before starting- The app can be in the background (Alt+Tab will bring it forward)



### Screenshots are blank or wrong timing6. **Multi-Symbol**: Loops through all symbols in `STOCK_SYMBOLS` list

- Adjust wait times in `.env` if charts load slower

- Increase `CHART_LOAD_DELAY_TAB1_3` or `CHART_LOAD_DELAY_TAB4` values2. Switch to the "Trend analysis" window and type the symbol (from `.env`)- Chart should accept direct typing (most TradingView setups do)



### AI Analysis fails## Project Structure

- Verify `PERPLEXITY_API_KEY` is set correctly

- Check that `openai` package is installed: `pip install openai`3. Wait 7 seconds for the chart to load- Simple and reliable - no complex shortcuts needed

- Ensure screenshots exist before analysis runs

- Check API key has sufficient credits- `main.py` - Main automation script



### Email alerts not sending- `list_windows.py` - Utility to list TradingView windows4. Take a screenshot and save as `screenshots/SYMBOL/SYMBOL_tab1.png`

- Verify all email settings in `.env` are correct

- For Gmail, use App Password (not regular password)- `requirements.txt` - Python dependencies

- Ensure SMTP port 587 is not blocked by firewall

- Check spam folder for alerts- `.env` - Configuration file (not committed)5. Switch to each of the other 3 windows and capture screenshots### Safety Features



### Perplexity API errors- `.env.example` - Example environment configuration

- `401 Unauthorized`: Invalid API key

- `429 Too Many Requests`: Rate limit exceeded, wait and retry- `.gitignore` - Git ignore rules6. Save all screenshots without timestamps (overwrites previous runs)

- `500 Server Error`: Perplexity service issue, try again later



### Scheduling issues

- **"Outside market hours" during trading day**: Check `CAPTURE_TIMEZONE` matches your market## License- **Failsafe**: Move mouse to top-left corner to stop automation

- **Not running at expected times**: Verify `CAPTURE_START_TIME` and `CAPTURE_STOP_TIME` are correct

- **pytz errors**: Install with `pip install pytz`

- **Running continuously even outside hours**: Set `SCHEDULE_ENABLED=True` in `.env`

MIT License - feel free to use and modify for your needs.## Screenshots Location- **Simple workflow**: Alt+Tab → Click → Type → Enter → Screenshot

## Project Structure



```- **Error handling**: Clear error messages and graceful failures

desktop_auto/

├── main.py                    # Main automation orchestrator with schedulingScreenshots are saved in `screenshots/SYMBOL/` where SYMBOL is the stock symbol from your `.env` file.

├── perplexity_analysis.py     # AI analysis module

├── list_windows.py            # Utility to list available windows## Project Structure

├── test_symbolik.py           # Symbolik automation test

├── requirements.txt           # Python dependenciesExample:

├── .env                       # Configuration (not in git)

├── .gitignore                 # Git ignore rules- `screenshots/SNAP/SNAP_tab1.png````

├── README.md                  # This file

└── screenshots/               # Output directory- `screenshots/SNAP/SNAP_tab2.png`desktop_auto/

```

- `screenshots/SNAP/SNAP_tab3.png`├── main.py              # Main application entry point

## Dependencies

- `screenshots/SNAP/SNAP_tab4.png`├── requirements.txt     # Python dependencies

- `pyautogui>=0.9.54` - Desktop automation

- `pillow>=10.0.0` - Screenshot handling├── README.md           # This file

- `pywin32>=306` - Windows API for window management

- `python-dotenv>=1.0.0` - Environment configuration## Utilities└── .github/

- `pynput` - Mouse/keyboard input

- `openai>=1.0.0` - Perplexity API client    └── copilot-instructions.md  # Copilot configuration

- `pytz>=2023.3` - Timezone support for scheduling

- `list_windows.py` - List all TradingView windows to verify your setup```

## Usage Examples



### Run during market hours with hourly captures

```bash## Troubleshooting## Development

# In .env

SCHEDULE_ENABLED=True

CAPTURE_START_TIME=09:30

CAPTURE_STOP_TIME=16:00**Windows not found:**This project is set up for development in VS Code with Python support. The recommended extensions will be suggested when you open the project.

CAPTURE_INTERVAL_SECONDS=3600

- Ensure all 4 TradingView windows are open

# Run

python main.py- Check that window titles contain the expected keywords## License

```

- Run `python list_windows.py` to see all available windows

### Run every 30 minutes during extended hours

```bashThis project is for personal use.

# In .env**Screenshots are blank or wrong timing:**

CAPTURE_START_TIME=08:00- Adjust wait times in `main.py` if charts load slower

CAPTURE_STOP_TIME=18:00- Increase `time.sleep()` values after window switches

CAPTURE_INTERVAL_SECONDS=1800

**Symbol not updating:**

# Run- Verify the click position (1674, 1568) matches your screen resolution

python main.py- Adjust coordinates in `main.py` for your setup

```

## Project Structure

### Run once without scheduling

```bash- `main.py` - Main automation script

# In .env- `list_windows.py` - Utility to list TradingView windows

SCHEDULE_ENABLED=False- `requirements.txt` - Python dependencies

- `.env.example` - Example environment configuration

# Run- `.gitignore` - Git ignore rules

python main.py

```## License



## LicenseMIT License - feel free to use and modify for your needs.


This project is for personal use.

## Contributing

Feel free to submit issues or pull requests for improvements.

## Changelog

### v2.1.0 - Market Hours Scheduling
- Added scheduled continuous operation mode
- Market hours detection with timezone support
- Configurable capture intervals
- Automatic sleep outside market hours
- Run count tracking

### v2.0.0 - AI Analysis Integration
- Added Perplexity AI screenshot analysis
- Trend change detection with probability scoring
- Email alert system with configurable thresholds
- Comprehensive analysis reports
- Prior analysis comparison

### v1.1.0 - Symbolik Integration
- Added Symbolik.com browser automation
- Dropdown selection support
- Automatic .bz suffix handling

### v1.0.0 - Initial Release
- Multi-window TradingView automation
- Multi-symbol support
- Screenshot capture and organization
- Parameterized configuration
