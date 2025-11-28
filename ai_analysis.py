"""
AI API integration module for screenshot analysis with email alerts
Supports both Perplexity and Claude APIs
"""
# Standard library imports
import logging
import os
import random
import time
from datetime import datetime
from typing import Optional, Dict, Any

# Local imports
from utils import (
    encode_image_to_base64, 
    ensure_directory_exists, 
    get_base_dir,
    COMBINED_ANALYSIS_FILENAME,
    MULTI_PROVIDER_HTML_FILENAME
)

# Third-party imports with availability checks
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    print("Warning: openai package not installed. Please install it with: pip install openai")
    OpenAI = None
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    print("Warning: google-generativeai package not installed. Please install it with: pip install google-generativeai")
    genai = None
    GOOGLE_AI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    print("Warning: anthropic package not installed. Please install it with: pip install anthropic")
    anthropic = None
    ANTHROPIC_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAnalyzer:
    """Base class for AI analysis providers"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize base analyzer"""
        self.api_key = api_key
    
    def encode_image_to_base64(self, image_path: str) -> str:
        """
        Encode an image file to base64 string (delegates to shared utility)
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image as data URI
        """
        return encode_image_to_base64(image_path)
    
    def analyze_screenshots(self, messages: list) -> str:
        """Abstract method to be implemented by specific providers"""
        raise NotImplementedError("Must be implemented by specific analyzer")


class PerplexityAnalyzer(BaseAnalyzer):
    """Class to handle screenshot analysis using Perplexity API via OpenAI-compatible interface"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Perplexity analyzer
        
        Args:
            api_key: Perplexity API key. If None, will try to get from environment variable
        """
        if not OPENAI_AVAILABLE or OpenAI is None:
            raise ImportError("openai package is required. Install with: pip install openai")
        
        super().__init__(api_key)
        
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        
        if not self.api_key:
            raise ValueError("Perplexity API key is required. Set PERPLEXITY_API_KEY environment variable or pass api_key parameter")
        
        # Initialize the OpenAI client with Perplexity's endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.perplexity.ai"
        )
    
    def analyze_screenshots(self, messages: list) -> str:
        """Analyze screenshots using Perplexity API"""
        try:
            response = self.client.chat.completions.create(
                model="sonar",
                messages=messages,
                max_tokens=4000,
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Perplexity API error: {e}")
            raise


class ClaudeAnalyzer(BaseAnalyzer):
    """Class to handle screenshot analysis using Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Claude analyzer
        
        Args:
            api_key: Claude API key. If None, will try to get from environment variable
        """
        if not ANTHROPIC_AVAILABLE or anthropic is None:
            raise ImportError("anthropic package is required. Install with: pip install anthropic")
        
        super().__init__(api_key)
        
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        
        if not self.api_key:
            raise ValueError("Claude API key is required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter")
        
        # Initialize the Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def analyze_screenshots(self, messages: list) -> str:
        """Analyze screenshots using Claude API"""
        try:
            # Convert OpenAI-style messages to Claude format
            claude_messages = []
            system_message = None
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                elif msg["role"] == "user":
                    content = []
                    if isinstance(msg["content"], list):
                        for item in msg["content"]:
                            if item["type"] == "text":
                                content.append({"type": "text", "text": item["text"]})
                            elif item["type"] == "image_url":
                                # Extract base64 from data URI
                                image_data = item["image_url"]["url"]
                                if image_data.startswith("data:"):
                                    media_type, base64_data = image_data.split(",", 1)
                                    content.append({
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": media_type.split(":")[1].split(";")[0],
                                            "data": base64_data
                                        }
                                    })
                    else:
                        content = [{"type": "text", "text": msg["content"]}]
                    
                    claude_messages.append({"role": "user", "content": content})
            
            # Prepare the request parameters
            request_params = {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "temperature": 0.2,
                "messages": claude_messages
            }
            
            # Add system message if present
            if system_message:
                request_params["system"] = system_message
            
            response = self.client.messages.create(**request_params)
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise


