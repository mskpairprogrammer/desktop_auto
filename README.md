# Desktop Auto - TradingView & Symbolik Automation with AI Analysis# Desktop Automation - TradingView & Symbolik Automation with AI Analysis# 



A Python-based desktop automation tool for capturing screenshots from multiple TradingView chart windows and Symbolik.com, with integrated Perplexity AI analysis for trend detection and automated email alerts. Runs continuously during market hours with configurable intervals and timestamp logging.



## 🚀 FeaturesA Python-based desktop automation tool for capturing screenshots from multiple TradingView chart windows and Symbolik.com, with integrated Perplexity AI analysis for trend detection and automated email alerts. Runs continuously during market hours with configurable intervals.



### Screenshot Automation

- ✅ Automatically switches between 4 separate TradingView windows

- ✅ Processes multiple stock symbols from a configurable list## Features## Features

- ✅ Captures screenshots from Symbolik.com browser

- ✅ Types each symbol in all chart layouts

- ✅ Organizes screenshots by symbol in separate folders

- ✅ Uses Windows API for reliable window management### Screenshot Automation



### TradingView Chart Layouts- Automatically switches between 4 separate TradingView windows

1. **Trend Analysis** (Tab 1) - LuxAlgo indicators

2. **Smoothed Heiken Ashi Candles** (Tab 2)- Processes multiple stock symbols from a configurable list- Automatically switches between 4 separate TradingView windows

3. **Volume Layout** (Tab 3)

4. **Volume Profile** (Tab 4 - with extended 15s load time)- Captures screenshots from Symbolik.com browser



### Symbolik.com Integration- Types each symbol in all chart layouts- Processes multiple stock symbols from a configurable list

- ✅ Automated browser window detection

- ✅ Dropdown selection for stock search- Organizes screenshots by symbol in separate folders

- ✅ Automatic .bz suffix handling

- ✅ Configurable wait delays- Uses Windows API for reliable window management- Types each symbol in all 4 chart layouts## Features## Getting Started



### Perplexity AI Analysis

- 🤖 **Automated Screenshot Analysis**: AI analyzes all captured screenshots together

- 📊 **Trend Change Detection**: Calculates probability (0-100%) of trend changes### TradingView Chart Layouts- Captures screenshots from all chart layouts:

- 📈 **Prior Analysis Comparison**: Compares with previous analysis to detect changes

- 📝 **Comprehensive Reports**: Generates detailed market analysis reports1. **Trend analysis** (Tab 1) - Luxo Algo indicators

- 📧 **Email Alerts**: Automatic notifications for significant trend changes

- 🎯 **Confidence Levels**: very_high, high, medium, low ratings2. **Smoothed Heiken Ashi Candles** (Tab 2)  1. Trend analysis

- 🚨 **Alert Levels**: critical, high, medium, low priority

- ⚙️ **LuxAlgo Integration**: Uses official documentation for trend analysis charts3. **Volume layout** (Tab 3)

- 🔧 **Customizable Threshold**: Set minimum probability for email alerts (default 35%)

4. **Volumeprofile** (Tab 4 - with extended 15s load time)  2. Smoothed Heiken Ashi Candles

### Market Hours Scheduling

- ⏰ **Automatic Market Hours Detection**: Only runs during configured trading hours

- 🔄 **Hourly Intervals**: Captures screenshots and analysis every hour (configurable)

- 🌍 **Timezone Support**: Configurable timezone (default: US/Eastern for NYSE/NASDAQ)### Symbolik.com Integration  3. Volume layout- Automatically switches between 4 separate TradingView windows### Prerequisites

- 🔁 **Continuous Operation**: Runs in loop, sleeping outside market hours

- ⚙️ **Flexible Scheduling**: Configurable start/stop times and intervals- Automated browser window detection

- 📅 **Timestamp Logging**: All messages include date/time stamps

- Dropdown selection for stock search  4. Volumeprofile (with extended 15s load time)

## 📋 Prerequisites

- Automatic .bz suffix handling

- **Windows OS** (uses win32gui for window management)

- **Python 3.8+**- Configurable wait delays- Organizes screenshots by symbol in separate folders- Updates symbol on the first chart (Trend analysis)

- **TradingView account** with 4 separate chart windows open

