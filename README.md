# Desktop Auto Project

A Python project for desktop automation tasks.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- VS Code with Python extension

### Installation

1. Clone or download this project
2. Open the project in VS Code
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment template and configure:
   ```bash
   copy .env.example .env
   ```
   Then edit `.env` with your specific settings.

### Configuration

The project uses environment variables for configuration. Key settings in `.env`:

- `APP_NAME`: Application name (default: "Desktop Auto")
- `DEBUG`: Enable debug mode (true/false)
- `AUTOMATION_DELAY`: Delay between automation actions in seconds
- `SCREENSHOT_DIR`: Directory for screenshot storage
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

## Usage Examples

### Simple Usage (Recommended)
```bash
# Run the simple automation
python main.py
```

### What the simple automation does:
1. 🔄 **Alt+Tab to TradingView** (brings app to foreground)
2. �️ **Click center of screen** (activates chart area)
3. ⌨️ **Type "QBTS"** (enters the stock symbol)
4. ✅ **Press Enter** (confirms the symbol)
5. 📸 **Take screenshot** (captures the chart)
6. 💾 **Save to folder**: `screenshots/QBTS/QBTS_timestamp.png`

### Alternative Scripts
```bash
# Manual control version (you focus TradingView yourself)
python manual_automator.py

# Test different click positions
python manual_automator.py
# Choose option 2 for position testing
```

### TradingView Automation Features

The project includes automated TradingView desktop app interaction:

1. **Brings TradingView to foreground** (if possible)
2. **Changes stock symbol** using Ctrl+K shortcut
3. **Takes screenshot** of the current chart
4. **Saves screenshot** in organized folders: `screenshots/SYMBOL/`

### Prerequisites for TradingView Automation

- TradingView desktop application must be running
- The app can be in the background (Alt+Tab will bring it forward)
- Chart should accept direct typing (most TradingView setups do)
- Simple and reliable - no complex shortcuts needed

### Safety Features

- **Failsafe**: Move mouse to top-left corner to stop automation
- **Simple workflow**: Alt+Tab → Click → Type → Enter → Screenshot
- **Error handling**: Clear error messages and graceful failures

## Project Structure

```
desktop_auto/
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .github/
    └── copilot-instructions.md  # Copilot configuration
```

## Development

This project is set up for development in VS Code with Python support. The recommended extensions will be suggested when you open the project.

## License

This project is for personal use.