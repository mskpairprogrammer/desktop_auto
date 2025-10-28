# Desktop Auto

Desktop Auto is a Python-based automation tool for multi-window TradingView and Symbolik.com screenshot capture, advanced AI-powered trading analysis, and intelligent email alerts.

## Features
- Automated screenshot capture from multiple TradingView and Symbolik.com windows
- Multi-provider AI analysis: Claude (Anthropic), Perplexity (OpenAI-compatible), and Google AI Studio (Gemini)
- Consensus logic and HTML report generation using Google AI Studio
- Intelligent email alerts for significant trend changes (sent only from Google AI consensus)
- Organized output by symbol, with modern HTML reports
- Configurable scheduling, symbol lists, and chart-specific intelligence

## AI Providers
- **Claude (Anthropic):** Advanced reasoning, detailed analysis
- **Perplexity (OpenAI-compatible):** Real-time web data, financial awareness
- **Google AI Studio (Gemini):** Consensus logic, HTML report generation, robust summarization

## How It Works
1. Captures screenshots from all configured chart windows
2. Runs AI analysis with enabled providers (Claude, Perplexity)
3. Google AI Studio (if enabled) generates a consolidated trading decision and HTML report
4. Only the Google AI consensus logic triggers email alerts for significant trend changes
5. All output is saved as a single HTML file per symbol

## Configuration
- Edit `.env` for provider API keys, enable flags, email settings, and scheduling
- List symbols to analyze in `stock_symbols.txt`
- See `requirements.txt` for dependencies

## Usage
```bash
python main.py
```
- To run on a schedule, set `SCHEDULE_ENABLED=true` in `.env`
- To build an executable: `python build_executable.py`

## File Structure
- `main.py` — Main automation script
- `ai_analysis.py` — Multi-provider AI and consensus logic
- `trading_analysis.py` — Core analysis and email alert logic
- `screenshots/` — Output folders by symbol
- `.env` — Configuration

## Notes
- Email alerts are only sent from the Google AI consensus logic (not from Claude or Perplexity individually)
- The HTML report includes Google AI consensus at the top, followed by Claude and Perplexity sections
- Requires Python 3.8+ and Windows

---
For more details, see code comments and `.env.example`.
# 📊 Desktop Auto - AI-Powered TradingView & Symbolik Automation

> **Professional multi-chart screenshot automation with comprehensive AI analysis, chart-specific indicator recognition, and intelligent email alerts for stock trading workflows**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Personal%20Use-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)


## 🎯 Overview

**Desktop Auto** is a sophisticated Python-based desktop automation tool that captures screenshots from multiple TradingView chart windows and Symbolik.com, then performs advanced AI-powered analysis using multiple AI providers with chart-specific indicator recognition. The system understands each chart's unique technical indicators and provides comprehensive multi-indicator analysis with intelligent email alerts.

### Key Capabilities


## 📋 Table of Contents


## ✨ Features

### Screenshot Automation

### AI-Powered Analysis

### Automation Features

## 🤖 AI Provider Configuration

The system supports multiple AI providers that can be used independently or together for comprehensive analysis. It also supports Google AI Studio (Gemini) for consensus logic and advanced HTML report generation.

### Supported AI Providers

#### 1. Perplexity AI

#### 2. Claude AI (Anthropic)

#### 3. Google AI Studio (Gemini)

### Configuration Options

#### Option 1: Single Provider
Enable only one AI provider:

```properties
# Use only Perplexity
PERPLEXITY_ENABLED=True
CLAUDE_ENABLED=False
PERPLEXITY_API_KEY=pplx-your-api-key-here

# OR use only Claude
PERPLEXITY_ENABLED=False
CLAUDE_ENABLED=True
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

#### Option 2: Multiple Providers (Sequential Analysis & Consensus)
Enable two or more providers for comprehensive analysis and consensus:

```properties
# Use both providers for comprehensive analysis
PERPLEXITY_ENABLED=True
CLAUDE_ENABLED=True
PERPLEXITY_API_KEY=pplx-your-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```


When both Claude and Perplexity are enabled:

When Google AI Studio is enabled (with Claude and/or Perplexity):

#### Option 3: No AI Analysis
Disable all AI analysis (screenshots only):

```properties
PERPLEXITY_ENABLED=False
CLAUDE_ENABLED=False
```

### Configuration Examples

**Scenario 1: Both Providers Enabled (Multi-Provider Analysis)**
```properties
CLAUDE_ENABLED=True
PERPLEXITY_ENABLED=True
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
PERPLEXITY_API_KEY=pplx-your-api-key-here
```
**Result**: Both providers analyze screenshots sequentially. A combined consensus report is generated.

**Scenario 2: Claude Only**
```properties
CLAUDE_ENABLED=True
PERPLEXITY_ENABLED=False
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```
**Result**: Only Claude analyzes screenshots.

**Scenario 3: Perplexity Only**
```properties
CLAUDE_ENABLED=False
PERPLEXITY_ENABLED=True
PERPLEXITY_API_KEY=pplx-your-api-key-here
```
**Result**: Only Perplexity analyzes screenshots.

## 🚀 Installation

### Prerequisites

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/desktop_auto.git
cd desktop_auto
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install AI Provider Packages
```bash
# For Perplexity AI
pip install openai