- **Perplexity API key** (optional, for AI analysis) - Get from [Perplexity](https://www.perplexity.ai/)

- **Gmail account** (optional, for email alerts with App Password)

### Perplexity AI Analysis- Uses Windows API for reliable window management

## 🔧 Installation

- **Automated Screenshot Analysis**: AI analyzes all captured screenshots together

### 1. Clone the repository

```bash- **Trend Change Detection**: Calculates probability (0-100%) of trend changes- Captures screenshots from all 4 chart layouts:- Python 3.8 or higher

git clone https://github.com/mskpairprogrammer/desktop_auto.git

cd desktop_auto- **Prior Analysis Comparison**: Compares with previous analysis to detect changes

```

- **Comprehensive Reports**: Generates detailed market analysis reports## Prerequisites

### 2. Create and activate virtual environment

```bash- **Email Alerts**: Automatic notifications for significant trend changes

python -m venv .venv

.venv\Scripts\activate- **Confidence Levels**: very_high, high, medium, low confidence ratings  1. Trend analysis- VS Code with Python extension

```

- **Alert Levels**: critical, high, medium, low priority alerts

### 3. Install dependencies

```bash- **Customizable Threshold**: Set minimum probability for email alerts (default 35%)- Windows OS (uses win32gui for window management)

pip install -r requirements.txt

```



### 4. Configure environment variables### Market Hours Scheduling (NEW!)- Python 3.8+  2. Smoothed Heiken Ashi Candles

Create a `.env` file with your settings:

- **Automatic Market Hours Detection**: Only runs during configured trading hours

```bash

# Required Settings- **Hourly Intervals**: Captures screenshots and analysis every hour (configurable)- TradingView account with 4 separate chart windows open

STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL

- **Timezone Support**: Configurable timezone (default: US/Eastern for NYSE/NASDAQ)

# TradingView Windows (customize based on your window titles)

TRADINGVIEW_ENABLED=True- **Continuous Operation**: Runs in loop, sleeping outside market hours  3. Volume layout### Installation

TRADINGVIEW_WINDOW1=trend analysis

TRADINGVIEW_WINDOW2=Smoothed Heiken Ashi Candles- **Flexible Scheduling**: Configurable start/stop times and intervals

TRADINGVIEW_WINDOW3=volume layout

TRADINGVIEW_WINDOW4=volumeprofile## Setup



# Symbolik Settings## Prerequisites

SYMBOLIK_ENABLED=True

SYMBOLIK_WINDOW=workspace  4. Volumeprofile



# Perplexity AI Analysis (optional)- **Windows OS** (uses win32gui for window management)

PERPLEXITY_ENABLED=True

PERPLEXITY_API_KEY=your_perplexity_api_key_here- **Python 3.8+**1. Clone the repository:



# Email Alerts (optional)- **TradingView account** with 4 separate chart windows open

EMAIL_USER=your_email@gmail.com

EMAIL_PASSWORD=your_app_password_here- **Perplexity API key** (optional, for AI analysis) - Get from [Perplexity](https://www.perplexity.ai/)   ```bash- Saves screenshots without timestamps (overwrites previous versions)1. Clone or download this project

EMAIL_TO=recipient@email.com

SMTP_SERVER=smtp.gmail.com- **Gmail account** (optional, for email alerts with App Password)

SMTP_PORT=587

EMAIL_ALERT_THRESHOLD=35   git clone https://github.com/mskpairprogrammer/desktop_auto.git



# Scheduling Settings## Setup

SCHEDULE_ENABLED=True

CAPTURE_START_TIME=09:30   cd desktop_auto- Uses Windows API for reliable window management2. Open the project in VS Code

CAPTURE_STOP_TIME=16:00

CAPTURE_TIMEZONE=US/Eastern1. Clone the repository:

CAPTURE_INTERVAL_SECONDS=3600

```   ```bash   ```



### 5. Gmail App Password Setup (for Email Alerts)   git clone https://github.com/mskpairprogrammer/desktop_auto.git



1. Go to your Google Account settings   cd desktop_auto3. Install dependencies:

2. Navigate to Security → 2-Step Verification (enable if not already)

3. Navigate to Security → App passwords   ```

4. Generate a new app password for "Mail"

5. Copy the 16-character password to `EMAIL_PASSWORD` in `.env`2. Create a virtual environment:



## 📊 TradingView Setup2. Create and activate virtual environment:



Open 4 separate TradingView windows (**not tabs!**) with these chart layouts:   ```bash   ```bash## Prerequisites   ```bash



1. **Trend Analysis** - Your main trend analysis chart with LuxAlgo indicators   python -m venv .venv

2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view

3. **Volume Layout** - Volume-focused chart   .venv\Scripts\activate   python -m venv .venv

4. **Volume Profile** - Volume profile analysis

   ```

The window titles must contain the keywords specified in your `.env` file for the automation to find them.

   ```   pip install -r requirements.txt

## 🎯 Usage

3. Install dependencies:

### Scheduled Mode (Recommended)

   ```bash

Run continuously during market hours:

```bash   pip install -r requirements.txt

python main.py

```   ```3. Activate the virtual environment:- Windows OS (uses win32gui for window management)   ```



With `SCHEDULE_ENABLED=True`, the program will:

- ✅ Check if current time is within market hours (9:30 AM - 4:00 PM ET)

- ✅ Run screenshot capture and AI analysis4. Configure environment variables in `.env`:   ```bash

- ✅ Wait for the configured interval (default: 1 hour)

- ✅ Repeat during market hours   ```bash

- ✅ Sleep and check every 5 minutes when outside market hours

   # Required Settings   .venv\Scripts\activate- Python 3.8+4. Copy the environment template and configure:

**Example output:**

```   STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL

[2025-10-26 09:30:15] 🕐 SCHEDULED MODE ENABLED

[2025-10-26 09:30:15] Market Hours: 09:30 - 16:00 US/Eastern      ```

[2025-10-26 09:30:15] Interval: 3600s (60 minutes)

[2025-10-26 09:30:18] 🚀 RUN #1 - 2025-10-26 09:30:18 EDT   # TradingView Windows (customize based on your window titles)

[2025-10-26 09:30:18] 📊 Processing 2 symbols: QBTS, SNAP

```   TRADINGVIEW_ENABLED=True- TradingView account with 4 separate chart windows open   ```bash



### Single Run Mode   TRADINGVIEW_WINDOW1=trend analysis



Set `SCHEDULE_ENABLED=False` in `.env` to run once and exit:   TRADINGVIEW_WINDOW2=Smoothed Heiken Ashi Candles4. Install dependencies:

```bash

python main.py   TRADINGVIEW_WINDOW3=volume layout

```

   TRADINGVIEW_WINDOW4=volumeprofile   ```bash   copy .env.example .env

## 🔄 Workflow

   

For each symbol in `STOCK_SYMBOLS`:

   # Symbolik Settings   pip install -r requirements.txt

### 1. TradingView Processing (if enabled)

- Switches to each of the 4 windows   SYMBOLIK_ENABLED=True

- Clicks center of screen for focus

- Types the symbol   SYMBOLIK_WINDOW=workspace   ```## Setup   ```

- Presses Enter

- Waits for chart to load (5s for Tabs 1-3, 15s for Tab 4)   

- Takes screenshot and saves as `screenshots/SYMBOL/SYMBOL_tab#.png`

   # Perplexity AI Analysis (optional)

### 2. Symbolik Processing (if enabled)

- Brings Symbolik browser window to front   PERPLEXITY_ENABLED=True

- Clicks search dropdown

- Types symbol with .bz suffix   PERPLEXITY_API_KEY=your_perplexity_api_key_here5. Create a `.env` file based on `.env.example`:   Then edit `.env` with your specific settings.

- Waits for chart to load

- Takes screenshot and saves as `screenshots/SYMBOL/SYMBOL_symbolik.png`   



### 3. AI Analysis (if enabled)   # Email Alerts (optional)   ```bash

- Encodes all screenshots to base64

- Sends to Perplexity AI for analysis with LuxAlgo context   EMAIL_USER=your_email@gmail.com

- Compares with prior analysis (if exists)

- Calculates trend change probability   EMAIL_PASSWORD=your_app_password_here   copy .env.example .env1. Clone the repository:

- Generates comprehensive analysis report

- Saves to `screenshots/SYMBOL/combined_analysis_latest.txt`   EMAIL_TO=recipient@email.com

- Sends email alert if probability >= threshold

   SMTP_SERVER=smtp.gmail.com   ```

### 4. Scheduled Loop

- If during market hours: waits for interval, then repeats   SMTP_PORT=587

- If outside market hours: checks every 5 minutes

   EMAIL_ALERT_THRESHOLD=35   ```bash### Configuration

## 📁 Screenshots Organization

   

Screenshots are organized by symbol in separate folders:

   # Scheduling Settings6. Edit `.env` and set your stock symbols:

```

screenshots/   SCHEDULE_ENABLED=True

├── QBTS/

│   ├── QBTS_luxoalgo.png   CAPTURE_START_TIME=09:30   ```   git clone https://github.com/mskpairprogrammer/desktop_auto.git

│   ├── QBTS_heiken.png

│   ├── QBTS_volume_layout.png   CAPTURE_STOP_TIME=16:00

│   ├── QBTS_rvol.png

│   ├── QBTS_symbolik.png   CAPTURE_TIMEZONE=US/Eastern   STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL

│   └── combined_analysis_latest.txt

├── SNAP/   CAPTURE_INTERVAL_SECONDS=3600

│   ├── SNAP_luxoalgo.png

│   ├── SNAP_heiken.png   ```   ```   cd desktop_autoThe project uses environment variables for configuration. Key settings in `.env`:

│   ├── SNAP_volume_layout.png

│   ├── SNAP_rvol.png

│   ├── SNAP_symbolik.png

│   └── combined_analysis_latest.txt### Gmail App Password Setup (for Email Alerts)   You can add or remove symbols as needed, separated by commas.

├── TSLA/

└── AAPL/

```

1. Go to your Google Account settings   ```

## 🤖 AI Analysis Reports

2. Navigate to Security → 2-Step Verification (enable if not already)

The Perplexity AI generates detailed analysis reports including:

3. Navigate to Security → App passwords## TradingView Setup

### Report Structure

- **Market Overview**: Current price, timeframe, overall market condition4. Generate a new app password for "Mail"

- **Key Visible Indicators**: Moving averages, oscillators, volume data, support/resistance

- **LuxAlgo Analysis**: Signal quality, price action concepts, overlay indicators (for trend analysis chart)5. Copy the 16-character password to `EMAIL_PASSWORD` in `.env`- `APP_NAME`: Application name (default: "Desktop Auto")

- **Critical Signals**: Most important actionable signals

- **Trading Decision**: Clear BUY/SELL/HOLD recommendation with rationale

- **Trend Change Evaluation**: Probability of trend change with confidence level

## TradingView SetupOpen 4 separate TradingView windows with these chart layouts:

### LuxAlgo Integration

For the trend analysis chart, Perplexity uses:

- **LuxAlgo Signals & Overlays**: https://docs.luxalgo.com/docs/algos/signals-overlays/signals

- **LuxAlgo Price Action Concepts**: https://docs.luxalgo.com/docs/algos/price-action-concepts/introductionOpen 4 separate TradingView windows (not tabs!) with these chart layouts:1. **Trend analysis** - Your main trend analysis chart2. Create a virtual environment:- `DEBUG`: Enable debug mode (true/false)



This ensures accurate analysis based on official LuxAlgo methodology.



### Trend Change Analysis Example1. **Trend analysis** - Your main trend analysis chart2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view

```json

{2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view

  "send_email": true,

  "alert_level": "high",3. **Volume layout** - Volume-focused chart3. **Volume layout** - Volume-focused chart   ```bash- `AUTOMATION_DELAY`: Delay between automation actions in seconds

  "trend_change_probability": 75,

  "confidence_level": "high",4. **Volumeprofile** - Volume profile analysis

  "summary": "Strong bullish reversal signals detected",

  "key_changes": [4. **Volumeprofile** - Volume profile analysis

    "Price broke above resistance",

    "Volume spike confirms momentum",The window titles must contain the keywords specified in your `.env` file for the automation to find them.

    "LuxAlgo signals show strong buy"

  ],   python -m venv .venv- `SCREENSHOT_DIR`: Directory for screenshot storage

  "probability_reasoning": "Multiple indicators align for uptrend"

}## Usage