class GoogleAIAnalyzer(BaseAnalyzer):
    """Class to handle consolidated decision analysis using Google AI Studio (Gemini)"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Google AI analyzer
        
        Args:
            api_key: Google AI API key. If None, will try to get from environment variable
        """
        if not GOOGLE_AI_AVAILABLE or genai is None:
            raise ImportError("google-generativeai package is required. Install with: pip install google-generativeai")
        
        super().__init__(api_key)
        
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv('GOOGLE_AI_API_KEY')
        
        if not self.api_key:
            raise ValueError("Google AI API key is required. Set GOOGLE_AI_API_KEY environment variable or pass api_key parameter")
        
        # Configure the API key
        genai.configure(api_key=self.api_key)
        
        # Initialize the model (using Gemini 3 Pro Preview - latest preview model)
        self.model = genai.GenerativeModel('gemini-3-pro-preview')
        
        logger.info("Google AI analyzer initialized successfully")
    
    def _call_with_backoff(self, content, max_attempts=5, base_delay=1.0):
        """Call Google AI with exponential backoff retry for rate limiting"""
        last_exception = None
        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(f"Google AI attempt {attempt}/{max_attempts}")
                
                # Handle both list and string content
                if isinstance(content, list):
                    resp = self.model.generate_content(content)
                else:
                    resp = self.model.generate_content(content)
                
                # Extract text from response
                text = getattr(resp, 'text', None)
                if text:
                    return text
                
                # Some responses may embed content differently
                if isinstance(resp, dict) and 'content' in resp:
                    return resp['content']
                
                logger.error("Empty response from Google AI (no text/content)")
                raise RuntimeError("Empty response from Google AI")
                
            except Exception as e:
                last_exception = e
                msg = str(e).lower()
                
                # Determine if this is a retryable error (rate limit / resource exhausted)
                is_retryable = any(keyword in msg for keyword in [
                    '429', 'resource exhausted', 'rate limit', 'quota', 
                    'ratelimit', 'too many requests'
                ])
                
                if is_retryable and attempt < max_attempts:
                    # Retry with exponential backoff + jitter
                    sleep_time = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1)
                    logger.warning(
                        f"Rate limit error (attempt {attempt}/{max_attempts}): {e}. "
                        f"Retrying in {sleep_time:.1f}s..."
                    )
                    time.sleep(sleep_time)
                else:
                    # Non-retryable error or max attempts reached
                    logger.error(f"Google AI error (attempt {attempt}/{max_attempts}): {e}")
                    if attempt == max_attempts:
                        break
        
        # All attempts failed
        logger.error(f"Google AI failed after {max_attempts} attempts: {last_exception}")
        return None
    
    def analyze_screenshots(self, messages: list) -> str:
        """
        Analyze chart screenshots using Google AI
        
        Args:
            messages: List of message dicts with 'type' and 'text'/'image_url' keys
            
        Returns:
            Analysis text from Google AI
        """
        try:
            import base64
            
            # For Gemini, we need to use genai.upload_file for files or pass inline data
            # Build content list with text and images
            content_parts = []
            
            for msg in messages:
                if msg.get('type') == 'text':
                    content_parts.append(msg['text'])
                elif msg.get('type') == 'image_url':
                    # Extract base64 from data URL if present
                    image_url = msg.get('image_url', {})
                    if isinstance(image_url, dict):
                        url = image_url.get('url', '')
                    else:
                        url = image_url
                    
                    if url.startswith('data:image'):
                        # Extract base64 data
                        try:
                            header, data = url.split(',', 1)
                            
                            # Determine media type from header
                            if 'png' in header:
                                media_type = 'image/png'
                            elif 'jpeg' in header or 'jpg' in header:
                                media_type = 'image/jpeg'
                            else:
                                media_type = 'image/jpeg'
                            
                            # Create inline data part - Gemini expects direct base64
                            image_part = {
                                "mime_type": media_type,
                                "data": data  # Keep as base64 string
                            }
                            content_parts.append(image_part)
                        except Exception as e:
                            logger.warning(f"Failed to process image data URL: {e}")
                            continue
            
            if not content_parts:
                return "No content to analyze"
            
            # Call Google AI with backoff retry
            response = self._call_with_backoff(content_parts)
            return response
            
        except Exception as e:
            logger.error(f"Google AI chart analysis error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_consolidated_decision(self, perplexity_analysis: str, claude_analysis: str, stock_symbol: str = "UNKNOWN", output_dir: str = None, screenshot_data: dict = None) -> str:
        """
        Generate a consolidated trading decision based on Perplexity and Claude analyses
        
        Args:
            perplexity_analysis: Full text analysis from Perplexity
            claude_analysis: Full text analysis from Claude
            stock_symbol: Stock symbol being analyzed
            output_dir: Directory for loading prior analysis
            screenshot_data: Screenshot data for loading prior analysis
            
        Returns:
            Consolidated trading decision text
        """
        try:
            # Load prior analysis for comparison (Google AI will handle this)
            prior_analysis = None
            if output_dir and screenshot_data:
                # Use the trading analyzer to load prior analysis
                from trading_analysis import PerplexityAnalyzer
                temp_analyzer = PerplexityAnalyzer()
                valid_screenshots = {k: v for k, v in screenshot_data.items() if v and os.path.exists(v)}
                if valid_screenshots:
                    prior_analysis = temp_analyzer._load_prior_analysis(output_dir, valid_screenshots, stock_symbol)
            
            # Create prompt for consolidated decision with prior analysis context
            prior_context = ""
            if prior_analysis:
                prior_context = f"""
PRIOR ANALYSIS FOR COMPARISON:
{prior_analysis[:1000]}...

TREND CHANGE EVALUATION REQUIRED:
Compare the current analyses above with the prior analysis to evaluate if there are significant changes or trend shifts.
"""
            else:
                prior_context = """
INITIAL ANALYSIS:
This is the first analysis for this symbol, so focus on current state evaluation.
"""
            
            prompt = f"""
You are an expert financial analyst tasked with creating a consolidated trading decision based on analyses from two different AI providers.

STOCK SYMBOL: {stock_symbol}

PERPLEXITY ANALYSIS:
{perplexity_analysis}

CLAUDE ANALYSIS:
{claude_analysis}

{prior_context}

Based on these two comprehensive analyses, generate a consolidated trading decision with the following format:

==================================================
CONSOLIDATED TRADING DECISION FOR {stock_symbol}
==================================================

TRADING DECISION: [BUY/SELL/HOLD]
Consensus Assessment: [Describe agreement/disagreement between providers]
Overall Confidence: [Provide a confidence percentage 0-100%]

TREND CHANGE EVALUATION:
[Synthesize the trend change probability from both analyses]
[Provide consolidated probability assessment]
[Explain key factors driving the trend evaluation]

CRITICAL FACTORS:
- [List 3-5 most important technical factors from both analyses]
- [Highlight any conflicting signals between providers]
- [Note volume, momentum, and support/resistance levels]

RISK ASSESSMENT:
- Upside Potential: [Based on resistance levels and bullish signals]
- Downside Risk: [Based on support levels and bearish signals]
- Stop Loss Recommendation: [If applicable]

PROVIDER SYNTHESIS:
- Perplexity Focus: [Summarize key points from Perplexity]
- Claude Focus: [Summarize key points from Claude]
- Agreement Areas: [Where both providers align]
- Disagreement Areas: [Where providers differ]

EMAIL ALERT DECISION:
Based on the analysis above, determine if an email alert should be sent.
Consider:
- Trend change probability (higher probability = more likely to send)
- Alert level from both providers
- Significance of changes detected
- Trading decision confidence

==================================================

Instructions:
1. Synthesize both analyses into a coherent trading decision
2. Highlight areas of agreement and disagreement
3. Provide specific price targets and risk levels when mentioned
4. Be objective and balanced in your assessment
5. Focus on actionable trading insights
6. Email alerts should be sent for significant changes that traders need to act on
"""

            # Helper to call the model with retries/backoff for transient errors (e.g., 429)
            def _call_with_backoff(prompt_text, max_attempts=5, base_delay=1.0):
                last_exception = None
                for attempt in range(1, max_attempts + 1):
                    try:
                        logger.info(f"Google AI attempt {attempt}/{max_attempts} for {stock_symbol}")
                        resp = self.model.generate_content(prompt_text)
                        
                        # Extract text from response
                        text = getattr(resp, 'text', None)
                        if text:
                            return text
                        
                        # Some responses may embed content differently
                        if isinstance(resp, dict) and 'content' in resp:
                            return resp['content']
                        
                        logger.error("Empty response from Google AI (no text/content)")
                        raise RuntimeError("Empty response from Google AI")
                        
                    except Exception as e:
                        last_exception = e
                        msg = str(e).lower()
                        
                        # Determine if this is a retryable error (rate limit / resource exhausted)
                        is_retryable = any(keyword in msg for keyword in [
                            '429', 'resource exhausted', 'rate limit', 'quota', 
                            'ratelimit', 'too many requests'
                        ])
                        
                        if is_retryable and attempt < max_attempts:
                            # Retry with exponential backoff + jitter
                            sleep_time = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1)
                            logger.warning(
                                f"Rate limit error (attempt {attempt}/{max_attempts}): {e}. "
                                f"Retrying in {sleep_time:.1f}s"
                            )
                            time.sleep(sleep_time)
                            continue
                        else:
                            # Non-retryable or exhausted attempts
                            logger.error(f"Google AI error (attempt {attempt}/{max_attempts}): {e}")
                            raise
                
                # If we get here, all retries exhausted
                raise RuntimeError(
                    f"Google AI generate_consolidated_decision failed after {max_attempts} attempts. "
                    f"Last error: {last_exception}"
                )

            # Generate response using Gemini with retries
            consolidated_text = _call_with_backoff(prompt)
            return consolidated_text
        except Exception as e:
            logger.error(f"Google AI API error: {e}")
            # Raise so callers (which fallback to local logic) can detect failure and fallback
            raise