# For Claude AI  
pip install anthropic
```

### Step 5: Configure Environment
1. Copy `.env.example` to `.env`
2. Configure your settings (see Configuration section)
3. Add your API keys

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```properties
# AI Provider Settings
CLAUDE_ENABLED=True
PERPLEXITY_ENABLED=True

# API Keys
PERPLEXITY_API_KEY=pplx-your-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Desktop Automation Settings
AUTOMATION_DELAY=1.0
SCREENSHOT_DIR=screenshots
TRADINGVIEW_ENABLED=True
SYMBOLIK_ENABLED=True

# Chart Loading Delays
CHART_LOAD_DELAY_TAB1_3=5.0
CHART_LOAD_DELAY_TAB4=15.0

# Email Alert Settings (optional)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_TO=recipient@gmail.com
EMAIL_ALERT_THRESHOLD=35

# Scheduling Settings
CAPTURE_START_TIME=09:30
CAPTURE_STOP_TIME=16:00
CAPTURE_TIMEZONE=US/Eastern
CAPTURE_INTERVAL_SECONDS=3600
SCHEDULE_ENABLED=false
```

### Stock Symbols Configuration

Edit `stock_symbols.txt` to specify which symbols to analyze:
```
AAPL
TSLA
NVDA
SPY
```

## 📱 Usage

### Run Once
```bash
python main.py
```

### Run with Scheduling
1. Set `SCHEDULE_ENABLED=True` in `.env`
2. Run: `python main.py`
3. The system will run continuously during market hours

### Build Executable
```bash
python build_executable.py
```

## 📊 Chart Layouts

The system captures screenshots from 4 different TradingView chart layouts:

### Window 1: Trend Analysis (LuxAlgo)

### Window 2: Smoothed Heiken Ashi Candles

### Window 3: Volume Layout

### Window 4: Volume Profile & RVOL

## 🤖 AI Analysis

### Analysis Process

1. **Screenshot Capture**: System captures screenshots from all configured windows
2. **AI Processing**: Enabled AI providers (Claude, Perplexity) analyze the screenshots
3. **Consensus & HTML Generation**: Google AI Studio (if enabled) generates a consolidated trading decision and creates a modern HTML report
4. **Chart Recognition**: AI identifies specific indicators and chart types
5. **Trend Analysis**: Probability scoring for trend changes (0-100%)
6. **Report Generation**: Comprehensive HTML analysis reports with consensus and provider breakdowns
7. **Email Notifications**: Automated alerts for significant changes (sent only from Google AI consensus logic)

### Multi-Provider Analysis


When multiple AI providers are enabled:

1. **Sequential Processing**: Each provider (Claude, Perplexity) analyzes independently
2. **Individual Reports**: Separate analysis from each provider
3. **Consensus Building**: Google AI Studio (if enabled) generates a consolidated trading decision and consensus summary
4. **Probability Averaging**: Average trend change probabilities
5. **Alert Aggregation**: Highest confidence alerts are prioritized
6. **HTML Output**: The report is generated as a single HTML file per symbol, with Google AI consensus at the top, followed by Claude and Perplexity
7. **Email Alerts**: Only the Google AI consensus logic triggers email alerts (not individual providers)

### Analysis Reports

Reports include:

## 📧 Email Alerts

### Configuration
```properties
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password  # Use app-specific password for Gmail
EMAIL_TO=recipient@gmail.com
EMAIL_ALERT_THRESHOLD=35  # Minimum probability for email alerts
```

### Alert Types

### Email Content

## 🔧 Troubleshooting

### Common Issues

#### AI Analysis Fails
1. **Check API Keys**: Ensure valid API keys in `.env`
2. **Check Provider Flags**: Verify `CLAUDE_ENABLED` and `PERPLEXITY_ENABLED` settings
3. **Install Packages**: Run `pip install openai anthropic`
4. **Check Internet**: Ensure stable internet connection

#### Screenshot Issues
1. **Window Titles**: Update window title keywords in `.env`
2. **Chart Loading**: Increase delay settings for slow charts
3. **Window Focus**: Ensure TradingView windows are properly arranged

#### Email Issues
1. **App Passwords**: Use app-specific passwords for Gmail
2. **SMTP Settings**: Verify SMTP server and port settings
3. **Firewall**: Check firewall allows SMTP connections

### Testing

Test individual components:
```bash
# Test Symbolik automation
python test_symbolik.py

# Test main system
python main.py
```

## 📁 File Structure

```
desktop_auto/
├── main.py                    # Main automation script
├── ai_analysis.py            # Multi-provider AI analysis
├── trading_analysis.py       # Core analysis logic
├── build_executable.py       # Build script for executable
├── test_symbolik.py          # Symbolik automation test
├── requirements.txt          # Python dependencies
├── stock_symbols.txt         # List of symbols to process
├── .env                      # Environment configuration
├── screenshots/              # Screenshot storage
│   ├── AAPL/                # Symbol-specific folders
│   └── TSLA/
├── build/                    # Build artifacts
└── .github/
    └── copilot-instructions.md
```

## 📄 License

This project is for personal use only. See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is a personal automation project. Contributions, issues, and feature requests are welcome!


**Note**: This tool is designed for personal trading analysis. Always conduct your own research and risk management when making trading decisions.