```

The window titles must contain these keywords for the automation to find them.

### Email Alert Levels

- 🚨 **CRITICAL** (81%+ probability): Immediate action recommended### Scheduled Mode (Recommended)

- ⚠️ **HIGH** (61-80% probability): Strong trend change signals

- 📊 **MEDIUM** (41-60% probability): Mixed signals, monitor closely   ```- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

- 📈 **LOW** (21-40% probability): Minor changes detected

Run continuously during market hours:

## ⚙️ Configuration Reference

```bash## Usage

### Scheduling Settings

```bashpython main.py

SCHEDULE_ENABLED=True              # Enable continuous scheduled mode

CAPTURE_START_TIME=09:30           # Market open (24-hour format HH:MM)```

CAPTURE_STOP_TIME=16:00            # Market close (24-hour format HH:MM)

CAPTURE_TIMEZONE=US/Eastern        # Timezone for market hours

CAPTURE_INTERVAL_SECONDS=3600      # Run every hour (3600 = 1 hour)

```With `SCHEDULE_ENABLED=True`, the program will:Run the automation script:



**Common intervals:**- Check if current time is within market hours (9:30 AM - 4:00 PM ET)

- `3600` = 1 hour (recommended for market hours)

- `1800` = 30 minutes- Run screenshot capture and AI analysis```bash3. Activate the virtual environment:## Usage Examples

