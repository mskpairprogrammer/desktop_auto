# AI Provider Configuration Guide

This document explains how to configure AI providers for analysis in the Desktop Auto project.

## Supported AI Providers

### 1. Perplexity AI
- **Model**: sonar
- **Strengths**: Real-time web data access, financial market awareness
- **API Endpoint**: https://api.perplexity.ai
- **Required Package**: openai
- **Environment Variables**:
  - `PERPLEXITY_API_KEY`: Your Perplexity API key
  - `PERPLEXITY_ENABLED`: Set to `True` to enable this provider

### 2. Claude AI (Anthropic)
- **Model**: claude-sonnet-4-5-20250929 (or latest available)
- **Strengths**: Advanced reasoning, detailed analysis, safety-focused
- **API Endpoint**: Anthropic's official API
- **Required Package**: anthropic
- **Environment Variables**:
  - `ANTHROPIC_API_KEY`: Your Claude API key
  - `CLAUDE_ENABLED`: Set to `True` to enable this provider

**Note**: Check [Anthropic's documentation](https://docs.anthropic.com/claude/docs/models-overview) for the latest available model names.

## Configuration Options

### Option 1: Single Provider
Enable only one AI provider by setting one to `True` and the other to `False`:

```properties
# Use only Perplexity
PERPLEXITY_ENABLED=True
CLAUDE_ENABLED=False

# OR use only Claude
PERPLEXITY_ENABLED=False
CLAUDE_ENABLED=True
```

### Option 2: Multiple Providers (Sequential Analysis)
Enable both providers to run analyses in sequence and generate a consensus report:

```properties
# Use both providers for comprehensive analysis
PERPLEXITY_ENABLED=True
CLAUDE_ENABLED=True
```

When both providers are enabled:
- Each provider analyzes the screenshots independently
- Results are combined into a multi-provider consensus report
- Average probability scores are calculated
- Alert levels are determined by the highest-confidence provider
- Email alerts are sent only once (from the first provider to avoid spam)

### Legacy Configuration
For backward compatibility, the `AI_PROVIDER` setting is still supported but deprecated:

```properties
# Deprecated - use individual enable flags instead
AI_PROVIDER=claude
```

### Enable AI Analysis

AI analysis must be enabled to use any provider:

```properties
# Enable AI analysis
AI_ANALYSIS_ENABLED=True
```

### API Keys Configuration

You need to provide API keys for the providers you want to use:

#### Perplexity AI
```properties
PERPLEXITY_API_KEY=pplx-your-api-key-here
PERPLEXITY_ENABLED=True
```

#### Claude AI
```properties
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
CLAUDE_ENABLED=True
```

## Installation

### Perplexity AI (Default)
```bash
pip install openai
```

### Claude AI
```bash
pip install anthropic
```

Or install both:
```bash
pip install -r requirements.txt
```

## Testing Your Configuration

Test your configuration by running the main script or checking the logs:

```bash
python main.py
```

This will show you:
- Current AI provider configuration
- Available providers and their initialization status  
- API key validation results
- Any configuration issues in the logs

## Switching Between Providers

1. **Change the AI_PROVIDER setting** in your `.env` file
2. **Ensure the required API key is configured**
3. **Restart the application** to apply changes

Example:
```properties
# Switch to Claude
AI_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-your-claude-key-here

# Switch to Perplexity  
AI_PROVIDER=perplexity
PERPLEXITY_API_KEY=pplx-your-perplexity-key-here
```

## Automatic Fallback

The system includes automatic fallback logic:
- If Claude is selected but not available → falls back to Perplexity
- If no provider is specified → defaults to Perplexity
- If an API call fails → logs error and continues with available provider

## API Usage Notes

### Perplexity AI
- Uses OpenAI-compatible interface
- Good for real-time market data analysis
- Includes web search capabilities
- Cost-effective for high-volume usage

### Claude AI  
- Advanced reasoning capabilities
- Better at complex pattern recognition
- More detailed explanations
- Higher accuracy for nuanced analysis
- More expensive per token

## Troubleshooting

### Common Issues

1. **"Import anthropic could not be resolved"**
   - Solution: `pip install anthropic`

2. **"API key is required"**
   - Check your `.env` file has the correct API key variable
   - Ensure the key starts with the correct prefix (pplx- or sk-ant-)

3. **"TradingAnalyzer failed to initialize"**
   - Check the test script output for specific errors
   - Verify both packages are installed: `pip list | grep -E "(openai|anthropic)"`

4. **Analysis fails with authentication error**
   - Verify your API key is valid and has sufficient credits
   - Check the API key has the necessary permissions

### Debug Mode

To see detailed provider selection logs, check the main application output:
```
🤖 Using Perplexity AI for analysis
# or
🤖 Using Claude AI for analysis
```

## Performance Comparison

| Feature | Perplexity | Claude |
|---------|------------|--------|
| Speed | Fast | Moderate |
| Cost | Lower | Higher |
| Web Access | Yes | No |
| Reasoning | Good | Excellent |
| Market Data | Real-time | Training cutoff |
| Analysis Detail | Concise | Comprehensive |

## Best Practices

1. **Start with Perplexity** for initial testing and development
2. **Switch to Claude** for more detailed analysis when needed
3. **Monitor API costs** especially with Claude
4. **Test both providers** with your specific use cases
5. **Keep API keys secure** and rotate them regularly

## Example Usage in Code

The switching is automatic based on configuration, but you can also test providers programmatically:

```python
from ai_analysis import TradingAnalyzer

# Use configured provider
analyzer = TradingAnalyzer()

# Force specific provider
analyzer = TradingAnalyzer('claude')
analyzer = TradingAnalyzer('perplexity')
```