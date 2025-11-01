# Quick Reference Guide for Code Updates

## New Files Added

### `utils.py` - Shared Utilities
```python
from utils import (
    encode_image_to_base64,      # Convert image to base64 data URI
    sanitize_for_logging,        # Redact sensitive data from logs
    get_base_dir,                # Get app directory (script or EXE)
    ensure_directory_exists,     # Safely create directories
    SCREENSHOTS_DIR,             # "screenshots"
    COMBINED_ANALYSIS_FILENAME,  # "combined_analysis_latest.txt"
    MULTI_PROVIDER_HTML_FILENAME # "multi_provider_analysis.html"
)
```

### `config.py` - Configuration Constants
```python
from config import (
    Coordinates,  # Screen click positions
    Defaults,     # Default timing values
    Paths,        # File/directory names
    Windows,      # Window title keywords
    Screenshots,  # Screenshot filename patterns
    API,          # API configuration
    SMTP          # Email configuration
)

# Usage examples:
pyautogui.click(Coordinates.TRADINGVIEW_FOCUS_X, Coordinates.TRADINGVIEW_FOCUS_Y)
delay = Defaults.WINDOW_SETTLE_DELAY
log_file = Paths.LOG_FILE
window = Windows.TRADINGVIEW_TREND_ANALYSIS
```

## Key Changes by File

### `build_executable.py`
- ⚠️ **SECURITY**: No longer bundles .env file
- Users MUST manually copy .env to dist/ folder

### `ai_analysis.py`
- Uses `utils.encode_image_to_base64()` instead of local copy
- Uses `utils.get_base_dir()` instead of inline function
- Uses `utils.ensure_directory_exists()` instead of `os.makedirs()`
- Improved retry logic with better error handling
- Organized imports (stdlib → local → third-party)

### `trading_analysis.py`
- Uses `utils.encode_image_to_base64()` instead of local copy
- Uses `utils.ensure_directory_exists()` instead of `os.makedirs()`
- SMTP uses context manager (`with` statement)
- Better exception handling (SMTPAuthenticationError, SMTPException)
- Organized imports

### `main.py`
- All functions have type hints now
- Uses `config.Coordinates.*` for screen positions
- Uses `config.Paths.*` for file names
- Better error handling in Symbolik screen matching
- Organized imports
- Fixed duplicate `timedelta` import

## Environment Variables (New)

Add these optional variables to your `.env`:

```bash
# Screen matching confidence for Symbolik (0.0-1.0)
SYMBOLIK_MATCH_CONFIDENCE=0.8

# Additional refresh wait if screen is blank (seconds)
SYMBOLIK_REFRESH_WAIT=5.0
```

## Migration Checklist

### For Development
- [x] All Python files compile without errors
- [ ] Test running `python main.py` locally
- [ ] Verify imports work correctly
- [ ] Test email functionality
- [ ] Test screenshot capture

### For Production/EXE
- [ ] Build new executable: `python build_executable.py`
- [ ] Copy `.env` file to `dist/` folder (REQUIRED!)
- [ ] Test executable runs without .env bundled
- [ ] Verify all functionality works from EXE
- [ ] Update deployment documentation

## Common Import Patterns

### Old (Before):
```python
import base64
import os
from datetime import datetime

# Later in code:
with open(image_path, "rb") as f:
    base64_image = base64.b64encode(f.read()).decode("utf-8")
```

### New (After):
```python
import os
from datetime import datetime
from utils import encode_image_to_base64

# Later in code:
image_data_uri = encode_image_to_base64(image_path)
```

## Testing Commands

```bash
# Syntax check all files
python -m py_compile main.py ai_analysis.py trading_analysis.py utils.py config.py

# Run main script
python main.py

# Build executable
python build_executable.py

# Don't forget to copy .env!
copy .env dist\.env
```

## Error Messages to Watch For

### ❌ "ModuleNotFoundError: No module named 'utils'"
**Fix**: Ensure `utils.py` is in the same directory as other Python files

### ❌ "ModuleNotFoundError: No module named 'config'"
**Fix**: Ensure `config.py` is in the same directory as other Python files

### ❌ ".env file not found" (when running EXE)
**Fix**: Copy `.env` file to the same directory as `DesktopAuto.exe`

### ❌ "AttributeError: module 'config' has no attribute 'Coordinates'"
**Fix**: Ensure you're importing the class, not the module: `from config import Coordinates`

## Performance Notes

- No runtime performance impact from changes
- Type hints are compile-time only
- Configuration constants loaded once at import
- SMTP context manager may be slightly faster

## Security Improvements

✅ API keys no longer in executable
✅ SMTP connections properly closed
✅ Framework for log sanitization ready
✅ Better error messages (less sensitive data exposure)

## What Wasn't Changed

These files work fine as-is:
- `test_symbolik.py`
- `record_clicks.py`
- `list_windows.py`
- `create_symbolik_reference.py`
- `build.bat`
- `requirements.txt`
- `stock_symbols.txt`
- `.env` (structure unchanged)

## Getting Help

If you encounter issues:
1. Check `desktop_auto.log` for detailed errors
2. Verify all imports are correct
3. Ensure `.env` file is in the right location
4. Check Python version compatibility (3.8+)
5. Review `CODE_REVIEW_FIXES.md` for detailed changes