- `900` = 15 minutes

- `300` = 5 minutes- Wait for the configured interval (default: 1 hour)



### Screenshot Settings- Repeat during market hourspython main.py

```bash

SCREENSHOT_DIR=screenshots- Sleep and check every 5 minutes when outside market hours

SCREENSHOT_NAME_TAB1={symbol}_luxoalgo.png

SCREENSHOT_NAME_TAB2={symbol}_heiken.png```   ```bash

SCREENSHOT_NAME_TAB3={symbol}_volume_layout.png

SCREENSHOT_NAME_TAB4={symbol}_rvol.png### Single Run Mode

SCREENSHOT_NAME_SYMBOLIK={symbol}_symbolik.png

```



The `{symbol}` placeholder is automatically replaced with each stock symbol.Set `SCHEDULE_ENABLED=False` in `.env` to run once and exit:



### Timing Settings```bashThe script will:   .venv\Scripts\activate### Simple Usage (Recommended)

```bash

WINDOW_SETTLE_DELAY=3.0        # Wait after bringing window to frontpython main.py

FOCUS_CLICK_DELAY=1.5          # Wait after clicking to focus

CHART_LOAD_DELAY_TAB1_3=5.0    # Chart load time for tabs 1-3```1. Wait 3 seconds before starting

CHART_LOAD_DELAY_TAB4=15.0     # Extended load time for volumeprofile

