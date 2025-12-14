# Desktop Auto - Multi-Provider AI Trading Analysis

Automated desktop trading analysis system with 5 AI providers for comprehensive chart analysis and intelligent email alerts.

## Features

- **Multi-Window Screenshot Capture**: Captures 4 TradingView chart windows + Symbolik.com
- **5 AI Providers**: Perplexity, Claude, Google AI, Grok, and OpenAI analyze charts independently
- **Consensus Decision**: Google AI consolidates all provider analyses into final recommendation
- **Email Alerts**: Automatic alerts when significant trading signals detected
- **HTML Reports**: Comprehensive multi-provider analysis reports

## Quick Start

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys in .env (copy from .env.example)
copy .env.example .env

# Add stock symbols to stock_symbols.txt
echo NVDA > stock_symbols.txt

# Run
python main.py
```

## Configuration (.env)

### API Keys
```env
PERPLEXITY_API_KEY=pplx-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
GOOGLE_AI_API_KEY=AIzaSy-xxxxx
GROK_API_KEY=xai-xxxxx
OPENAI_API_KEY=sk-xxxxx
```

### AI Models
```env
PERPLEXITY_MODEL=sonar-pro
CLAUDE_MODEL=claude-sonnet-4-20250514
GOOGLE_AI_MODEL=gemini-3-pro-preview
GROK_MODEL=grok-2-vision-1212
OPENAI_MODEL=gpt-4o
```

### Enable/Disable Providers
```env
PERPLEXITY_ENABLED=True
CLAUDE_ENABLED=True
GOOGLE_AI_CHART_ENABLED=True
GOOGLE_AI_CONSOLIDATION_ENABLED=True
GROK_ENABLED=True
OPENAI_ENABLED=True
```

### Email Alerts
```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=app-specific-password
EMAIL_TO=recipient@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## Project Structure

```
desktop_auto/
├── main.py              # Main orchestrator - window automation & scheduling
├── ai_analysis.py       # Multi-provider AI analysis system
├── trading_analysis.py  # Trading-specific analysis & email alerts
├── config.py            # Configuration constants
├── utils.py             # Shared utility functions
├── build_executable.py  # PyInstaller build script
├── requirements.txt     # Python dependencies
├── stock_symbols.txt    # Stock symbols to analyze (one per line)
├── .env                 # Environment configuration (not in git)
└── .env.example         # Template for .env
```

## AI Providers

| Provider | Model | Purpose |
|----------|-------|---------|
| Perplexity | sonar-pro | Technical analysis with real-time context |
| Claude | claude-sonnet-4-20250514 | Advanced pattern recognition |
| Google AI | gemini-3-pro-preview | Consensus consolidation & reports |
| Grok | grok-2-vision-1212 | Vision-based chart analysis |
| OpenAI | gpt-4o | Multi-modal chart interpretation |

## TradingView Windows

Configure 4 TradingView chart windows with these tab names:
1. `trend analysis` - LuxAlgo indicators
2. `Smoothed Heiken Ashi Candles` - Heiken Ashi analysis
3. `volume layout` - Volume flow analysis
4. `UT Bot -Lorentzian` - UT Bot alerts with Lorentzian ML classification

## Output

- **Screenshots**: `../data/screenshots/{SYMBOL}/`
- **Analysis**: `combined_analysis_latest.txt` per symbol
- **HTML Report**: `multi_provider_analysis.html` per symbol
- **Email**: Sent when consensus triggers alert threshold

## Requirements

- Windows 10/11
- Python 3.8+
- TradingView Desktop (4 windows configured)
- Microsoft Edge (for Symbolik.com)
- API keys for enabled providers

## Build Executable

```bash
python build_executable.py
```

Creates standalone `dist/DesktopAuto.exe`. Place `.env` in same directory as executable.

## License

Personal use only.
