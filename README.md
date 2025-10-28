# 📊 Desktop Auto - AI-Powered TradingView & Symbolik Automation

> **Professional multi-chart screenshot automation with comprehensive AI analysis, chart-specific indicator recognition, and intelligent email alerts for stock trading workflows**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Personal%20Use-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

---

## 🎯 Overview

**Desktop Auto** is a sophisticated Python-based desktop automation tool that captures screenshots from multiple TradingView chart windows and Symbolik.com, then performs advanced AI-powered analysis using multiple AI providers with chart-specific indicator recognition. The system understands each chart's unique technical indicators and provides comprehensive multi-indicator analysis with intelligent email alerts.

### Key Capabilities

- **📸 Multi-Chart Screenshot Automation**: Automated capture from 4 TradingView windows + Symbolik.com
- **🤖 Multi-Provider AI Analysis**: Support for Claude AI and Perplexity AI with sequential analysis
- **📊 Chart-Specific Intelligence**: Understands different indicators per chart layout
- **📧 Intelligent Email Alerts**: Automated notifications for trend changes and signals
- **⏰ Market Hours Scheduling**: Runs automatically during market hours with configurable intervals
- **🔄 Multi-Symbol Processing**: Handles multiple stock symbols sequentially
- **📁 Organized Storage**: Screenshots and reports organized by symbol and timestamp

## 📋 Table of Contents

- [Features](#-features)
- [AI Provider Configuration](#-ai-provider-configuration)
- [Installation](#-installation)
- [Configuration](#%EF%B8%8F-configuration)
- [Usage](#-usage)
- [Chart Layouts](#-chart-layouts)
- [AI Analysis](#-ai-analysis)
- [Email Alerts](#-email-alerts)
- [Troubleshooting](#-troubleshooting)
- [File Structure](#-file-structure)

## ✨ Features

### Screenshot Automation
- **Smart Window Detection**: Windows API for reliable window management
- **Multi-Symbol Support**: Process multiple stock symbols sequentially  
- **Organized Storage**: Screenshots saved by symbol in dedicated folders
- **TradingView Integration**: Automated interaction with 4 different chart layouts
- **Symbolik.com Integration**: Browser automation with dropdown search

### AI-Powered Analysis
- **Multi-Provider Support**: Claude AI and Perplexity AI with independent control
- **Sequential Analysis**: When both providers enabled, runs analyses in sequence
- **Consensus Reporting**: Combined reports with agreement metrics when using multiple providers
- **Chart-Specific Intelligence**: AI understands different indicators per chart layout
- **Trend Change Detection**: 0-100% probability scoring for trend changes
- **Historical Comparison**: Compares with previous analysis for change detection

### Automation Features
- **Market Hours Scheduling**: Configurable start/stop times with timezone support
- **Configurable Intervals**: Run every 15min, 30min, 1hour, or custom intervals
- **Multi-Symbol Processing**: Handles lists of stock symbols from text file
- **Error Handling**: Robust error handling with detailed logging
- **Background Operation**: Can run continuously with scheduling

## 🤖 AI Provider Configuration

The system supports multiple AI providers that can be used independently or together for comprehensive analysis. It also supports Google AI Studio (Gemini) for consensus logic and advanced HTML report generation.

### Supported AI Providers

#### 1. Perplexity AI
- **Model**: sonar
- **Strengths**: Real-time web data access, financial market awareness
- **API Endpoint**: https://api.perplexity.ai
- **Required Package**: openai

#### 2. Claude AI (Anthropic)
- **Model**: claude-sonnet-4-5-20250929
- **Strengths**: Advanced reasoning, detailed analysis, safety-focused
- **API Endpoint**: Anthropic's official API
- **Required Package**: anthropic

#### 3. Google AI Studio (Gemini)
- **Model**: Gemini 2.0 Flash (Google AI Studio)
- **Strengths**: Advanced consensus logic, HTML report generation, robust summarization
- **API Endpoint**: Google AI Studio API
- **Required Package**: google-generativeai

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
- Each provider analyzes the screenshots independently
- Results are combined into a multi-provider consensus report
- Average probability scores are calculated
- Alert levels are determined by the highest-confidence provider
- Email alerts are sent only once (from the consensus logic)

When Google AI Studio is enabled (with Claude and/or Perplexity):
- Google AI Studio generates the consolidated trading decision and consensus summary
- The HTML report is generated with Google AI's consensus at the top, followed by Claude and Perplexity sections
- Email alerts are sent only from the Google AI consensus logic (not from individual providers)

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
- Windows 10/11
- Python 3.8+
- TradingView account with specific chart layouts
- AI provider API keys (Perplexity and/or Claude)

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
- **LuxAlgo Signals & Overlays**: Professional signal quality analysis
- **Trend Direction Indicators**: Overlay indicators showing trend strength
- **Signal Confirmations**: Multi-indicator convergence validation

### Window 2: Smoothed Heiken Ashi Candles
- **Smoothed Heiken Ashi**: Trend-following candles that smooth price noise
- **AlgoAlpha HEMA Trend**: Hybrid Exponential Moving Average
- **Trend identification with reduced noise**

### Window 3: Volume Layout
- **Volume Profile**: Market Profile-style volume analysis
- **Volume indicators**: Volume-based momentum and trend analysis
- **Support/Resistance from volume**: Key levels based on volume

### Window 4: Volume Profile & RVOL
- **Volume Profile**: Detailed volume-at-price analysis
- **RVOL (Relative Volume)**: Current volume vs historical average
- **Institutional activity indicators**

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
- **Trend Direction**: Current trend analysis per chart
- **Signal Quality**: Strength and reliability of signals
- **Change Detection**: Comparison with previous analysis
- **Probability Scores**: 0-100% confidence in trend changes
- **Alert Levels**: Low/Medium/High priority classifications
- **Provider Consensus**: Agreement between multiple AI providers (when enabled)

## 📧 Email Alerts

### Configuration
```properties
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password  # Use app-specific password for Gmail
EMAIL_TO=recipient@gmail.com
EMAIL_ALERT_THRESHOLD=35  # Minimum probability for email alerts
```

### Alert Types
- **High Priority**: Trend change probability > 70%
- **Medium Priority**: Trend change probability 35-70%
- **Low Priority**: Trend change probability < 35%

### Email Content
- Complete AI analysis text
- Trend change probabilities
- Chart-specific insights
- Timestamp and symbol information
- Provider information (when using multiple providers)

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

---

**Note**: This tool is designed for personal trading analysis. Always conduct your own research and risk management when making trading decisions.