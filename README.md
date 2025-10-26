# 📊 Desktop Auto - Intelligent TradingView Automation# Desktop Auto - TradingView & Symbolik Automation with AI Analysis# 



> **Automated screenshot capture, AI-powered analysis, and email alerts for stock trading workflows**



[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)A Python-based desktop automation tool for capturing screenshots from multiple TradingView chart windows and Symbolik.com, with integrated Perplexity AI analysis for trend detection and automated email alerts. Runs continuously during market hours with configurable intervals and timestamp logging.

[![License](https://img.shields.io/badge/license-Personal%20Use-green.svg)](LICENSE)

[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)



A sophisticated Python-based desktop automation tool that captures screenshots from multiple TradingView chart windows and Symbolik.com, performs AI-powered analysis using Perplexity, and sends intelligent email alerts. Features market hours scheduling, timestamp logging, and LuxAlgo indicator integration.## 🚀 FeaturesA Python-based desktop automation tool for capturing screenshots from multiple TradingView chart windows and Symbolik.com, with integrated Perplexity AI analysis for trend detection and automated email alerts. Runs continuously during market hours with configurable intervals.



---



## ✨ Key Features### Screenshot Automation



### 🖥️ Multi-Window Screenshot Automation- ✅ Automatically switches between 4 separate TradingView windows

- **4 TradingView Windows**: Automatically cycles through separate chart layouts

- **Symbolik.com Integration**: Browser automation with dropdown search- ✅ Processes multiple stock symbols from a configurable list## Features## Features

- **Smart Window Detection**: Windows API for reliable window management

- **Multi-Symbol Support**: Process multiple stock symbols sequentially- ✅ Captures screenshots from Symbolik.com browser

- **Organized Storage**: Screenshots saved by symbol in dedicated folders

- ✅ Types each symbol in all chart layouts

### 🤖 AI-Powered Analysis (Perplexity)

- **Intelligent Chart Analysis**: AI examines all screenshots together- ✅ Organizes screenshots by symbol in separate folders

- **LuxAlgo Integration**: Uses official documentation for trend analysis

  - [Signals & Overlays](https://docs.luxalgo.com/docs/algos/signals-overlays/signals)- ✅ Uses Windows API for reliable window management### Screenshot Automation

  - [Price Action Concepts](https://docs.luxalgo.com/docs/algos/price-action-concepts/introduction)

- **Trend Change Detection**: 0-100% probability scoring

- **Historical Comparison**: Compares with previous analysis

- **Confidence Ratings**: Very High, High, Medium, Low### TradingView Chart Layouts- Automatically switches between 4 separate TradingView windows

- **Comprehensive Reports**: Detailed market analysis saved as text

1. **Trend Analysis** (Tab 1) - LuxAlgo indicators

### 📧 Smart Email Alerts

- **Automatic Notifications**: Triggered by trend change probability2. **Smoothed Heiken Ashi Candles** (Tab 2)- Processes multiple stock symbols from a configurable list- Automatically switches between 4 separate TradingView windows

- **Customizable Threshold**: Set minimum probability (default 35%)

- **Priority Levels**: 🚨 Critical, ⚠️ High, 📊 Medium, 📈 Low3. **Volume Layout** (Tab 3)

- **Rich Content**: Includes probability, changes, and full analysis

- **Gmail Integration**: Secure App Password authentication4. **Volume Profile** (Tab 4 - with extended 15s load time)- Captures screenshots from Symbolik.com browser



### ⏰ Market Hours Scheduling

- **Timezone Aware**: Configurable timezone (default: US/Eastern)

- **Automatic Start/Stop**: Only runs during trading hours### Symbolik.com Integration- Types each symbol in all chart layouts- Processes multiple stock symbols from a configurable list

- **Flexible Intervals**: Hourly, 30min, 15min, or custom

- **Outside Hours Handling**: Sleeps and checks every 5 minutes- ✅ Automated browser window detection

- **Continuous Operation**: Runs in loop with run counting

- **Timestamp Logging**: All messages include date/time- ✅ Dropdown selection for stock search- Organizes screenshots by symbol in separate folders



---- ✅ Automatic .bz suffix handling



## 📋 Table of Contents- ✅ Configurable wait delays- Uses Windows API for reliable window management- Types each symbol in all 4 chart layouts## Features## Getting Started



- [Prerequisites](#-prerequisites)

- [Quick Start](#-quick-start)

- [Configuration](#-configuration)### Perplexity AI Analysis

- [Usage](#-usage)

- [TradingView Setup](#-tradingview-setup)- 🤖 **Automated Screenshot Analysis**: AI analyzes all captured screenshots together

- [AI Analysis](#-ai-analysis)

- [Scheduling](#-scheduling)- 📊 **Trend Change Detection**: Calculates probability (0-100%) of trend changes### TradingView Chart Layouts- Captures screenshots from all chart layouts:

- [Troubleshooting](#-troubleshooting)

- [Project Structure](#-project-structure)- 📈 **Prior Analysis Comparison**: Compares with previous analysis to detect changes

- [Examples](#-examples)

- [Changelog](#-changelog)- 📝 **Comprehensive Reports**: Generates detailed market analysis reports1. **Trend analysis** (Tab 1) - Luxo Algo indicators



---- 📧 **Email Alerts**: Automatic notifications for significant trend changes



## 🔧 Prerequisites- 🎯 **Confidence Levels**: very_high, high, medium, low ratings2. **Smoothed Heiken Ashi Candles** (Tab 2)  1. Trend analysis



| Requirement | Description |- 🚨 **Alert Levels**: critical, high, medium, low priority

|------------|-------------|

| **Operating System** | Windows 10/11 (uses `win32gui` API) |- ⚙️ **LuxAlgo Integration**: Uses official documentation for trend analysis charts3. **Volume layout** (Tab 3)

| **Python** | Version 3.8 or higher |

| **TradingView** | Account with 4 separate chart windows |- 🔧 **Customizable Threshold**: Set minimum probability for email alerts (default 35%)

| **Perplexity API** | API key from [perplexity.ai](https://www.perplexity.ai/) *(optional)* |

| **Gmail Account** | For email alerts with App Password *(optional)* |4. **Volumeprofile** (Tab 4 - with extended 15s load time)  2. Smoothed Heiken Ashi Candles



---### Market Hours Scheduling



## 🚀 Quick Start- ⏰ **Automatic Market Hours Detection**: Only runs during configured trading hours



### 1️⃣ Installation- 🔄 **Hourly Intervals**: Captures screenshots and analysis every hour (configurable)



```bash- 🌍 **Timezone Support**: Configurable timezone (default: US/Eastern for NYSE/NASDAQ)### Symbolik.com Integration  3. Volume layout- Automatically switches between 4 separate TradingView windows### Prerequisites

# Clone the repository

git clone https://github.com/mskpairprogrammer/desktop_auto.git- 🔁 **Continuous Operation**: Runs in loop, sleeping outside market hours

cd desktop_auto

- ⚙️ **Flexible Scheduling**: Configurable start/stop times and intervals- Automated browser window detection

# Create virtual environment

python -m venv .venv- 📅 **Timestamp Logging**: All messages include date/time stamps



# Activate virtual environment- Dropdown selection for stock search  4. Volumeprofile (with extended 15s load time)

.venv\Scripts\activate

## 📋 Prerequisites

# Install dependencies

pip install -r requirements.txt- Automatic .bz suffix handling

```

- **Windows OS** (uses win32gui for window management)

### 2️⃣ Configuration

- **Python 3.8+**- Configurable wait delays- Organizes screenshots by symbol in separate folders- Updates symbol on the first chart (Trend analysis)

Create a `.env` file in the project root:

- **TradingView account** with 4 separate chart windows open

```bash

# Stock Symbols- **Perplexity API key** (optional, for AI analysis) - Get from [Perplexity](https://www.perplexity.ai/)

STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL

- **Gmail account** (optional, for email alerts with App Password)

# TradingView Windows

TRADINGVIEW_ENABLED=True### Perplexity AI Analysis- Uses Windows API for reliable window management

TRADINGVIEW_WINDOW1=trend analysis

TRADINGVIEW_WINDOW2=Smoothed Heiken Ashi Candles## 🔧 Installation

TRADINGVIEW_WINDOW3=volume layout

TRADINGVIEW_WINDOW4=volumeprofile- **Automated Screenshot Analysis**: AI analyzes all captured screenshots together



# Symbolik.com### 1. Clone the repository

SYMBOLIK_ENABLED=True

SYMBOLIK_WINDOW=workspace```bash- **Trend Change Detection**: Calculates probability (0-100%) of trend changes- Captures screenshots from all 4 chart layouts:- Python 3.8 or higher



# Perplexity AIgit clone https://github.com/mskpairprogrammer/desktop_auto.git

PERPLEXITY_ENABLED=True

PERPLEXITY_API_KEY=your_api_key_herecd desktop_auto- **Prior Analysis Comparison**: Compares with previous analysis to detect changes



# Email Alerts```

EMAIL_USER=your_email@gmail.com

EMAIL_PASSWORD=your_app_password- **Comprehensive Reports**: Generates detailed market analysis reports## Prerequisites

EMAIL_TO=recipient@email.com

EMAIL_ALERT_THRESHOLD=35### 2. Create and activate virtual environment



# Scheduling```bash- **Email Alerts**: Automatic notifications for significant trend changes

SCHEDULE_ENABLED=True

CAPTURE_START_TIME=09:30python -m venv .venv

CAPTURE_STOP_TIME=16:00

CAPTURE_TIMEZONE=US/Eastern.venv\Scripts\activate- **Confidence Levels**: very_high, high, medium, low confidence ratings  1. Trend analysis- VS Code with Python extension

CAPTURE_INTERVAL_SECONDS=3600

``````



### 3️⃣ Gmail App Password Setup- **Alert Levels**: critical, high, medium, low priority alerts



1. Go to [Google Account Security](https://myaccount.google.com/security)### 3. Install dependencies

2. Enable **2-Step Verification** (if not already enabled)

3. Navigate to **Security** → **App passwords**```bash- **Customizable Threshold**: Set minimum probability for email alerts (default 35%)- Windows OS (uses win32gui for window management)

4. Generate password for **Mail**

5. Copy 16-character password to `EMAIL_PASSWORD` in `.env`pip install -r requirements.txt



### 4️⃣ Run```



```bash

python main.py

```### 4. Configure environment variables### Market Hours Scheduling (NEW!)- Python 3.8+  2. Smoothed Heiken Ashi Candles



---Create a `.env` file with your settings:



## ⚙️ Configuration- **Automatic Market Hours Detection**: Only runs during configured trading hours



### 📊 Stock Symbols```bash

```bash

STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL# Required Settings- **Hourly Intervals**: Captures screenshots and analysis every hour (configurable)- TradingView account with 4 separate chart windows open

```

Comma-separated list of symbols to process.STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL



### 🪟 TradingView Windows- **Timezone Support**: Configurable timezone (default: US/Eastern for NYSE/NASDAQ)

```bash

TRADINGVIEW_ENABLED=True# TradingView Windows (customize based on your window titles)

TRADINGVIEW_WINDOW1=trend analysis        # Window 1 keyword

TRADINGVIEW_WINDOW2=Smoothed Heiken Ashi  # Window 2 keywordTRADINGVIEW_ENABLED=True- **Continuous Operation**: Runs in loop, sleeping outside market hours  3. Volume layout### Installation

TRADINGVIEW_WINDOW3=volume layout         # Window 3 keyword

TRADINGVIEW_WINDOW4=volumeprofile         # Window 4 keywordTRADINGVIEW_WINDOW1=trend analysis

```

Keywords to identify each TradingView window. Run `python list_windows.py` to see available windows.TRADINGVIEW_WINDOW2=Smoothed Heiken Ashi Candles- **Flexible Scheduling**: Configurable start/stop times and intervals



### ⏱️ Timing SettingsTRADINGVIEW_WINDOW3=volume layout

```bash

WINDOW_SETTLE_DELAY=3.0        # Wait after window focus (seconds)TRADINGVIEW_WINDOW4=volumeprofile## Setup

FOCUS_CLICK_DELAY=1.5          # Wait after clicking (seconds)

CHART_LOAD_DELAY_TAB1_3=5.0    # Chart load time for tabs 1-3

CHART_LOAD_DELAY_TAB4=15.0     # Extended load time for volumeprofile

SYMBOLIK_WAIT_DELAY=10.0       # Symbolik chart load time# Symbolik Settings## Prerequisites

```

Adjust if charts load slower on your system.SYMBOLIK_ENABLED=True



### 📸 Screenshot NamingSYMBOLIK_WINDOW=workspace  4. Volumeprofile

```bash

SCREENSHOT_DIR=screenshots

SCREENSHOT_NAME_TAB1={symbol}_luxoalgo.png

SCREENSHOT_NAME_TAB2={symbol}_heiken.png# Perplexity AI Analysis (optional)- **Windows OS** (uses win32gui for window management)

SCREENSHOT_NAME_TAB3={symbol}_volume_layout.png

SCREENSHOT_NAME_TAB4={symbol}_rvol.pngPERPLEXITY_ENABLED=True

SCREENSHOT_NAME_SYMBOLIK={symbol}_symbolik.png

```PERPLEXITY_API_KEY=your_perplexity_api_key_here- **Python 3.8+**1. Clone the repository:

Use `{symbol}` placeholder for dynamic naming.



### 🤖 Perplexity AI

```bash# Email Alerts (optional)- **TradingView account** with 4 separate chart windows open

PERPLEXITY_ENABLED=True

PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxEMAIL_USER=your_email@gmail.com

```

Get your API key from [Perplexity](https://www.perplexity.ai/).EMAIL_PASSWORD=your_app_password_here- **Perplexity API key** (optional, for AI analysis) - Get from [Perplexity](https://www.perplexity.ai/)   ```bash- Saves screenshots without timestamps (overwrites previous versions)1. Clone or download this project



### 📧 Email AlertsEMAIL_TO=recipient@email.com

```bash

EMAIL_USER=your_email@gmail.comSMTP_SERVER=smtp.gmail.com- **Gmail account** (optional, for email alerts with App Password)

EMAIL_PASSWORD=your_16_char_app_password

EMAIL_TO=recipient@email.comSMTP_PORT=587

SMTP_SERVER=smtp.gmail.com

SMTP_PORT=587EMAIL_ALERT_THRESHOLD=35   git clone https://github.com/mskpairprogrammer/desktop_auto.git

EMAIL_ALERT_THRESHOLD=35

```

Alert threshold is minimum probability (%) to trigger email.

# Scheduling Settings## Setup

### 📅 Scheduling

```bashSCHEDULE_ENABLED=True

SCHEDULE_ENABLED=True

CAPTURE_START_TIME=09:30       # Market open (HH:MM)CAPTURE_START_TIME=09:30   cd desktop_auto- Uses Windows API for reliable window management2. Open the project in VS Code

CAPTURE_STOP_TIME=16:00        # Market close (HH:MM)

CAPTURE_TIMEZONE=US/EasternCAPTURE_STOP_TIME=16:00

CAPTURE_INTERVAL_SECONDS=3600  # 1 hour

```CAPTURE_TIMEZONE=US/Eastern1. Clone the repository:



**Common intervals:**CAPTURE_INTERVAL_SECONDS=3600

- `3600` = 1 hour *(recommended)*

- `1800` = 30 minutes```   ```bash   ```

- `900` = 15 minutes

- `300` = 5 minutes



---### 5. Gmail App Password Setup (for Email Alerts)   git clone https://github.com/mskpairprogrammer/desktop_auto.git



## 🎯 Usage



### Scheduled Mode (Continuous)1. Go to your Google Account settings   cd desktop_auto3. Install dependencies:



```bash2. Navigate to Security → 2-Step Verification (enable if not already)

python main.py

```3. Navigate to Security → App passwords   ```



With `SCHEDULE_ENABLED=True`:4. Generate a new app password for "Mail"

1. ✅ Checks if within market hours (9:30 AM - 4:00 PM ET)

2. ✅ Captures screenshots from all windows5. Copy the 16-character password to `EMAIL_PASSWORD` in `.env`2. Create a virtual environment:

3. ✅ Performs AI analysis with Perplexity

4. ✅ Sends email alerts if threshold met

5. ✅ Waits for interval (e.g., 1 hour)

6. ✅ Repeats steps 1-5## 📊 TradingView Setup2. Create and activate virtual environment:

7. ✅ Outside market hours: sleeps and checks every 5 minutes



**Example output:**

```Open 4 separate TradingView windows (**not tabs!**) with these chart layouts:   ```bash   ```bash## Prerequisites   ```bash

[2025-10-26 09:30:15] 🕐 SCHEDULED MODE ENABLED

[2025-10-26 09:30:15] Market Hours: 09:30 - 16:00 US/Eastern

[2025-10-26 09:30:15] Interval: 3600s (60 minutes)

[2025-10-26 09:30:18] 🚀 RUN #1 - 2025-10-26 09:30:18 EDT1. **Trend Analysis** - Your main trend analysis chart with LuxAlgo indicators   python -m venv .venv

[2025-10-26 09:30:18] 📊 Processing 2 symbols: QBTS, SNAP

[2025-10-26 09:30:20] ✅ Found window: TradingView - trend analysis2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view

[2025-10-26 09:30:25] 📸 Taking screenshot for Tab 1...

[2025-10-26 09:30:45] 🤖 Starting Perplexity AI analysis for QBTS...3. **Volume Layout** - Volume-focused chart   .venv\Scripts\activate   python -m venv .venv

[2025-10-26 09:30:52] 🚨 HIGH ALERT: Strong bullish reversal detected

[2025-10-26 09:30:52] 📊 Trend Change Probability: 78%4. **Volume Profile** - Volume profile analysis

[2025-10-26 09:30:53] 📧 Email alert sent to user@email.com

[2025-10-26 09:31:30] ✅ Completed processing QBTS!   ```

```

The window titles must contain the keywords specified in your `.env` file for the automation to find them.

### Single Run Mode

   ```   pip install -r requirements.txt

Set `SCHEDULE_ENABLED=False` in `.env`:

```bash## 🎯 Usage

python main.py

```3. Install dependencies:

Runs once and exits.

### Scheduled Mode (Recommended)

### List Available Windows

   ```bash

```bash

python list_windows.pyRun continuously during market hours:

```

Shows all window titles for configuration.```bash   pip install -r requirements.txt



### Test Symbolik Automationpython main.py



```bash```   ```3. Activate the virtual environment:- Windows OS (uses win32gui for window management)   ```

python test_symbolik.py

```

Tests browser automation separately.

With `SCHEDULE_ENABLED=True`, the program will:

---

- ✅ Check if current time is within market hours (9:30 AM - 4:00 PM ET)

## 📊 TradingView Setup

- ✅ Run screenshot capture and AI analysis4. Configure environment variables in `.env`:   ```bash

Open **4 separate TradingView windows** (not tabs):

- ✅ Wait for the configured interval (default: 1 hour)

| Window | Purpose | Indicators |

|--------|---------|-----------|- ✅ Repeat during market hours   ```bash

| **1. Trend Analysis** | Main analysis chart | LuxAlgo Signals, Overlays, Price Action |

| **2. Heiken Ashi** | Smoothed candle view | Smoothed Heiken Ashi Candles |- ✅ Sleep and check every 5 minutes when outside market hours

| **3. Volume Layout** | Volume patterns | Volume analysis indicators |

| **4. Volume Profile** | Volume distribution | Volume profile chart |   # Required Settings   .venv\Scripts\activate- Python 3.8+4. Copy the environment template and configure:



**Important:** Window titles must contain the keywords specified in your `.env` file.**Example output:**



**Example Setup:**```   STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL

- Window 1 title: `TradingView - trend analysis - QBTS`

- Window 2 title: `TradingView - Smoothed Heiken Ashi Candles`[2025-10-26 09:30:15] 🕐 SCHEDULED MODE ENABLED

- Window 3 title: `TradingView - volume layout`

- Window 4 title: `TradingView - volumeprofile`[2025-10-26 09:30:15] Market Hours: 09:30 - 16:00 US/Eastern      ```



---[2025-10-26 09:30:15] Interval: 3600s (60 minutes)



## 🤖 AI Analysis[2025-10-26 09:30:18] 🚀 RUN #1 - 2025-10-26 09:30:18 EDT   # TradingView Windows (customize based on your window titles)



### How It Works[2025-10-26 09:30:18] 📊 Processing 2 symbols: QBTS, SNAP



1. **Screenshot Capture**: All 5 windows captured for each symbol```   TRADINGVIEW_ENABLED=True- TradingView account with 4 separate chart windows open   ```bash

2. **Base64 Encoding**: Images converted for API transmission

3. **AI Prompt Creation**:

   - Includes chart-specific context

   - References LuxAlgo documentation for Window 1### Single Run Mode   TRADINGVIEW_WINDOW1=trend analysis

   - Includes prior analysis for comparison

4. **Perplexity API Call**: Single request with all images

5. **Response Parsing**: Extracts analysis text and trend JSON

6. **Report Generation**: Saves to `combined_analysis_latest.txt`Set `SCHEDULE_ENABLED=False` in `.env` to run once and exit:   TRADINGVIEW_WINDOW2=Smoothed Heiken Ashi Candles4. Install dependencies:

7. **Email Alert**: Sends if probability ≥ threshold

```bash

### LuxAlgo Integration

python main.py   TRADINGVIEW_WINDOW3=volume layout

For **Trend Analysis** (Window 1), Perplexity uses:

- **Signals & Overlays**: [Documentation](https://docs.luxalgo.com/docs/algos/signals-overlays/signals)```

- **Price Action Concepts**: [Documentation](https://docs.luxalgo.com/docs/algos/price-action-concepts/introduction)

   TRADINGVIEW_WINDOW4=volumeprofile   ```bash   copy .env.example .env

This ensures accurate analysis based on LuxAlgo's methodology.

## 🔄 Workflow

### Analysis Report Structure

   

```

Combined Screenshot Analysis ReportFor each symbol in `STOCK_SYMBOLS`:

====================================

Analysis Date: 2025-10-26 09:30:52   # Symbolik Settings   pip install -r requirements.txt

Screenshots Analyzed: 5

### 1. TradingView Processing (if enabled)

Screenshot Sources:

- Trend Analysis: QBTS_luxoalgo.png- Switches to each of the 4 windows   SYMBOLIK_ENABLED=True

- Heiken Ashi: QBTS_heiken.png

- Volume Layout: QBTS_volume_layout.png- Clicks center of screen for focus

- Volume Profile: QBTS_rvol.png

- Workspace: QBTS_symbolik.png- Types the symbol   SYMBOLIK_WINDOW=workspace   ```## Setup   ```



Trend Change Analysis:- Presses Enter

📊 Trend Change Probability: 78%

🎯 Confidence Level: HIGH- Waits for chart to load (5s for Tabs 1-3, 15s for Tab 4)   

🚨 Alert Status: ALERT (HIGH)

📋 Summary: Strong bullish reversal signals detected- Takes screenshot and saves as `screenshots/SYMBOL/SYMBOL_tab#.png`



Combined Analysis Results:   # Perplexity AI Analysis (optional)

=========================================

### 2. Symbolik Processing (if enabled)

**MARKET OVERVIEW**

QBTS showing strong bullish momentum with price at $2.45...- Brings Symbolik browser window to front   PERPLEXITY_ENABLED=True



**KEY VISIBLE INDICATORS**- Clicks search dropdown

- LuxAlgo Signal: Strong Buy (confirmed)

- Price broke above resistance at $2.40- Types symbol with .bz suffix   PERPLEXITY_API_KEY=your_perplexity_api_key_here5. Create a `.env` file based on `.env.example`:   Then edit `.env` with your specific settings.

- Volume spike: 3x average

...- Waits for chart to load

```

- Takes screenshot and saves as `screenshots/SYMBOL/SYMBOL_symbolik.png`   

### Trend Change JSON



```json

{### 3. AI Analysis (if enabled)   # Email Alerts (optional)   ```bash

  "send_email": true,

  "alert_level": "high",- Encodes all screenshots to base64

  "trend_change_probability": 78,

  "confidence_level": "high",- Sends to Perplexity AI for analysis with LuxAlgo context   EMAIL_USER=your_email@gmail.com

  "summary": "Strong bullish reversal signals detected",

  "key_changes": [- Compares with prior analysis (if exists)

    "Price broke above resistance at $2.40",

    "LuxAlgo signals confirm strong buy",- Calculates trend change probability   EMAIL_PASSWORD=your_app_password_here   copy .env.example .env1. Clone the repository:

    "Volume spike 3x average confirms momentum"

  ],- Generates comprehensive analysis report

  "probability_reasoning": "Multiple indicators align with high confidence"

}- Saves to `screenshots/SYMBOL/combined_analysis_latest.txt`   EMAIL_TO=recipient@email.com

```

- Sends email alert if probability >= threshold

### Email Alert Levels

   SMTP_SERVER=smtp.gmail.com   ```

| Level | Probability | Icon | Action |

|-------|-------------|------|--------|### 4. Scheduled Loop

| **CRITICAL** | 81-100% | 🚨 | Immediate action recommended |

| **HIGH** | 61-80% | ⚠️ | Strong trend change signals |- If during market hours: waits for interval, then repeats   SMTP_PORT=587

| **MEDIUM** | 41-60% | 📊 | Mixed signals, monitor closely |

| **LOW** | 21-40% | 📈 | Minor changes detected |- If outside market hours: checks every 5 minutes



---   EMAIL_ALERT_THRESHOLD=35   ```bash### Configuration



## 📅 Scheduling## 📁 Screenshots Organization



### Market Hours Configuration   



```bashScreenshots are organized by symbol in separate folders:

SCHEDULE_ENABLED=True

CAPTURE_START_TIME=09:30       # NYSE open   # Scheduling Settings6. Edit `.env` and set your stock symbols:

CAPTURE_STOP_TIME=16:00        # NYSE close

CAPTURE_TIMEZONE=US/Eastern```

```

screenshots/   SCHEDULE_ENABLED=True

### Supported Timezones

├── QBTS/

- `US/Eastern` - NYSE/NASDAQ (New York)

- `US/Pacific` - PSX (Los Angeles)│   ├── QBTS_luxoalgo.png   CAPTURE_START_TIME=09:30   ```   git clone https://github.com/mskpairprogrammer/desktop_auto.git

- `Europe/London` - LSE (London)

- `Asia/Tokyo` - TSE (Tokyo)│   ├── QBTS_heiken.png

- `Asia/Hong_Kong` - HKEX (Hong Kong)

│   ├── QBTS_volume_layout.png   CAPTURE_STOP_TIME=16:00

Full list: [pytz timezones](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)

│   ├── QBTS_rvol.png

### Behavior

│   ├── QBTS_symbolik.png   CAPTURE_TIMEZONE=US/Eastern   STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL

**During Market Hours:**

- Executes capture and analysis│   └── combined_analysis_latest.txt

- Waits for `CAPTURE_INTERVAL_SECONDS`

- Repeats continuously├── SNAP/   CAPTURE_INTERVAL_SECONDS=3600



**Outside Market Hours:**│   ├── SNAP_luxoalgo.png

- Displays "Outside market hours" message

- Sleeps for 5 minutes│   ├── SNAP_heiken.png   ```   ```   cd desktop_autoThe project uses environment variables for configuration. Key settings in `.env`:

- Checks again

│   ├── SNAP_volume_layout.png

**Single Run:**

- Set `SCHEDULE_ENABLED=False`│   ├── SNAP_rvol.png

- Runs once and exits

│   ├── SNAP_symbolik.png

---

│   └── combined_analysis_latest.txt### Gmail App Password Setup (for Email Alerts)   You can add or remove symbols as needed, separated by commas.

## 🛠️ Troubleshooting

├── TSLA/

### ❌ Windows Not Found

└── AAPL/

**Symptoms:** `Window with 'X' not found`

```

**Solutions:**

1. ✅ Ensure all 4 TradingView windows are open1. Go to your Google Account settings   ```

2. ✅ Run `python list_windows.py` to see available windows

3. ✅ Update `.env` with exact window title keywords## 🤖 AI Analysis Reports

4. ✅ Check window titles contain configured keywords

2. Navigate to Security → 2-Step Verification (enable if not already)

### 📸 Blank Screenshots

The Perplexity AI generates detailed analysis reports including:

**Symptoms:** Screenshots are black or show wrong content

3. Navigate to Security → App passwords## TradingView Setup

**Solutions:**

1. ✅ Increase load delays in `.env`:### Report Structure

   ```bash

   CHART_LOAD_DELAY_TAB1_3=7.0  # Instead of 5.0- **Market Overview**: Current price, timeframe, overall market condition4. Generate a new app password for "Mail"

   CHART_LOAD_DELAY_TAB4=20.0   # Instead of 15.0

   ```- **Key Visible Indicators**: Moving averages, oscillators, volume data, support/resistance

2. ✅ Ensure windows are maximized

3. ✅ Check screen resolution matches click coordinates (1280, 800)- **LuxAlgo Analysis**: Signal quality, price action concepts, overlay indicators (for trend analysis chart)5. Copy the 16-character password to `EMAIL_PASSWORD` in `.env`- `APP_NAME`: Application name (default: "Desktop Auto")



### 🤖 AI Analysis Fails- **Critical Signals**: Most important actionable signals



**Error: 401 Unauthorized**- **Trading Decision**: Clear BUY/SELL/HOLD recommendation with rationale

- Invalid API key

- Solution: Check `PERPLEXITY_API_KEY` in `.env`- **Trend Change Evaluation**: Probability of trend change with confidence level



**Error: 429 Too Many Requests**## TradingView SetupOpen 4 separate TradingView windows with these chart layouts:

- Rate limit exceeded

- Solution: Reduce capture frequency or wait### LuxAlgo Integration



**Error: 500 Server Error**For the trend analysis chart, Perplexity uses:

- Perplexity service issue

- Solution: Wait and retry later- **LuxAlgo Signals & Overlays**: https://docs.luxalgo.com/docs/algos/signals-overlays/signals



**Module Not Found:**- **LuxAlgo Price Action Concepts**: https://docs.luxalgo.com/docs/algos/price-action-concepts/introductionOpen 4 separate TradingView windows (not tabs!) with these chart layouts:1. **Trend analysis** - Your main trend analysis chart2. Create a virtual environment:- `DEBUG`: Enable debug mode (true/false)

```bash

pip install openai

```

This ensures accurate analysis based on official LuxAlgo methodology.

### 📧 Email Not Sending



**Checklist:**

1. ✅ Verify `EMAIL_USER`, `EMAIL_PASSWORD`, `EMAIL_TO` are set### Trend Change Analysis Example1. **Trend analysis** - Your main trend analysis chart2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view

2. ✅ Use Gmail **App Password**, not regular password

3. ✅ Enable 2-Step Verification on Gmail account```json

4. ✅ Check firewall allows SMTP port 587

5. ✅ Check spam/junk folder{2. **Smoothed Heiken Ashi Candles** - Heiken Ashi candle view



**Test email configuration:**  "send_email": true,

```python

from perplexity_analysis import EmailAlertManager  "alert_level": "high",3. **Volume layout** - Volume-focused chart3. **Volume layout** - Volume-focused chart   ```bash- `AUTOMATION_DELAY`: Delay between automation actions in seconds

email = EmailAlertManager()

print(f"Email configured: {email.is_configured}")  "trend_change_probability": 75,

```

  "confidence_level": "high",4. **Volumeprofile** - Volume profile analysis

### ⏰ Scheduling Issues

  "summary": "Strong bullish reversal signals detected",

**"Outside market hours" during trading day:**

- Check `CAPTURE_TIMEZONE` matches your market  "key_changes": [4. **Volumeprofile** - Volume profile analysis

- Verify system time is correct

    "Price broke above resistance",

**Not running at expected times:**

- Verify `CAPTURE_START_TIME` format (HH:MM, 24-hour)    "Volume spike confirms momentum",The window titles must contain the keywords specified in your `.env` file for the automation to find them.

- Check `CAPTURE_STOP_TIME` is after start time

    "LuxAlgo signals show strong buy"

**pytz errors:**

```bash  ],   python -m venv .venv- `SCREENSHOT_DIR`: Directory for screenshot storage

pip install pytz

```  "probability_reasoning": "Multiple indicators align for uptrend"



### 📦 Package Installation Issues}## Usage



```bash```

# Reinstall all dependencies

pip uninstall -r requirements.txt -yThe window titles must contain these keywords for the automation to find them.

pip install -r requirements.txt

### Email Alert Levels

# Or specific packages

pip install pywin32- 🚨 **CRITICAL** (81%+ probability): Immediate action recommended### Scheduled Mode (Recommended)

pip install openai

pip install pytz- ⚠️ **HIGH** (61-80% probability): Strong trend change signals

```

- 📊 **MEDIUM** (41-60% probability): Mixed signals, monitor closely   ```- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

---

- 📈 **LOW** (21-40% probability): Minor changes detected

## 📁 Project Structure

Run continuously during market hours:

```

desktop_auto/## ⚙️ Configuration Reference

│

├── 📄 main.py                      # Main automation script```bash## Usage

├── 📄 perplexity_analysis.py       # AI analysis & email module

├── 📄 list_windows.py              # Window discovery utility### Scheduling Settings

├── 📄 test_symbolik.py             # Symbolik automation test

│```bashpython main.py

├── 📄 requirements.txt             # Python dependencies

├── 📄 .env                         # Configuration (gitignored)SCHEDULE_ENABLED=True              # Enable continuous scheduled mode

├── 📄 .env.example                 # Configuration template

├── 📄 .gitignore                   # Git ignore rulesCAPTURE_START_TIME=09:30           # Market open (24-hour format HH:MM)```

├── 📄 README.md                    # This file

│CAPTURE_STOP_TIME=16:00            # Market close (24-hour format HH:MM)

├── 📁 .venv/                       # Virtual environment

├── 📁 .vscode/                     # VS Code tasksCAPTURE_TIMEZONE=US/Eastern        # Timezone for market hours

├── 📁 .github/                     # GitHub config

│CAPTURE_INTERVAL_SECONDS=3600      # Run every hour (3600 = 1 hour)

└── 📁 screenshots/                 # Screenshot storage

    ├── 📁 QBTS/```With `SCHEDULE_ENABLED=True`, the program will:Run the automation script:

    │   ├── 📸 QBTS_luxoalgo.png

    │   ├── 📸 QBTS_heiken.png

    │   ├── 📸 QBTS_volume_layout.png

    │   ├── 📸 QBTS_rvol.png**Common intervals:**- Check if current time is within market hours (9:30 AM - 4:00 PM ET)

    │   ├── 📸 QBTS_symbolik.png

    │   └── 📄 combined_analysis_latest.txt- `3600` = 1 hour (recommended for market hours)

    ├── 📁 SNAP/

    ├── 📁 TSLA/- `1800` = 30 minutes- Run screenshot capture and AI analysis```bash3. Activate the virtual environment:## Usage Examples

    └── 📁 AAPL/

```- `900` = 15 minutes



---- `300` = 5 minutes- Wait for the configured interval (default: 1 hour)



## 💡 Examples



### Example 1: Hourly During Market Hours### Screenshot Settings- Repeat during market hourspython main.py



```bash```bash

# .env

SCHEDULE_ENABLED=TrueSCREENSHOT_DIR=screenshots- Sleep and check every 5 minutes when outside market hours

CAPTURE_START_TIME=09:30

CAPTURE_STOP_TIME=16:00SCREENSHOT_NAME_TAB1={symbol}_luxoalgo.png

CAPTURE_INTERVAL_SECONDS=3600

SCREENSHOT_NAME_TAB2={symbol}_heiken.png```   ```bash

# Run

python main.pySCREENSHOT_NAME_TAB3={symbol}_volume_layout.png

```

SCREENSHOT_NAME_TAB4={symbol}_rvol.png### Single Run Mode

**Result:** Runs at 9:30 AM, 10:30 AM, 11:30 AM, ..., 4:00 PM ET

SCREENSHOT_NAME_SYMBOLIK={symbol}_symbolik.png

### Example 2: Every 30 Minutes Extended Hours

```

```bash

# .env

CAPTURE_START_TIME=08:00

CAPTURE_STOP_TIME=18:00The `{symbol}` placeholder is automatically replaced with each stock symbol.Set `SCHEDULE_ENABLED=False` in `.env` to run once and exit:

CAPTURE_INTERVAL_SECONDS=1800



# Run

python main.py### Timing Settings```bashThe script will:   .venv\Scripts\activate### Simple Usage (Recommended)

```

```bash

**Result:** Runs every 30 minutes from 8:00 AM to 6:00 PM

WINDOW_SETTLE_DELAY=3.0        # Wait after bringing window to frontpython main.py

### Example 3: Single Run (On-Demand)

FOCUS_CLICK_DELAY=1.5          # Wait after clicking to focus

```bash

# .envCHART_LOAD_DELAY_TAB1_3=5.0    # Chart load time for tabs 1-3```1. Wait 3 seconds before starting

SCHEDULE_ENABLED=False

CHART_LOAD_DELAY_TAB4=15.0     # Extended load time for volumeprofile

# Run

python main.pySYMBOLIK_WAIT_DELAY=10.0       # Wait for Symbolik chart to load

```

```

**Result:** Runs once immediately and exits

## Workflow2. For each symbol in `STOCK_SYMBOLS`:   ``````bash

### Example 4: High-Frequency Monitoring

### Enable/Disable Features

```bash

# .env```bash

CAPTURE_START_TIME=09:30

CAPTURE_STOP_TIME=16:00TRADINGVIEW_ENABLED=True    # Toggle TradingView automation

CAPTURE_INTERVAL_SECONDS=300   # 5 minutes

EMAIL_ALERT_THRESHOLD=50       # More selective alertsSYMBOLIK_ENABLED=True       # Toggle Symbolik automationFor each symbol in `STOCK_SYMBOLS`:   - Switch to each of the 4 windows



# RunPERPLEXITY_ENABLED=True     # Toggle AI analysis

python main.py

```SCHEDULE_ENABLED=True       # Toggle scheduled continuous mode



**Result:** Runs every 5 minutes, only sends alerts for ≥50% probability```



---1. **TradingView Processing** (if enabled):   - Click center of screen for focus# Run the simple automation



## 📦 Dependencies## 🔧 Troubleshooting



| Package | Version | Purpose |   - Switches to each of the 4 windows

|---------|---------|---------|

| `pyautogui` | ≥0.9.54 | Desktop automation, screenshots |### Windows not found

| `pillow` | ≥10.0.0 | Image processing |

| `pywin32` | ≥306 | Windows API integration |- ✅ Ensure all 4 TradingView windows are open   - Clicks center of screen for focus   - Type the symbol

| `python-dotenv` | ≥1.0.0 | Environment configuration |

| `pynput` | latest | Mouse/keyboard input |- ✅ Check that window titles contain the keywords from `.env`

| `openai` | ≥1.0.0 | Perplexity API client |

| `pytz` | ≥2023.3 | Timezone support |- ✅ Run `python list_windows.py` to see all available windows   - Types the symbol



**Install all:**- ✅ Update `TRADINGVIEW_WINDOW1-4` with exact window title keywords

```bash

pip install -r requirements.txt   - Presses Enter   - Press Enter4. Install dependencies:python main.py

```

### Screenshots are blank or wrong timing

---

- ✅ Adjust wait times in `.env` if charts load slower   - Waits for chart to load (5s for Tabs 1-3, 15s for Tab 4)

## 📝 License

- ✅ Increase `CHART_LOAD_DELAY_TAB1_3` or `CHART_LOAD_DELAY_TAB4` values

This project is for **personal use** only.

- ✅ Ensure windows are maximized   - Takes screenshot and saves as `screenshots/SYMBOL/SYMBOL_tab#.png`   - Wait for chart to load (5s for Tabs 1-3, 15s for Tab 4)

---

- ✅ Check screen resolution (default click position is 1280x800)

## 🤝 Contributing



Contributions are welcome!

### AI Analysis fails

1. Fork the repository

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)- ✅ Verify `PERPLEXITY_API_KEY` is set correctly2. **Symbolik Processing** (if enabled):   - Take screenshot and save as `screenshots/SYMBOL/SYMBOL_tab#.png`   ```bash```

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)

4. Push to the branch (`git push origin feature/AmazingFeature`)- ✅ Check that `openai` package is installed: `pip install openai`

5. Open a Pull Request

- ✅ Ensure screenshots exist before analysis runs   - Brings Symbolik browser window to front

---

- ✅ Check API key has sufficient credits

## 📅 Changelog

- ✅ Review error messages in console with timestamps   - Clicks search dropdown3. Process all symbols sequentially

### v2.2.0 - LuxAlgo & Logging Enhancement (2025-10-26)

- ✅ **LuxAlgo Integration**: Added documentation references for AI analysis

- ✅ **Timestamp Logging**: All messages now include [YYYY-MM-DD HH:MM:SS]

- ✅ **Enhanced Analysis**: Official LuxAlgo methodology for trend charts### Email alerts not sending   - Types symbol with .bz suffix

- ✅ **Better Debugging**: Date/time stamped logs for troubleshooting

- ✅ Verify all email settings in `.env` are correct

### v2.1.0 - Market Hours Scheduling (2025-10-26)

- ✅ **Scheduled Mode**: Continuous operation during market hours- ✅ For Gmail, use App Password (not regular password)   - Waits for chart to load   pip install -r requirements.txt

- ✅ **Timezone Support**: Configurable timezone with pytz

- ✅ **Flexible Intervals**: Hourly, 30min, 15min, or custom- ✅ Ensure SMTP port 587 is not blocked by firewall

- ✅ **Auto Sleep**: Automatically sleeps outside market hours

- ✅ **Run Tracking**: Displays run count and next execution time- ✅ Check spam folder for alerts   - Takes screenshot and saves as `screenshots/SYMBOL/SYMBOL_symbolik.png`



### v2.0.0 - AI Analysis Integration (2025-10-25)- ✅ Verify 2-Step Verification is enabled for Gmail account

- ✅ **Perplexity AI**: Automated screenshot analysis

- ✅ **Trend Detection**: 0-100% probability scoring## Screenshots Location

- ✅ **Email Alerts**: Configurable threshold notifications

- ✅ **Analysis Reports**: Comprehensive market analysis### Perplexity API errors

- ✅ **Historical Comparison**: Compares with prior analysis

- **401 Unauthorized**: Invalid API key3. **AI Analysis** (if enabled):

### v1.1.0 - Symbolik Integration (2025-10-24)

- ✅ **Browser Automation**: Symbolik.com screenshot capture- **429 Too Many Requests**: Rate limit exceeded, wait and retry

- ✅ **Dropdown Search**: Automated stock symbol search

- ✅ **Auto .bz Suffix**: Automatic suffix handling- **500 Server Error**: Perplexity service issue, try again later   - Encodes all screenshots to base64   ```### What the simple automation does:



### v1.0.0 - Initial Release (2025-10-23)

- ✅ **Multi-Window**: 4 TradingView window automation

- ✅ **Multi-Symbol**: Process multiple stocks### Scheduling issues   - Sends to Perplexity AI for analysis

- ✅ **Screenshot Capture**: Organized storage

- ✅ **Parameterized Config**: .env configuration- **"Outside market hours" during trading day**: Check `CAPTURE_TIMEZONE` matches your market



---- **Not running at expected times**: Verify `CAPTURE_START_TIME` and `CAPTURE_STOP_TIME` are correct   - Compares with prior analysis (if exists)Screenshots are organized by symbol in separate folders under `screenshots/`:



## 🔗 Links & Resources- **pytz errors**: Install with `pip install pytz`



- **GitHub Repository**: [mskpairprogrammer/desktop_auto](https://github.com/mskpairprogrammer/desktop_auto)- **Running continuously even outside hours**: Set `SCHEDULE_ENABLED=True` in `.env`   - Calculates trend change probability

- **LuxAlgo Signals**: [Documentation](https://docs.luxalgo.com/docs/algos/signals-overlays/signals)

- **LuxAlgo Price Action**: [Documentation](https://docs.luxalgo.com/docs/algos/price-action-concepts/introduction)

- **Perplexity AI**: [Website](https://www.perplexity.ai/)

- **TradingView**: [Platform](https://www.tradingview.com/)## 📦 Project Structure   - Generates comprehensive analysis report1. 🔄 **Alt+Tab to TradingView** (brings app to foreground)

- **Symbolik**: [Platform](https://symbolik.com/)



---

```   - Saves to `screenshots/SYMBOL/combined_analysis_latest.txt`

## 📞 Support

desktop_auto/

Need help? Here's how to get support:

├── main.py                    # Main automation orchestrator with scheduling   - Sends email alert if probability >= thresholdExample with `STOCK_SYMBOLS=QBTS,SNAP,TSLA,AAPL`:

1. **Check Documentation**: Review this README thoroughly

2. **Troubleshooting Section**: See [Troubleshooting](#-troubleshooting)├── perplexity_analysis.py     # AI analysis module with LuxAlgo integration

3. **GitHub Issues**: [Open an issue](https://github.com/mskpairprogrammer/desktop_auto/issues)

4. **Example Logs**: Include timestamp logs when reporting issues├── list_windows.py            # Utility to list available windows



**When reporting issues, include:**├── test_symbolik.py           # Symbolik automation test

- Python version (`python --version`)

- Operating system version├── requirements.txt           # Python dependencies4. **Scheduled Loop**:```5. Create a `.env` file based on `.env.example`:2. �️ **Click center of screen** (activates chart area)

- Relevant `.env` settings (redact sensitive data)

- Console output with timestamps├── .env                       # Configuration (not in git)

- Screenshots if applicable

├── .env.example               # Example configuration template   - If during market hours: waits for interval, then repeats

---

├── .gitignore                 # Git ignore rules

## ⭐ Star This Repository

├── README.md                  # This file   - If outside market hours: checks every 5 minutesscreenshots/

If you find this project useful, please consider giving it a star on GitHub!

└── screenshots/               # Output directory

[![GitHub stars](https://img.shields.io/github/stars/mskpairprogrammer/desktop_auto.svg?style=social&label=Star)](https://github.com/mskpairprogrammer/desktop_auto)

    ├── QBTS/

---

    ├── SNAP/

**Made with ❤️ for automated stock trading analysis**

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