SYMBOLIK_WAIT_DELAY=10.0       # Wait for Symbolik chart to load

```

## Workflow2. For each symbol in `STOCK_SYMBOLS`:   ``````bash

### Enable/Disable Features

```bash

TRADINGVIEW_ENABLED=True    # Toggle TradingView automation

SYMBOLIK_ENABLED=True       # Toggle Symbolik automationFor each symbol in `STOCK_SYMBOLS`:   - Switch to each of the 4 windows

PERPLEXITY_ENABLED=True     # Toggle AI analysis

SCHEDULE_ENABLED=True       # Toggle scheduled continuous mode

```

1. **TradingView Processing** (if enabled):   - Click center of screen for focus# Run the simple automation

## 🔧 Troubleshooting

   - Switches to each of the 4 windows

### Windows not found

- ✅ Ensure all 4 TradingView windows are open   - Clicks center of screen for focus   - Type the symbol

- ✅ Check that window titles contain the keywords from `.env`

- ✅ Run `python list_windows.py` to see all available windows   - Types the symbol

- ✅ Update `TRADINGVIEW_WINDOW1-4` with exact window title keywords

   - Presses Enter   - Press Enter4. Install dependencies:python main.py

### Screenshots are blank or wrong timing

- ✅ Adjust wait times in `.env` if charts load slower   - Waits for chart to load (5s for Tabs 1-3, 15s for Tab 4)

- ✅ Increase `CHART_LOAD_DELAY_TAB1_3` or `CHART_LOAD_DELAY_TAB4` values

- ✅ Ensure windows are maximized   - Takes screenshot and saves as `screenshots/SYMBOL/SYMBOL_tab#.png`   - Wait for chart to load (5s for Tabs 1-3, 15s for Tab 4)

- ✅ Check screen resolution (default click position is 1280x800)



### AI Analysis fails

- ✅ Verify `PERPLEXITY_API_KEY` is set correctly2. **Symbolik Processing** (if enabled):   - Take screenshot and save as `screenshots/SYMBOL/SYMBOL_tab#.png`   ```bash```

- ✅ Check that `openai` package is installed: `pip install openai`

- ✅ Ensure screenshots exist before analysis runs   - Brings Symbolik browser window to front

- ✅ Check API key has sufficient credits

- ✅ Review error messages in console with timestamps   - Clicks search dropdown3. Process all symbols sequentially