class AnalyzerFactory:
    """Factory class to create the appropriate analyzer based on configuration"""
    
    @staticmethod
    def create_analyzer(provider: str) -> BaseAnalyzer:
        """
        Create an analyzer instance based on the provider
        
        Args:
            provider: 'perplexity' or 'claude'
            
        Returns:
            Analyzer instance
        """
        provider = provider.lower()
        
        if provider == 'perplexity':
            return PerplexityAnalyzer()
        elif provider == 'claude':
            return ClaudeAnalyzer()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}. Use 'perplexity' or 'claude'")


class TradingAnalyzer:
    """Main trading analyzer that supports running multiple AI providers in sequence"""
    
    def __init__(self):
        """Initialize with provider settings from environment variables"""
        self.claude_enabled = os.getenv('CLAUDE_ENABLED', 'False').lower() == 'true'
        self.perplexity_enabled = os.getenv('PERPLEXITY_ENABLED', 'False').lower() == 'true'
        self.google_enabled = os.getenv('GOOGLE_AI_ENABLED', 'False').lower() == 'true'
        
        # Import the actual analysis methods from trading_analysis.py
        self.original_analyzer = None
        try:
            from trading_analysis import PerplexityAnalyzer as OriginalAnalyzer
            # Only initialize if we have the API key
            if os.getenv('PERPLEXITY_API_KEY'):
                self.original_analyzer = OriginalAnalyzer()
        except ImportError:
            logger.error("trading_analysis module is required")
        except Exception as e:
            logger.warning(f"Could not initialize original analyzer: {e}")
        
        # Initialize enabled AI providers
        self.providers = {}
        self.google_analyzer = None
        
        # Check Perplexity setup
        if self.perplexity_enabled:
            perplexity_key = os.getenv('PERPLEXITY_API_KEY')
            if perplexity_key and self.original_analyzer:
                self.providers['perplexity'] = None  # Use original analyzer
                logger.info("Perplexity provider enabled")
            else:
                if not perplexity_key:
                    logger.warning("PERPLEXITY_ENABLED=True but PERPLEXITY_API_KEY not found")
                if not self.original_analyzer:
                    logger.warning("Could not initialize Perplexity analyzer")
                self.perplexity_enabled = False
                
        # Check Claude setup  
        if self.claude_enabled:
            claude_key = os.getenv('ANTHROPIC_API_KEY')
            if claude_key:
                try:
                    self.providers['claude'] = AnalyzerFactory.create_analyzer('claude')
                    logger.info("Claude provider enabled")
                except Exception as e:
                    logger.error(f"Failed to initialize Claude analyzer: {e}")
                    self.claude_enabled = False
            else:
                logger.warning("CLAUDE_ENABLED=True but ANTHROPIC_API_KEY not found")
                self.claude_enabled = False
        
        # Check Google AI setup for chart analysis
        if self.google_enabled:
            google_key = os.getenv('GOOGLE_AI_API_KEY')
            if google_key:
                try:
                    self.google_analyzer = GoogleAIAnalyzer(google_key)
                    self.providers['google'] = self.google_analyzer
                    logger.info("Google AI chart analyzer enabled")
                except Exception as e:
                    logger.error(f"Failed to initialize Google AI analyzer: {e}")
                    self.google_enabled = False
            else:
                logger.warning("GOOGLE_AI_ENABLED=True but GOOGLE_AI_API_KEY not found")
                self.google_enabled = False
        
        if not self.providers:
            logger.warning("No AI providers enabled or properly configured. Check API keys and enable flags.")
    
    def analyze_with_trend_alerts(self, screenshot_data: dict, output_dir: str = None, stock_symbol: str = None):
        """
        Main analysis method that runs all enabled AI providers in sequence
        """
        if not self.providers:
            logger.error("No AI providers enabled")
            return None, None
        
        results = {}
        combined_analysis = None
        combined_change_analysis = None
        
        # Run each enabled provider WITHOUT prior analysis - they focus on current state only
        for provider_name in self.providers.keys():
            logger.info(f"Running analysis with {provider_name.title()}")
            
            if provider_name == 'perplexity':
                # Use original Perplexity analyzer directly - but skip prior analysis
                analysis_text, change_analysis = self._analyze_with_perplexity_no_prior(
                    screenshot_data, output_dir, stock_symbol
                )
            elif provider_name == 'google':
                # Use Google AI analyzer for chart analysis
                analysis_text, change_analysis = self._analyze_with_google_ai(
                    screenshot_data, output_dir, stock_symbol
                )
            else:
                # Use custom provider (Claude, etc.) - but skip prior analysis
                analysis_text, change_analysis = self._analyze_with_custom_provider(
                    screenshot_data, output_dir, stock_symbol, provider_name, prior_analysis=None
                )
            
            if analysis_text and change_analysis:
                results[provider_name] = {
                    'analysis_text': analysis_text,
                    'change_analysis': change_analysis
                }
                
                # For the first successful analysis, use as base
                if combined_analysis is None:
                    combined_analysis = analysis_text
                    combined_change_analysis = change_analysis
        
        # If we have multiple results, create a combined report
        if len(results) > 1:
            combined_analysis, combined_change_analysis = self._combine_multi_provider_results(
                results, screenshot_data, output_dir, stock_symbol
            )
        
        return combined_analysis, combined_change_analysis
    
    def _analyze_with_perplexity_no_prior(self, screenshot_data: dict, output_dir: str = None, stock_symbol: str = None):
        """Analyze with Perplexity without prior analysis comparison"""
        try:
            # Filter out None/empty paths
            valid_screenshots = {k: v for k, v in screenshot_data.items() if v and os.path.exists(v)}
            
            if not valid_screenshots:
                logger.warning("No valid screenshots found for analysis")
                return None, None

            print(f"   📋 Analyzing current state only (no prior comparison)")

            # Encode all images
            image_data_uris = {}
            for window_type, image_path in valid_screenshots.items():
                try:
                    image_data_uris[window_type] = self.original_analyzer.encode_image_to_base64(image_path)
                except Exception as e:
                    logger.error(f"Failed to encode {window_type} image {image_path}: {e}")
                    continue
            
            if not image_data_uris:
                logger.error("Failed to encode any images")
                return None, None
            
            # Create prompt WITHOUT prior analysis
            prompt = self.original_analyzer._create_analysis_prompt(list(image_data_uris.keys()), prior_analysis=None, stock_symbol=stock_symbol)
            
            # Build content array with text prompt and all images
            content = [{"type": "text", "text": prompt}]
            
            # Add all images to the content
            for window_type, image_uri in image_data_uris.items():
                content.append({
                    "type": "image_url",
                    "image_url": {"url": image_uri}
                })
            
            print(f"   🤖 Analyzing {len(image_data_uris)} screenshots...")
            
            # Make API request using the original analyzer's client
            completion = self.original_analyzer.client.chat.completions.create(
                model="sonar",
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )
            
            result = completion.choices[0].message.content
            logger.info(f"Successfully analyzed {len(image_data_uris)} screenshots")
            
            # Parse response - no prior analysis so it will be treated as initial analysis
            analysis_text, change_analysis = self.original_analyzer._parse_response(result, prior_analysis=None)
            
            return analysis_text, change_analysis
            
        except Exception as e:
            logger.error(f"Perplexity analysis error: {e}")
            return None, None
    
    def _combine_multi_provider_results(self, results: dict, screenshot_data: dict, output_dir: str, stock_symbol: str):
        """Combine results from multiple AI providers into a comprehensive analysis"""
        from trading_analysis import logger

        # Create combined analysis report as HTML
        html = []
        html.append(f"""
<html>
<head>
    <meta charset='utf-8'>
    <title>Multi-Provider AI Analysis Report for {stock_symbol or 'Stock'}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f8f9fa; color: #222; margin: 0; padding: 0; }}
        .container {{ max-width: 900px; margin: 30px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 32px; }}
        h1 {{ text-align: center; font-size: 2.2em; margin-bottom: 0.2em; }}
        h2 {{ border-bottom: 2px solid #eee; padding-bottom: 0.2em; margin-top: 2em; }}
        .section {{ margin: 2em 0; }}
        .divider {{ border-top: 2px solid #bbb; margin: 2em 0; }}
        .summary-box {{ background: #f1f8e9; border-left: 6px solid #4caf50; padding: 1em 1.5em; margin: 1.5em 0; border-radius: 6px; font-size: 1.1em; }}
        ul, li {{ margin-bottom: 0.5em; }}
        .alert-list li {{ margin-bottom: 0.3em; }}
        .consensus-low {{ background: #fff3e0; border-left: 6px solid #ff9800; }}
        .consensus-high {{ background: #e3f2fd; border-left: 6px solid #2196f3; }}
        .provider-title {{ font-size: 1.3em; color: #333; margin-top: 1.5em; }}
        .meta {{ color: #888; font-size: 0.95em; text-align: right; margin-bottom: 1em; }}
    </style>
</head>
<body>
<div class='container'>
    <h1>Multi-Provider AI Analysis Report for {stock_symbol or 'Stock'}</h1>
    <div class='meta'>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
""")

        # Collect probabilities and alerts for consensus first
        all_probabilities = []
        all_alerts = []

        for provider_name, result in results.items():
            change_analysis = result['change_analysis']

            # Collect probabilities and alerts for consensus
            if change_analysis.get('trend_change_probability'):
                all_probabilities.append(change_analysis['trend_change_probability'])

            if change_analysis.get('has_changes'):
                all_alerts.append({
                    'provider': provider_name,
                    'alert_level': change_analysis['alert_level'],
                    'summary': change_analysis['summary'],
                    'probability': change_analysis.get('trend_change_probability', 0)
                })

        # Calculate averages for generating Google AI analysis first
        if all_probabilities:
            avg_probability = sum(all_probabilities) / len(all_probabilities)
            max_probability = max(all_probabilities)
            min_probability = min(all_probabilities)
        else:
            avg_probability = 0
            max_probability = 0
            min_probability = 0

        # Generate Google AI consolidated trading decision FIRST
        results_list = [(provider_name, result['analysis_text'], result['change_analysis']) 
                      for provider_name, result in results.items()]
        trading_decision = self._generate_consolidated_trading_decision(results_list, avg_probability, all_alerts, stock_symbol, output_dir, screenshot_data)
        
        # Parse Google AI's email alert decision from the consolidated decision text
        google_ai_wants_email = self._parse_google_ai_email_decision(trading_decision)
        html.append("<div class='divider'></div>")
        html.append("<h2>Google AI Consolidated Trading Decision</h2>")
        html.append(f"<div class='section'><pre style='white-space:pre-wrap;font-family:inherit;font-size:1.08em;background:#f6f8fa;padding:1em;border-radius:6px;border:1px solid #eee'>{trading_decision.strip()}</pre></div>")

        # Add individual provider analyses in desired order: Claude, then Perplexity
        provider_order = ['claude', 'perplexity']
        section_titles = {
            'claude': 'Claude Analysis',
            'perplexity': 'Perplexity Analysis'
        }
        for provider_name in provider_order:
            if provider_name in results:
                result = results[provider_name]
                analysis = result['analysis_text']
                html.append("<div class='divider'></div>")
                html.append(f"<div class='provider-title'>{section_titles[provider_name]}</div>")
                html.append(f"<div class='section'><pre style='white-space:pre-wrap;font-family:inherit;font-size:1.08em;background:#f6f8fa;padding:1em;border-radius:6px;border:1px solid #eee'>{analysis.strip()}</pre></div>")
        # Add any other providers not in the ordered list
        for provider_name, result in results.items():
            if provider_name not in provider_order:
                analysis = result['analysis_text']
                html.append("<div class='divider'></div>")
                html.append(f"<div class='provider-title'>{provider_name.upper()} Analysis</div>")
                html.append(f"<div class='section'><pre style='white-space:pre-wrap;font-family:inherit;font-size:1.08em;background:#f6f8fa;padding:1em;border-radius:6px;border:1px solid #eee'>{analysis.strip()}</pre></div>")

        # Create consensus summary at the end
        html.append("<div class='divider'></div>")
        html.append("<h2>Multi-Provider Consensus Summary</h2>")
        html.append("<div class='section'>")
        if all_probabilities:
            html.append(f"<ul><li><b>Average Trend Change Probability:</b> {avg_probability:.1f}%</li><li><b>Range:</b> {min_probability:.1f}% - {max_probability:.1f}%</li></ul>")

        # Determine consensus alert level
        # IMPORTANT: Google AI's email decision overrides provider consensus
        if google_ai_wants_email:
            # Google AI determined email should be sent
            if all_alerts:
                html.append(f"<div><b>Alerts from {len(all_alerts)} provider(s):</b></div>")
                html.append("<ul class='alert-list'>")
                for alert in all_alerts:
                    html.append(f"<li><b>{alert['provider'].title()}:</b> <span style='color:#d84315;font-weight:bold'>{alert['alert_level'].upper()}</span> ({alert['probability']}%) - {alert['summary']}</li>")
                html.append("</ul>")
                # Use highest alert level for consensus
                alert_levels = {'low': 1, 'medium': 2, 'high': 3}
                max_alert = max(all_alerts, key=lambda x: alert_levels.get(x['alert_level'].lower(), 0))
                alert_level = max_alert['alert_level']
                summary = f"Google AI Consensus: {max_alert['summary']}"
            else:
                # Google AI says send email even if providers didn't flag changes
                alert_level = 'medium' if avg_probability >= 50 else 'low'
                summary = f"Google AI detected significant market conditions requiring attention"
            
            html.append(f"<div class='summary-box consensus-high'>CONSENSUS: <b>{alert_level.upper()}</b> | Confidence: <b>HIGH</b> | Google AI: <b>EMAIL ALERT</b> | Providers: <b>{len(results)}</b> | Probability: <b>{avg_probability:.1f}%</b><br>SUMMARY: {summary}</div>")
            consensus_change_analysis = {
                'has_changes': True,  # Google AI determined email should be sent
                'alert_level': alert_level,
                'summary': summary,
                'trend_change_probability': avg_probability,
                'confidence_level': 'high',
                'provider_count': len(results),
                'provider_agreement': len(all_alerts) / len(results) * 100 if all_alerts else 0,
                'google_ai_decision': True
            }
        elif all_alerts:
            # Providers flagged changes but Google AI didn't explicitly say to send email
            html.append(f"<div><b>Alerts from {len(all_alerts)} provider(s):</b></div>")
            html.append("<ul class='alert-list'>")
            for alert in all_alerts:
                html.append(f"<li><b>{alert['provider'].title()}:</b> <span style='color:#d84315;font-weight:bold'>{alert['alert_level'].upper()}</span> ({alert['probability']}%) - {alert['summary']}</li>")
            html.append("</ul>")
            alert_levels = {'low': 1, 'medium': 2, 'high': 3}
            max_alert = max(all_alerts, key=lambda x: alert_levels.get(x['alert_level'].lower(), 0))
            html.append(f"<div class='summary-box consensus-high'>CONSENSUS: <b>{max_alert['alert_level'].upper()}</b> | Confidence: <b>HIGH</b> | Providers: <b>{len(results)}</b> | Agreement: <b>{len(all_alerts) / len(results) * 100:.1f}%</b><br>SUMMARY: {max_alert['summary']}</div>")
            consensus_change_analysis = {
                'has_changes': True,
                'alert_level': max_alert['alert_level'],
                'summary': f"Consensus from {len(results)} providers: {max_alert['summary']}",
                'trend_change_probability': avg_probability,
                'confidence_level': 'high',
                'provider_count': len(results),
                'provider_agreement': len(all_alerts) / len(results) * 100
            }
        else:
            # No alerts from providers and Google AI didn't request email
            html.append(f"<div class='summary-box consensus-low'>CONSENSUS: <b>LOW</b> | Confidence: <b>MEDIUM</b> | Providers: <b>{len(results)}</b> | Agreement: <b>0%</b><br>SUMMARY: No significant changes detected</div>")
            consensus_change_analysis = {
                'has_changes': False,
                'alert_level': 'low',
                'summary': f"No significant changes detected by {len(results)} providers or Google AI",
                'trend_change_probability': avg_probability,
                'confidence_level': 'medium',
                'provider_count': len(results),
                'provider_agreement': 0
            }
        html.append("</div>")
        html.append("</div></body></html>")

        # Save the combined report as HTML in the correct symbol folder (no text file)
        try:
            base_dir = get_base_dir()
            print(f"[DEBUG] Attempting to save HTML report for {stock_symbol}...")
            print(f"[DEBUG] Current working directory: {os.getcwd()}")
            print(f"[DEBUG] Base dir for output: {base_dir}")
            symbol_dir = os.path.join(base_dir, 'screenshots', stock_symbol)
            print(f"[DEBUG] Target symbol_dir: {symbol_dir}")
            ensure_directory_exists(symbol_dir)
            report_path = os.path.join(symbol_dir, MULTI_PROVIDER_HTML_FILENAME)
            print(f"[DEBUG] Writing HTML to: {report_path}")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(''.join(html))
            print(f"[DEBUG] HTML report successfully written: {report_path}")
            logger.info(f"Multi-provider HTML report saved to: {report_path}")

            # Send email alert ONLY from Google AI consensus (not from individual providers like Perplexity/Claude)
            try:
                from trading_analysis import EmailAlertManager
                print("   📧 Google AI Consensus: Evaluating email alert...")
                email_manager = EmailAlertManager()
                
                if email_manager.is_configured and consensus_change_analysis.get('has_changes', False):
                    print(f"   📧 Sending email alert from Google AI consensus")
                    print(f"   📊 Alert Level: {consensus_change_analysis.get('alert_level', 'unknown').upper()}")
                    print(f"   📊 Probability: {consensus_change_analysis.get('trend_change_probability', 0):.1f}%")
                    
                    email_sent = email_manager.send_trend_alert(consensus_change_analysis, ''.join(html), stock_symbol, output_dir)
                    
                    if email_sent:
                        print(f"   ✅ Email alert sent successfully from Google AI consensus")
                    else:
                        print(f"   ⚠️ Email alert failed to send")
                        logger.warning("Google AI consensus email alert failed to send")
                elif not email_manager.is_configured:
                    print("   📧 Email alerts not configured (check .env settings)")
                else:
                    print(f"   📧 No email sent - no significant changes detected by Google AI consensus")
            except Exception as e:
                print(f"   ❌ Error sending Google AI consensus email alert: {e}")
                logger.error(f"Failed to send Google AI consensus email alert: {e}")
        except Exception as e:
            print(f"[ERROR] Failed to write HTML report for {stock_symbol}: {e}")
            import traceback
            traceback.print_exc()
            logger.error(f"Failed to write HTML report for {stock_symbol}: {e}")
        return ''.join(html), consensus_change_analysis
    
    def _parse_google_ai_email_decision(self, trading_decision: str) -> bool:
        """
        Parse Google AI's email alert decision from the consolidated trading decision text.
        Uses multiple heuristics to determine if an email alert should be sent.
        
        Returns:
            True if Google AI recommends sending an email alert, False otherwise
        """
        if not trading_decision:
            return False
        
        # Normalize text for case-insensitive matching
        decision_text = trading_decision.upper()
        
        # Look for explicit YES/SEND patterns (highest priority)
        yes_patterns = [
            "EMAIL ALERT DECISION: YES",
            "EMAIL ALERT DECISION:YES",
            "SEND EMAIL ALERT",
            "EMAIL: YES",
            "ALERT: YES",
            "RECOMMENDATION: SEND EMAIL",
            "SHOULD SEND EMAIL",
            "ALERT RECOMMENDED"
        ]
        
        # Look for explicit NO/DON'T SEND patterns (highest priority)
        no_patterns = [
            "EMAIL ALERT DECISION: NO",
            "EMAIL ALERT DECISION:NO",
            "DO NOT SEND EMAIL",
            "DON'T SEND EMAIL",
            "EMAIL: NO",
            "ALERT: NO",
            "NO EMAIL NEEDED",
            "NOT ALERT",
            "NO ALERT NEEDED"
        ]
        
        # Check for explicit YES/NO patterns first (highest priority)
        for pattern in yes_patterns:
            if pattern in decision_text:
                from trading_analysis import logger
                logger.info(f"Google AI email decision: SEND (matched pattern: '{pattern}')")
                print(f"   📧 Google AI Decision: SEND EMAIL ALERT (matched: '{pattern}')")
                return True
        
        for pattern in no_patterns:
            if pattern in decision_text:
                from trading_analysis import logger
                logger.info(f"Google AI email decision: DO NOT SEND (matched pattern: '{pattern}')")
                print(f"   📧 Google AI Decision: NO EMAIL (matched: '{pattern}')")
                return False
        
        # Secondary heuristics: Look for key indicator words that suggest an alert
        # Count bullish vs bearish signals
        bullish_keywords = ["BUY", "STRONG BUY", "BULLISH", "UPTREND", "SIGNAL", "ALERT", "OPPORTUNITY", "REVERSAL UP", "BREAKOUT"]
        bearish_keywords = ["SELL", "STRONG SELL", "BEARISH", "DOWNTREND", "WARNING", "CAUTION", "REVERSAL DOWN", "BREAKDOWN"]
        
        bullish_count = sum(1 for keyword in bullish_keywords if keyword in decision_text)
        bearish_count = sum(1 for keyword in bearish_keywords if keyword in decision_text)
        
        # If there's a clear bias toward bullish signals AND the word "ALERT" or "SIGNAL" appears, likely should alert
        if ("ALERT" in decision_text or "SIGNAL" in decision_text) and (bullish_count > bearish_count):
            from trading_analysis import logger
            logger.info("Google AI email decision: SEND (based on bullish signals and alert keywords)")
            print("   📧 Google AI Decision: SEND EMAIL ALERT (based on bullish signals)")
            return True
        
        # If there's significant bearish content with warning keywords, also alert
        if ("WARNING" in decision_text or "CAUTION" in decision_text) and bearish_count > 0:
            from trading_analysis import logger
            logger.info("Google AI email decision: SEND (based on bearish warnings)")
            print("   📧 Google AI Decision: SEND EMAIL ALERT (based on bearish warnings)")
            return True
        
        # No clear pattern found - default to False for safety
        from trading_analysis import logger
        logger.info("Google AI email decision: UNCLEAR (defaulting to NO)")
        print("   ⚠️ Google AI Decision: UNCLEAR (defaulting to NO EMAIL)")
        return False
    
    def _generate_consolidated_trading_decision(self, results: list, avg_probability: float, all_alerts: list, stock_symbol: str = "UNKNOWN", output_dir: str = None, screenshot_data: dict = None):
        """Generate a consolidated trading decision using Google AI Studio API"""
        if not results:
            return "\n=== CONSOLIDATED TRADING DECISION ===\nNo provider analyses available.\n"
        
        try:
            # Initialize Google AI analyzer if Google AI API key is available
            google_api_key = os.getenv('GOOGLE_AI_API_KEY')
            if not google_api_key or google_api_key == 'YOUR_GOOGLE_AI_API_KEY_HERE':
                # Fall back to original logic if Google AI is not configured
                return self._generate_local_consolidated_decision(results, avg_probability, all_alerts, stock_symbol)
            
            # Initialize Google AI analyzer
            google_analyzer = GoogleAIAnalyzer(google_api_key)
            
            # Extract individual provider analyses
            perplexity_analysis = ""
            claude_analysis = ""
            
            for provider_name, analysis_text, change_analysis in results:
                if provider_name.lower() == 'perplexity':
                    perplexity_analysis = analysis_text
                elif provider_name.lower() == 'claude':
                    claude_analysis = analysis_text
            
            # Generate consolidated decision using Google AI
            if perplexity_analysis or claude_analysis:
                consolidated_decision = google_analyzer.generate_consolidated_decision(
                    perplexity_analysis, claude_analysis, stock_symbol, output_dir, screenshot_data
                )
                return f"\n{consolidated_decision}\n"
            else:
                # Fall back to local logic if no provider analyses found
                return self._generate_local_consolidated_decision(results, avg_probability, all_alerts, stock_symbol)
                
        except Exception as e:
            logger.error(f"Failed to generate Google AI consolidated decision: {e}")
            # Fall back to original logic if Google AI fails
            return self._generate_local_consolidated_decision(results, avg_probability, all_alerts, stock_symbol)
    
    def _generate_local_consolidated_decision(self, results: list, avg_probability: float, all_alerts: list, stock_symbol: str = "UNKNOWN"):
        """Original local logic for generating consolidated trading decisions (fallback)"""
        # Collect trading recommendations and confidence levels
        recommendations = []
        total_providers = len(results)
        
        # Use all_alerts if available, otherwise extract from results
        if all_alerts:
            for alert in all_alerts:
                alert_level = alert.get('alert_level', 'medium')
                probability = alert.get('probability', 50) / 100  # Convert percentage to decimal
                
                if alert_level == 'high' or probability > 0.7:
                    recommendations.append('BUY')
                elif alert_level == 'low' or probability < 0.3:
                    recommendations.append('SELL')
                else:
                    recommendations.append('HOLD')
        else:
            # Fall back to extracting from results
            for provider_name, _, change_analysis in results:
                if change_analysis and change_analysis.get('has_changes', False):
                    alert_level = change_analysis.get('alert_level', 'medium')
                    probability = change_analysis.get('trend_change_probability', 0.5)
                    
                    if alert_level == 'high' or probability > 0.7:
                        recommendations.append('BUY')
                    elif alert_level == 'low' or probability < 0.3:
                        recommendations.append('SELL')
                    else:
                        recommendations.append('HOLD')
                else:
                    recommendations.append('HOLD')
        
        # Ensure we have recommendations for all providers
        while len(recommendations) < total_providers:
            recommendations.append('HOLD')
        
        # Calculate consensus
        buy_votes = recommendations.count('BUY')
        sell_votes = recommendations.count('SELL')
        hold_votes = recommendations.count('HOLD')
        
        # Determine consensus decision
        if buy_votes > sell_votes and buy_votes > hold_votes:
            consensus_decision = 'BUY'
            decision_strength = f"{buy_votes}/{total_providers}"
        elif sell_votes > buy_votes and sell_votes > hold_votes:
            consensus_decision = 'SELL'
            decision_strength = f"{sell_votes}/{total_providers}"
        else:
            consensus_decision = 'HOLD'
            decision_strength = f"{hold_votes}/{total_providers}"
        
        # Generate consolidated report
        consolidated_text = f"\n{'='*50}\n"
        consolidated_text += f"LOCAL CONSOLIDATED TRADING DECISION FOR {stock_symbol}\n"
        consolidated_text += f"{'='*50}\n\n"
        
        consolidated_text += f"TRADING DECISION: {consensus_decision}\n"
        consolidated_text += f"Provider Consensus: {decision_strength} providers agree\n"
        consolidated_text += f"Average Confidence: {avg_probability:.2f}\n\n"
        
        consolidated_text += "TREND CHANGE EVALUATION:\n"
        if avg_probability > 0.6:
            consolidated_text += f"High probability ({avg_probability:.1%}) of significant trend change\n"
        elif avg_probability > 0.4:
            consolidated_text += f"Moderate probability ({avg_probability:.1%}) of trend change\n"
        else:
            consolidated_text += f"Low probability ({avg_probability:.1%}) of trend change\n"
        
        consolidated_text += "\nProvider Breakdown:\n"
        for i, (provider_name, _, change_analysis) in enumerate(results):
            if i < len(recommendations):
                rec = recommendations[i]
                if all_alerts and i < len(all_alerts):
                    conf = all_alerts[i].get('probability', 0) / 100
                elif change_analysis:
                    conf = change_analysis.get('trend_change_probability', avg_probability)
                else:
                    conf = avg_probability
                consolidated_text += f"- {provider_name}: {rec} (confidence: {conf:.2f})\n"
        
        consolidated_text += f"\n{'='*50}\n"
        
        return consolidated_text
    
    def _analyze_with_google_ai(self, screenshot_data: dict, output_dir: str = None, stock_symbol: str = None):
        """Analyze charts with Google AI"""
        try:
            # Filter out None/empty paths
            valid_screenshots = {k: v for k, v in screenshot_data.items() if v and os.path.exists(v)}
            
            if not valid_screenshots:
                logger.warning("No valid screenshots found for Google AI analysis")
                return None, None
            
            print(f"   🤖 Google AI analyzing {len(valid_screenshots)} chart screenshot(s)...")
            
            # Encode all images
            image_data_uris = {}
            for window_type, image_path in valid_screenshots.items():
                try:
                    image_data_uris[window_type] = self.google_analyzer.encode_image_to_base64(image_path)
                except Exception as e:
                    logger.error(f"Failed to encode {window_type} image for Google AI: {e}")
                    continue
            
            if not image_data_uris:
                logger.error("Failed to encode any images for Google AI analysis")
                return None, None
            
            # Create analysis prompt for Google AI - SAME AS PERPLEXITY/CLAUDE
            window_types = list(image_data_uris.keys())
            symbol_text = f" for {stock_symbol}" if stock_symbol else ""
            email_threshold = int(os.getenv('EMAIL_ALERT_THRESHOLD', '60'))
            
            # Create chart-specific context (same as Perplexity)
            chart_context = ""
            if 'trend_analysis' in window_types:
                chart_context += """
CHART CONTEXT - Trend Analysis Window:
This chart displays LuxAlgo technical indicators. Use the following documentation to analyze it:
- LuxAlgo Signals & Overlays: https://docs.luxalgo.com/docs/algos/signals-overlays/signals
- LuxAlgo Price Action Concepts: https://docs.luxalgo.com/docs/algos/price-action-concepts/introduction

Pay special attention to:
- Signal Quality (Strong Buy/Sell signals)
- Price Action Concepts (Support/Resistance levels, market structure)
- Overlay indicators (trend direction, strength)
- Signal confirmations and divergences

"""
            
            if 'heiken_ashi' in window_types:
                chart_context += """
CHART CONTEXT - Smoothed Heiken Ashi Candles Window:
This chart displays the following technical indicators:
- Smoothed Heiken Ashi Candles: Trend-following candles that smooth out price action
- AlgoAlpha HEMA Trend: Hybrid Exponential Moving Average for trend identification
- Divergence Indicators: Price vs indicator divergences for reversal signals
- Volume Footprint: Order flow analysis showing buy/sell volume at each price level

Pay special attention to:
- Smoothed Heiken Ashi candle colors (bullish/bearish trends)
- HEMA trend direction and crossovers
- Divergence signals (bullish/bearish divergences)
- Trend strength and momentum
- Reversal patterns indicated by divergences
- Volume Footprint Analysis:
  * Absorption: Large volume at price level with minimal price movement indicates strong institutional support/resistance
  * Exhaustion: Decreasing volume as price extends signals trend weakness and potential reversal
  * Bid/ask imbalances at key levels for order flow confirmation

"""
            
            if 'volume_layout' in window_types:
                chart_context += """
CHART CONTEXT - Volume Layout Window:
This chart displays the following technical indicators:
- LuxAlgo Money Flow Profile: Shows institutional money flow and buying/selling pressure
- CVD Divergence Oscillator: Cumulative Volume Delta divergences for trend reversals
- SQZMOM_LB: Squeeze Momentum indicator with LazyBear modifications
- MA Distance with StdDev Bands: Moving average distance with standard deviation bands

Pay special attention to:
- Money flow profile (accumulation/distribution zones)
- CVD divergence signals (bullish/bearish divergences)
- SQZMOM_LB squeeze conditions and momentum direction
- MA distance from price and standard deviation extremes
- **CRITICAL**: If a +RD (Positive Reversal Divergence) or -RD (Negative Reversal Divergence) was formed recently, clearly indicate this in the analysis as it signals potential trend reversal
- Volume patterns confirming or diverging from price action

"""
            
            if 'volumeprofile' in window_types:
                chart_context += """
CHART CONTEXT - Volume Profile Window:
This chart displays the following technical indicators:
- RVOL: Relative Volume indicator showing volume compared to average
- VOLD Ratio: Volume Delta ratio showing buying vs selling pressure
- MS (Matrix Mod): Matrix momentum indicator with overbought/oversold levels
- TTOB (Trapped Trader Order Blocks): Identifies trapped trader zones and order blocks

Pay special attention to:
- RVOL levels (high relative volume confirms moves)
- VOLD ratio (positive = buying pressure, negative = selling pressure)
- **MS Matrix Mod overbought/oversold conditions**: If the MS indicator shows overbought or oversold conditions, clearly indicate this in the analysis as it signals potential reversal zones
- TTOB order blocks (support/resistance from trapped traders)
- Volume profile distribution (high volume nodes, value area)
- Point of Control (POC) levels
- Volume confirmation of price movements

"""
            
            if 'workspace' in window_types:
                chart_context += """
CHART CONTEXT - Symbolik Workspace Window:
This chart displays the following technical indicators:
- ATM Chart Lines: Algorithmic Trading Model support/resistance lines
- ATM Elliott Projections: Elliott Wave price projections and targets
- ATM Elliott Waves: Elliott Wave count and structure analysis
- ATM Pressure Alert: Market pressure and momentum alerts
- TKT Analysis: Technical Knowledge Trading analysis framework
- TKT Score: Quantified trading opportunity score
- Variable Aggressive Sequential (Demark Sequential): TD Sequential buy/sell setup and countdown signals

Pay special attention to:
- **ATM Chart Lines alignment**: If the current price is sitting on or near an ATM chart line, clearly indicate this in the analysis as it represents a key support/resistance level
- ATM Elliott Wave count and current position in the wave structure
- ATM Elliott projections for price targets
- ATM Pressure alerts (bullish/bearish pressure signals)
- TKT analysis signals and overall market structure
- TKT score value (higher scores indicate stronger opportunities)
- Variable Aggressive Sequential setup and countdown numbers (9s and 13s are critical)
- Demark Sequential buy/sell signals at exhaustion points

"""
            
            prompt = f"""
You are an expert stock market analyst. Analyze these {len(window_types)} chart screenshots{symbol_text}.

CRITICAL INSTRUCTION: Only analyze what you can clearly see in the screenshots. If a chart window appears blank, contains no data, or is not loaded properly, explicitly state "Chart not loaded" or "No data visible" for that window. DO NOT make assumptions or provide analysis for charts that are not visible or contain no data.

{chart_context}
ANALYSIS FORMAT:

**MARKET OVERVIEW** (2-3 sentences)
Current price, timeframe, and overall market condition.

**KEY VISIBLE INDICATORS**
List specific indicators visible:
- For Trend Analysis chart: LuxAlgo signals, price action concepts, overlays
- For Smoothed Heiken Ashi chart: Heiken Ashi candles, HEMA trend, divergences
- For Volume Layout chart: Money flow profile, CVD divergence, SQZMOM_LB, MA distance with StdDev bands, +RD/-RD signals
- For Volume Profile chart: RVOL, VOLD ratio, MS (Matrix Mod) overbought/oversold, TTOB order blocks
- For Symbolik Workspace chart: ATM chart lines, ATM Elliott Waves/Projections, ATM Pressure alerts, TKT analysis/score, Variable Aggressive Sequential (Demark)
- Moving averages, oscillators, volume data, support/resistance levels

**CRITICAL SIGNALS**
Most important actionable signals (include any +RD or -RD formations, MS overbought/oversold conditions, ATM chart line alignments, Demark Sequential 9s or 13s if present)

**TRADING DECISION**
Clear BUY/SELL/HOLD with rationale

**TREND CHANGE EVALUATION**
Assess probability of significant trend change or reversal in the short term (0-100%). Explain what indicators suggest this.
"""
            
            # Build content array with text prompt and all images
            content = [{"type": "text", "text": prompt}]
            
            # Add all images to the content
            for window_type, image_uri in image_data_uris.items():
                content.append({
                    "type": "image_url",
                    "image_url": {"url": image_uri}
                })
            
            # Call Google AI analyze_screenshots method
            analysis_text = self.google_analyzer.analyze_screenshots(content)
            
            if not analysis_text:
                logger.warning("Google AI returned empty analysis")
                return None, None
            
            # For Google AI chart analysis, we mark as "change" if high confidence analysis provided
            change_analysis = {
                'has_changes': True,  # Google AI provides detailed analysis
                'alert_level': 'low',  # Chart analysis is informational
                'summary': 'Google AI chart analysis completed',
                'probability': 0  # No change probability for chart analysis
            }
            
            logger.info(f"Google AI chart analysis completed for {stock_symbol}")
            return analysis_text, change_analysis
            
        except Exception as e:
            logger.error(f"Google AI chart analysis error: {e}")
            import traceback
            traceback.print_exc()
            return None, None
    
    def _analyze_with_custom_provider(self, screenshot_data: dict, output_dir: str = None, stock_symbol: str = None, provider_name: str = 'claude', prior_analysis: str = None):
        """Analyze using custom AI provider (Claude, etc.)"""
        try:
            # Import necessary components
            from trading_analysis import logger
            
            # Get the specific AI provider
            ai_provider = self.providers.get(provider_name)
            if not ai_provider:
                logger.error(f"Provider {provider_name} not available")
                return None, None
            
            # Filter out None/empty paths (same as original)
            valid_screenshots = {k: v for k, v in screenshot_data.items() if v and os.path.exists(v)}
            
            if not valid_screenshots:
                logger.warning("No valid screenshots found for analysis")
                return None, None

            # Use the passed prior analysis (which will be None for current state analysis)
            if prior_analysis:
                print(f"   📋 Using prior analysis for comparison")
            else:
                print(f"   📋 Analyzing current state only (no prior comparison)")

            # Encode all images using our AI provider
            image_data_uris = {}
            for window_type, image_path in valid_screenshots.items():
                try:
                    image_data_uris[window_type] = ai_provider.encode_image_to_base64(image_path)
                except Exception as e:
                    logger.error(f"Failed to encode {window_type} image {image_path}: {e}")
                    continue
            
            if not image_data_uris:
                logger.error("Failed to encode any images")
                return None, None
            
            # Create prompt using original method
            prompt = self.original_analyzer._create_analysis_prompt(list(image_data_uris.keys()), prior_analysis, stock_symbol)
            
            # Build messages for AI provider
            messages = self._build_messages_for_provider(prompt, image_data_uris)
            
            print(f"   🤖 Analyzing {len(image_data_uris)} screenshots with {provider_name.title()}...")
            
            # Make API request using our provider
            result = ai_provider.analyze_screenshots(messages)
            logger.info(f"Successfully analyzed {len(image_data_uris)} screenshots with {provider_name}")
            
            # Parse response using original method
            analysis_text, change_analysis = self.original_analyzer._parse_response(result, prior_analysis)
            
            # Handle alerts and email (same as original)
            self._handle_alerts(change_analysis, analysis_text, stock_symbol, output_dir, provider_name)
            
            return analysis_text, change_analysis
            
        except Exception as e:
            logger.error(f"Error in {provider_name} analysis: {e}")
            return None, None
    
    def _build_messages_for_provider(self, prompt: str, image_data_uris: dict) -> list:
        """Build messages compatible with different AI providers"""
        # For Claude, we don't use system messages in the messages array
        # The system prompt is handled separately
        
        # Build content array with text prompt and all images
        content = [{"type": "text", "text": prompt}]
        
        # Add all images to the content
        for window_type, image_uri in image_data_uris.items():
            content.append({
                "type": "image_url", 
                "image_url": {"url": image_uri}
            })
        
        return [{"role": "user", "content": content}]
    
    def _handle_alerts(self, change_analysis: dict, analysis_text: str, stock_symbol: str, output_dir: str, provider_name: str = None):
        """Handle alert display and email notifications"""
        provider_label = f" ({provider_name.title()})" if provider_name else ""
        
        if change_analysis['has_changes']:
            alert_level = change_analysis['alert_level'].upper()
            probability = change_analysis.get('trend_change_probability', 0)
            print(f"   🚨 {alert_level} ALERT{provider_label}: {change_analysis['summary']}")
            print(f"   📊 Trend Change Probability: {probability}%")
            print(f"   📧 Email will be sent from Google AI consensus (not individual providers)")
        else:
            probability = change_analysis.get('trend_change_probability', 0)
            print(f"   ✅ No significant trend changes detected{provider_label} (Probability: {probability}%)")
    
    def save_combined_analysis_report(self, screenshot_data, analysis, output_dir, change_analysis):
        """Delegate to original analyzer"""
        return self.original_analyzer.save_combined_analysis_report(screenshot_data, analysis, output_dir, change_analysis)