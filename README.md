# 📊 Desktop Auto - AI-Powered Multi-Window Trading Analysis

> **Professional multi-chart screenshot automation with multi-provider AI analysis, chart-specific indicator recognition, and intelligent email alerts**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4.svg)](https://www.microsoft.com/windows)

## Overview

**Desktop Auto** is a sophisticated Python-based desktop automation system that:
- 📸 Captures screenshots from **4 simultaneous TradingView windows** + **Symbolik.com**
- 🤖 Performs **AI analysis with 3 independent providers** (Perplexity, Claude, Google AI)
- 📊 Generates **consensus trading decisions** with confidence scoring
- 📧 Sends **intelligent email alerts** for significant trade signals
- 📄 Creates **comprehensive HTML reports** with multi-indicator analysis

## Features

### Desktop Automation
- ✅ Concurrent capture from 4 TradingView chart windows
  - Trend Analysis (LuxAlgo indicators)
  - Smoothed Heiken Ashi Candles
  - Volume Layout
  - Volume Profile / RVOL
- ✅ Symbolik.com automation for additional analysis
- ✅ Smart window focus and error recovery
- ✅ Configurable capture scheduling (market hours, intervals)

### Multi-Provider AI Analysis
- **Perplexity AI** — Real-time technical analysis with financial context
- **Claude AI (Anthropic)** — Advanced reasoning and pattern recognition
- **Google AI (Gemini)** — Consensus logic and HTML report generation

Each provider analyzes the same screenshots independently, enabling:
- Robust failure handling (if one provider fails, others continue)
- Consensus scoring (bullish/bearish/neutral from each provider)
- Comparison of different analytical perspectives

### Intelligent Decision Making
- Consolidates analyses from all 3 providers
- Generates confidence-weighted trading decisions
- Triggers email alerts only when consensus is strong
- Supports per-provider enable/disable for flexibility

### Output & Reporting
- HTML reports with per-provider analysis
- Combined trading decision summary
- Signal strength and confidence metrics
- Email notifications with analysis details

## Quick Start

### 1. Setup Environment
```bash
# Clone repository
git clone https://github.com/mskpairprogrammer/desktop_auto.git
cd desktop_auto

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure `.env`
```bash
# Copy template (if exists)
copy .env.example .env

# Edit .env with your API keys and settings
# See Configuration section below
```

### 3. Add Stock Symbols
Edit `stock_symbols.txt` (one symbol per line):
```
SNAP
QBTS
NVDA
```

### 4. Run
```bash
python main.py
```

### 5. Schedule (Optional)
Set in `.env`:
```env
SCHEDULE_ENABLED=true
CAPTURE_START_TIME=09:30
CAPTURE_STOP_TIME=16:00
CAPTURE_TIMEZONE=US/Eastern
CAPTURE_INTERVAL_SECONDS=3600
```

## Configuration

### API Keys (`.env`)
```env
# Perplexity
PERPLEXITY_API_KEY=pplx-xxxxx
PERPLEXITY_MODEL=sonar

# Claude (Anthropic)
ANTHROPIC_API_KEY=sk-ant-xxxxx
CLAUDE_MODEL=claude-sonnet-4-5-20250929

# Google AI (Gemini)
GOOGLE_AI_API_KEY=AIzaSy-xxxxx
GOOGLE_AI_MODEL=gemini-3-pro-preview
```

### Provider Enable/Disable
```env
PERPLEXITY_ENABLED=True        # Enable Perplexity analysis
CLAUDE_ENABLED=True             # Enable Claude analysis
GOOGLE_AI_CHART_ENABLED=True    # Enable Google AI chart analysis
GOOGLE_AI_CONSOLIDATION_ENABLED=True  # Enable Google AI consensus decision
```

### Email Alerts
```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=app-specific-password
EMAIL_TO=recipient@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ALERT_THRESHOLD=35  # Confidence threshold (0-100)
```

### TradingView Settings
```env
TRADINGVIEW_ENABLED=True
TRADINGVIEW_WINDOW1=trend analysis
TRADINGVIEW_WINDOW2=Smoothed Heiken Ashi Candles
TRADINGVIEW_WINDOW3=volume layout
TRADINGVIEW_WINDOW4=volumeprofile
WINDOW_SETTLE_DELAY=3.0
CHART_LOAD_DELAY_TAB1_3=7.0
CHART_LOAD_DELAY_TAB4=20.0
```

### Symbolik.com Settings
```env
SYMBOLIK_ENABLED=True
SYMBOLIK_URL=https://symbolik.com
SYMBOLIK_WINDOW=workspace
SYMBOLIK_WAIT_DELAY=10.0
```

## Project Structure

```
desktop_auto/
├── main.py                  # Main orchestrator script
├── ai_analysis.py           # Multi-provider AI system (1460+ lines)
├── trading_analysis.py      # Perplexity analyzer & email logic
├── config.py               # Configuration constants
├── utils.py                # Shared utilities
├── build_executable.py     # PyInstaller build script
├── requirements.txt        # Python dependencies
├── stock_symbols.txt       # List of symbols to analyze
├── .env                    # Environment configuration (DO NOT COMMIT)
├── .env.example            # Template for .env
├── test_individual_providers.py  # Test each provider
├── screenshots/            # Output directory (organized by symbol)
├── build/                  # PyInstaller build artifacts
├── dist/                   # Compiled executable output
├── MULTI_AGENT_ARCHITECTURE.md  # Future architecture design
└── README.md              # This file
```

## Core Modules

### `main.py`
- Windows automation orchestrator
- Screenshot capture from 4 TradingView windows + Symbolik
- Stock symbol iteration
- Market hours scheduling
- Keyboard automation (Alt+Tab, window management)

### `ai_analysis.py` (1460+ lines)
**Multi-Provider AI System with Consensus Logic**

Classes:
- `BaseAnalyzer` — Abstract base for all providers
- `PerplexityAnalyzer` — OpenAI-compatible interface for Perplexity API
- `ClaudeAnalyzer` — Anthropic API integration
- `GoogleAIAnalyzer` — Google Generative AI (Gemini) integration
- `TradingAnalyzer` — Main orchestrator for all AI providers

Features:
- Parallel or sequential provider execution
- Automatic retry with exponential backoff
- Rate limit handling
- Standardized prompt across all providers (150+ lines of technical indicators)
- Email decision parsing from Google AI consensus
- HTML report generation
- Per-provider enable/disable flags

### `trading_analysis.py`
- `PerplexityAnalyzer` — Legacy Perplexity integration
- `EmailAlertManager` — SMTP email sending with error handling
- Detailed technical prompt (~350 lines) for indicator analysis

### `config.py`
- Screen coordinates for window clicks
- File paths and naming conventions
- Timing defaults for window settling
- API configuration structure

### `utils.py`
- `encode_image_to_base64()` — Convert images to Gemini-compatible format
- `ensure_directory_exists()` — Safe directory creation
- `get_base_dir()` — Script/executable directory detection
- Image validation and logging utilities

## Testing

### Run Individual Providers
```bash
python test_individual_providers.py
```

Tests each provider independently:
- Checks for screenshot files
- Validates API keys
- Shows response preview
- Reports pass/fail for each provider

### Build Executable
```bash
python build_executable.py
```

Creates standalone `.exe` using PyInstaller (62.8 MB):
- No Python installation required
- All dependencies bundled
- Requires `.env` in same directory as `.exe`

## Architecture

### Current: Sequential Processing
1. UI Automation → Capture screenshots (4 windows sequentially)
2. AI Analysis → Each provider analyzes sequentially
3. Decision → Consolidate and generate report
4. Email → Send alert if threshold met

**Processing time: ~130-180 seconds per symbol**

### Future: Multi-Agent (Agentic) System
See `MULTI_AGENT_ARCHITECTURE.md` for proposed parallel architecture:
- 4 UI agents capture windows concurrently
- 3 AI agents analyze in parallel
- Message bus for inter-agent communication
- Dynamic agent lifecycle management

**Estimated processing time: ~40-55 seconds (3x improvement)**

## Email Alerts

Email alerts are triggered only by **Google AI consensus logic** (not individual providers):

1. **Threshold**: Email sent when confidence > `EMAIL_ALERT_THRESHOLD` (default: 35%)
2. **Format**: HTML email with:
   - Trading decision (BULLISH/BEARISH/NEUTRAL)
   - Confidence score
   - Key technical factors from all 3 providers
   - Link to HTML report
3. **Authentication**: Requires Gmail app-specific password (not regular password)

### Gmail Setup
1. Enable 2-factor authentication
2. Create app-specific password: https://myaccount.google.com/apppasswords
3. Use app password in `.env`:
   ```env
   EMAIL_PASSWORD=your-16-char-app-password
   ```

## Troubleshooting

### Common Issues

**"No module named 'ai_analysis'"**
- Ensure you're in the correct directory
- Virtual environment activated: `.venv\Scripts\activate`

**Email not sending**
- Verify `EMAIL_PASSWORD` is app-specific password (not account password)
- Check `GOOGLE_AI_CONSOLIDATION_ENABLED=True` in `.env`
- Review email threshold (`EMAIL_ALERT_THRESHOLD`)

**Screenshots not captured**
- Ensure TradingView windows are focused and visible
- Check window titles match `.env` settings
- Verify `TRADINGVIEW_ENABLED=True`

**API rate limiting**
- Add delays in `.env`: `WINDOW_SETTLE_DELAY`, `CHART_LOAD_DELAY_TAB1_3`
- Providers have built-in exponential backoff

**AI provider failures**
- Check API keys are valid and have sufficient quota
- Verify `.env` contains correct model names
- Other providers continue even if one fails

## Requirements

- **OS**: Windows 10/11
- **Python**: 3.8+
- **Internet**: Required for API calls
- **Display**: 1920x1080 or higher (for coordinate accuracy)
- **RAM**: 2GB+ (depends on provider concurrency)

## Dependencies

See `requirements.txt`:
```
python-dotenv
pyautogui
pillow
anthropic
openai
google-generativeai
pytz
pywin32
```

## Performance Metrics

| Operation | Time |
|-----------|------|
| Screenshot capture (4 windows) | 40-60s (sequential) |
| AI analysis (3 providers) | 90-120s (sequential) |
| HTML report generation | 2-5s |
| Total per symbol | 130-180s |

**With multi-agent parallelization: 40-55s (proposed)**

## Security

- ⚠️ **DO NOT commit `.env` file** (contains API keys)
- `.env` is in `.gitignore`
- Use environment-specific copies in production
- Rotate API keys regularly
- Gmail app-specific passwords are safer than account passwords

## Building Executable

```bash
python build_executable.py
```

Creates `dist/DesktopAuto.exe`:
- Self-contained (~62.8 MB)
- Copy `.env` to same directory as `.exe`
- Run: `DesktopAuto.exe`

**Note**: First run extracts dependencies (~5-10 seconds)

## Roadmap

### Completed ✅
- Multi-provider AI analysis (Perplexity, Claude, Google AI)
- Consensus decision logic
- Email alerts from Google AI
- HTML report generation
- Provider enable/disable flags
- Test script for individual providers

### In Development 🔄
- Multi-agent agentic architecture (parallel processing)
- Provider-specific performance metrics
- Advanced signal filtering

### Future 🔮
- Web dashboard for monitoring
- Historical signal tracking
- ML-based confidence calibration
- Support for crypto and forex
- Mobile notifications

## License

Personal use. See LICENSE file.

## Support

For issues, questions, or feature requests:
1. Check troubleshooting section
2. Review code comments in main modules
3. Examine `.env.example` for configuration options
4. Check git commit history for recent changes