### Email alerts not sending   - Types symbol with .bz suffix

- ✅ Verify all email settings in `.env` are correct

- ✅ For Gmail, use App Password (not regular password)   - Waits for chart to load   pip install -r requirements.txt

- ✅ Ensure SMTP port 587 is not blocked by firewall

- ✅ Check spam folder for alerts   - Takes screenshot and saves as `screenshots/SYMBOL/SYMBOL_symbolik.png`

- ✅ Verify 2-Step Verification is enabled for Gmail account

## Screenshots Location

### Perplexity API errors

- **401 Unauthorized**: Invalid API key3. **AI Analysis** (if enabled):

- **429 Too Many Requests**: Rate limit exceeded, wait and retry

- **500 Server Error**: Perplexity service issue, try again later   - Encodes all screenshots to base64   ```### What the simple automation does:



### Scheduling issues   - Sends to Perplexity AI for analysis

- **"Outside market hours" during trading day**: Check `CAPTURE_TIMEZONE` matches your market

- **Not running at expected times**: Verify `CAPTURE_START_TIME` and `CAPTURE_STOP_TIME` are correct   - Compares with prior analysis (if exists)Screenshots are organized by symbol in separate folders under `screenshots/`:

- **pytz errors**: Install with `pip install pytz`

- **Running continuously even outside hours**: Set `SCHEDULE_ENABLED=True` in `.env`   - Calculates trend change probability



## 📦 Project Structure   - Generates comprehensive analysis report1. 🔄 **Alt+Tab to TradingView** (brings app to foreground)



```   - Saves to `screenshots/SYMBOL/combined_analysis_latest.txt`

desktop_auto/

├── main.py                    # Main automation orchestrator with scheduling   - Sends email alert if probability >= thresholdExample with `STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL`:

├── perplexity_analysis.py     # AI analysis module with LuxAlgo integration

├── list_windows.py            # Utility to list available windows

├── test_symbolik.py           # Symbolik automation test

├── requirements.txt           # Python dependencies4. **Scheduled Loop**:```5. Create a `.env` file based on `.env.example`:2. �️ **Click center of screen** (activates chart area)

├── .env                       # Configuration (not in git)

├── .env.example               # Example configuration template   - If during market hours: waits for interval, then repeats

├── .gitignore                 # Git ignore rules

├── README.md                  # This file   - If outside market hours: checks every 5 minutesscreenshots/

└── screenshots/               # Output directory

    ├── QBTS/

    ├── SNAP/

    ├── TSLA/## Screenshots Organization├── QBTS/   ```bash3. ⌨️ **Type "QBTS"** (enters the stock symbol)

    └── AAPL/

```



## 📚 DependenciesScreenshots are organized by symbol in separate folders:│   ├── QBTS_tab1.png



- `pyautogui>=0.9.54` - Desktop automation

- `pillow>=10.0.0` - Screenshot handling

- `pywin32>=306` - Windows API for window management```│   ├── QBTS_tab2.png   copy .env.example .env4. ✅ **Press Enter** (confirms the symbol)

- `python-dotenv>=1.0.0` - Environment configuration

- `pynput` - Mouse/keyboard inputscreenshots/

- `openai>=1.0.0` - Perplexity API client

- `pytz>=2023.3` - Timezone support for scheduling├── QBTS/│   ├── QBTS_tab3.png



## 💡 Usage Examples│   ├── QBTS_luxoalgo.png



### Run during market hours with hourly captures│   ├── QBTS_heiken.png│   └── QBTS_tab4.png   ```5. 📸 **Take screenshot** (captures the chart)

```bash

# In .env│   ├── QBTS_volume_layout.png

SCHEDULE_ENABLED=True

CAPTURE_START_TIME=09:30│   ├── QBTS_rvol.png├── SNAP/

CAPTURE_STOP_TIME=16:00

CAPTURE_INTERVAL_SECONDS=3600│   ├── QBTS_symbolik.png



# Run│   └── combined_analysis_latest.txt│   ├── SNAP_tab1.png6. 💾 **Save to folder**: `screenshots/QBTS/QBTS_timestamp.png`

python main.py

```├── SNAP/



### Run every 30 minutes during extended hours│   ├── SNAP_luxoalgo.png│   ├── SNAP_tab2.png

```bash

# In .env│   ├── SNAP_heiken.png

CAPTURE_START_TIME=08:00

CAPTURE_STOP_TIME=18:00│   ├── SNAP_volume_layout.png│   ├── SNAP_tab3.png6. Edit `.env` and set your default stock symbol:

CAPTURE_INTERVAL_SECONDS=1800

│   ├── SNAP_rvol.png

# Run

python main.py│   ├── SNAP_symbolik.png│   └── SNAP_tab4.png

```

│   └── combined_analysis_latest.txt

### Run once without scheduling

```bash├── TSLA/├── TSLA/   ```### Alternative Scripts

# In .env

SCHEDULE_ENABLED=False└── AAPL/



# Run```│   └── ...

python main.py

```



### View available windows## AI Analysis Reports└── AAPL/   DEFAULT_SYMBOL=SNAP```bash

```bash

python list_windows.py

```

The Perplexity AI generates detailed analysis reports including:    └── ...

### Test Symbolik automation

```bash

python test_symbolik.py

```### Report Structure```   ```# Manual control version (you focus TradingView yourself)



## 📝 License- **Market Overview**: Current price, timeframe, overall market condition



This project is for personal use.- **Key Visible Indicators**: Moving averages, oscillators, volume data, support/resistance



## 🤝 Contributing- **Critical Signals**: Most important actionable signals



Feel free to submit issues or pull requests for improvements.- **Trading Decision**: Clear BUY/SELL/HOLD recommendation with rationale## Configurationpython manual_automator.py



## 📅 Changelog- **Trend Change Evaluation**: Probability of trend change with confidence level



### v2.2.0 - LuxAlgo Integration & Logging (2025-10-26)

- Added LuxAlgo documentation references for Perplexity AI

- Implemented timestamp logging for all messages### Trend Change Analysis

- Enhanced trend analysis with official LuxAlgo methodology

- Improved debugging with date/time stamped logs```jsonEdit `.env` to customize:## TradingView Setup



### v2.1.0 - Market Hours Scheduling (2025-10-26){

- Added scheduled continuous operation mode

- Market hours detection with timezone support  "send_email": true,- `STOCK_SYMBOLS` - Comma-separated list of stock symbols to process

- Configurable capture intervals

- Automatic sleep outside market hours  "alert_level": "high",

- Run count tracking

  "trend_change_probability": 75,- `CHART_LOAD_DELAY` - Base delay for chart loading (not currently used)# Test different click positions

### v2.0.0 - AI Analysis Integration (2025-10-25)

- Added Perplexity AI screenshot analysis  "confidence_level": "high",

- Trend change detection with probability scoring

- Email alert system with configurable thresholds  "summary": "Strong bullish reversal signals detected",- `SCREENSHOT_DIR` - Base directory for screenshots

- Comprehensive analysis reports

- Prior analysis comparison  "key_changes": [



### v1.1.0 - Symbolik Integration (2025-10-24)    "Price broke above resistance",Open 4 separate TradingView windows with these chart layouts:python manual_automator.py

- Added Symbolik.com browser automation

- Dropdown selection support    "Volume spike confirms momentum"

- Automatic .bz suffix handling

  ],## Utilities

### v1.0.0 - Initial Release (2025-10-23)

- Multi-window TradingView automation  "probability_reasoning": "Multiple indicators align for uptrend"

- Multi-symbol support

- Screenshot capture and organization}1. **Trend analysis** - Your main trend analysis chart# Choose option 2 for position testing

- Parameterized configuration

```

## 🔗 Links

- `list_windows.py` - List all TradingView windows to verify your setup

- **Repository**: https://github.com/mskpairprogrammer/desktop_auto

- **LuxAlgo Signals Documentation**: https://docs.luxalgo.com/docs/algos/signals-overlays/signals### Email Alert Levels

- **LuxAlgo Price Action Documentation**: https://docs.luxalgo.com/docs/algos/price-action-concepts/introduction

- **Perplexity AI**: https://www.perplexity.ai/- 🚨 **CRITICAL** (81%+ probability): Immediate action recommended2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view```



## 📞 Support- ⚠️ **HIGH** (61-80% probability): Strong trend change signals



For issues or questions:- 📊 **MEDIUM** (41-60% probability): Mixed signals, monitor closely## Troubleshooting

1. Check the [Troubleshooting](#-troubleshooting) section

2. Review existing [GitHub Issues](https://github.com/mskpairprogrammer/desktop_auto/issues)- 📈 **LOW** (21-40% probability): Minor changes detected

3. Create a new issue with detailed description and logs

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
