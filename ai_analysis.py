"""
AI API integration module for screenshot analysis with email alerts
Supports both Perplexity and Claude APIs
"""
# Standard library imports
import logging
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Optional, Dict, Any

# Local imports
from utils import (
    encode_image_to_base64, 
    ensure_directory_exists, 
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
        
        # Get model from environment variable or use default
        self.model = os.getenv('PERPLEXITY_MODEL', 'sonar-pro')
        
        # Initialize the OpenAI client with Perplexity's endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.perplexity.ai"
        )
    
    def analyze_screenshots(self, messages: list) -> str:
        """Analyze screenshots using Perplexity API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
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
        
        # Get model from environment variable or use default
        self.model = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')
        
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
                "model": self.model,
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
        
        # Get model from environment variable or use default
        model_name = os.getenv('GOOGLE_AI_MODEL', 'gemini-3-pro-preview')
        
        # Initialize the model
        self.model = genai.GenerativeModel(model_name)
        
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
                    
                # Try alternate extraction methods
                if hasattr(resp, 'candidates') and resp.candidates:
                    candidate = resp.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content.parts:
                        return candidate.content.parts[0].text
                
                return None
                
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()
                
                # Check if this is a retryable error (rate limiting, quota, etc.)
                is_retryable = any(term in error_str for term in [
                    'rate', 'limit', 'quota', '429', '503', 'overloaded', 'resource_exhausted'
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
    
    def generate_consolidated_decision(self, perplexity_analysis: str, claude_analysis: str, stock_symbol: str = "UNKNOWN", output_dir: str = None, screenshot_data: dict = None, google_analysis: str = None) -> str:
        """
        Generate a consolidated trading decision based on analyses from multiple AI providers
        
        Args:
            perplexity_analysis: Full text analysis from Perplexity
            claude_analysis: Full text analysis from Claude
            stock_symbol: Stock symbol being analyzed
            output_dir: Directory for loading prior analysis
            screenshot_data: Screenshot data for loading prior analysis
            google_analysis: Optional analysis from Google AI
            
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
            
            # Build provider sections dynamically
            provider_sections = f"""PERPLEXITY ANALYSIS:
{perplexity_analysis}

CLAUDE ANALYSIS:
{claude_analysis}"""

            if google_analysis:
                provider_sections += f"""

GOOGLE AI ANALYSIS:
{google_analysis}"""
            
            prompt = f"""
You are an expert financial analyst tasked with creating a consolidated trading decision based on analyses from multiple AI providers.

STOCK SYMBOL: {stock_symbol}

{provider_sections}

{prior_context}

Based on these comprehensive analyses, generate a consolidated trading decision with the following format:

==================================================
CONSOLIDATED TRADING DECISION FOR {stock_symbol}
==================================================

TRADING DECISION: [BUY/SELL/HOLD]
Consensus Assessment: [Describe agreement/disagreement between providers]
Overall Confidence: [Provide a confidence percentage 0-100%]

TREND CHANGE EVALUATION:
[Synthesize the trend change probability from all analyses]
[Provide consolidated probability assessment]
[Explain key factors driving the trend evaluation]

CRITICAL FACTORS:
- [List 3-5 most important technical factors from all analyses]
- [Highlight any conflicting signals between providers]
- [Note volume, momentum, and support/resistance levels]

RISK ASSESSMENT:
- Upside Potential: [Based on resistance levels and bullish signals]
- Downside Risk: [Based on support levels and bearish signals]
- Stop Loss Recommendation: [If applicable]

PROVIDER SYNTHESIS:
- Perplexity Focus: [Summarize key points from Perplexity]
- Claude Focus: [Summarize key points from Claude]"""

            if google_analysis:
                prompt += """
- Google AI Focus: [Summarize key points from Google AI]"""
            
            prompt += """
- Agreement Areas: [Where providers align]
- Disagreement Areas: [Where providers differ]

EMAIL ALERT DECISION:
Based on the analysis above, determine if an email alert should be sent.
Consider:
- Trend change probability (higher probability = more likely to send)
- Alert levels from all providers
- Significance of changes detected
- Trading decision confidence

==================================================

Instructions:
1. Synthesize all analyses into a coherent trading decision
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

    def generate_consolidated_decision_multi(self, provider_analyses: dict, stock_symbol: str = "UNKNOWN", output_dir: str = None, screenshot_data: dict = None) -> str:
        """
        Generate a consolidated trading decision based on analyses from any combination of AI providers
        
        Args:
            provider_analyses: Dict of {provider_name: analysis_text} for all providers
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
                from trading_analysis import PerplexityAnalyzer
                temp_analyzer = PerplexityAnalyzer()
                valid_screenshots = {k: v for k, v in screenshot_data.items() if v and os.path.exists(v)}
                if valid_screenshots:
                    prior_analysis = temp_analyzer._load_prior_analysis(output_dir, valid_screenshots, stock_symbol)
            
            # Create prior context
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
            
            # Build provider sections dynamically from all available providers
            provider_sections = ""
            provider_names = list(provider_analyses.keys())
            
            for provider_name in provider_analyses:
                analysis_text = provider_analyses[provider_name]
                provider_sections += f"""{provider_name.upper()} ANALYSIS:
{analysis_text}

"""
            
            # Build dynamic provider synthesis section
            provider_synthesis = "\nPROVIDER SYNTHESIS:\n"
            for provider_name in provider_analyses:
                provider_synthesis += f"- {provider_name.title()} Focus: [Summarize key points from {provider_name.title()}]\n"
            provider_synthesis += "- Agreement Areas: [Where providers align]\n"
            provider_synthesis += "- Disagreement Areas: [Where providers differ]\n"
            
            prompt = f"""
You are an expert financial analyst tasked with creating a consolidated trading decision based on analyses from multiple AI providers.

STOCK SYMBOL: {stock_symbol}

{provider_sections}

{prior_context}

Based on these comprehensive analyses, generate a consolidated trading decision with the following format:

==================================================
CONSOLIDATED TRADING DECISION FOR {stock_symbol}
==================================================

TRADING DECISION: [BUY/SELL/HOLD]
Consensus Assessment: [Describe agreement/disagreement between providers]
Overall Confidence: [Provide a confidence percentage 0-100%]

TREND CHANGE EVALUATION:
[Synthesize the trend change probability from all analyses]
[Provide consolidated probability assessment]
[Explain key factors driving the trend evaluation]

CRITICAL FACTORS:
- [List 3-5 most important technical factors from all analyses]
- [Highlight any conflicting signals between providers]
- [Note volume, momentum, and support/resistance levels]

RISK ASSESSMENT:
- Upside Potential: [Based on resistance levels and bullish signals]
- Downside Risk: [Based on support levels and bearish signals]
- Stop Loss Recommendation: [If applicable]
{provider_synthesis}

EMAIL ALERT DECISION:
Based on the analysis above, determine if an email alert should be sent.
Consider:
- Trend change probability (higher probability = more likely to send)
- Alert levels from all providers
- Significance of changes detected
- Trading decision confidence

Clearly state: EMAIL ALERT DECISION: YES or EMAIL ALERT DECISION: NO

==================================================

Instructions:
1. Synthesize all analyses into a coherent trading decision
2. Highlight areas of agreement and disagreement
3. Provide specific price targets and risk levels when mentioned
4. Be objective and balanced in your assessment
5. Focus on actionable trading insights
6. Email alerts should be sent for significant changes that traders need to act on
"""

            # Helper to call the model with retries/backoff for transient errors
            def _call_with_backoff(prompt_text, max_attempts=5, base_delay=1.0):
                last_exception = None
                for attempt in range(1, max_attempts + 1):
                    try:
                        logger.info(f"Google AI multi-provider consolidation attempt {attempt}/{max_attempts} for {stock_symbol}")
                        resp = self.model.generate_content(prompt_text)
                        
                        text = getattr(resp, 'text', None)
                        if text:
                            return text
                        
                        if isinstance(resp, dict) and 'content' in resp:
                            return resp['content']
                        
                        logger.error("Empty response from Google AI (no text/content)")
                        raise RuntimeError("Empty response from Google AI")
                        
                    except Exception as e:
                        last_exception = e
                        msg = str(e).lower()
                        
                        is_retryable = any(keyword in msg for keyword in [
                            '429', 'resource exhausted', 'rate limit', 'quota', 
                            'ratelimit', 'too many requests'
                        ])
                        
                        if is_retryable and attempt < max_attempts:
                            sleep_time = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1)
                            logger.warning(
                                f"Rate limit error (attempt {attempt}/{max_attempts}): {e}. "
                                f"Retrying in {sleep_time:.1f}s"
                            )
                            time.sleep(sleep_time)
                            continue
                        else:
                            logger.error(f"Google AI error (attempt {attempt}/{max_attempts}): {e}")
                            raise
                
                raise RuntimeError(
                    f"Google AI generate_consolidated_decision_multi failed after {max_attempts} attempts. "
                    f"Last error: {last_exception}"
                )

            consolidated_text = _call_with_backoff(prompt)
            return consolidated_text
        except Exception as e:
            logger.error(f"Google AI API error in multi-provider consolidation: {e}")
            raise


class GrokAnalyzer(BaseAnalyzer):
    """Class to handle screenshot analysis using Grok API via OpenAI-compatible interface"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Grok analyzer
        
        Args:
            api_key: Grok API key. If None, will try to get from environment variable
        """
        if not OPENAI_AVAILABLE or OpenAI is None:
            raise ImportError("openai package is required. Install with: pip install openai")
        
        super().__init__(api_key)
        
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv('GROK_API_KEY')
        
        if not self.api_key:
            raise ValueError("Grok API key is required. Set GROK_API_KEY environment variable or pass api_key parameter")
        
        # Get model from environment variable or use default
        self.model = os.getenv('GROK_MODEL', 'grok-2')
        
        # Initialize the OpenAI client with Grok's endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.x.ai/v1"
        )
    
    def analyze_screenshots(self, messages: list) -> str:
        """Analyze screenshots using Grok API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4000,
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Grok API error: {e}")
            raise


class OpenAIAnalyzer(BaseAnalyzer):
    """Class to handle screenshot analysis using OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI analyzer
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable
        """
        if not OPENAI_AVAILABLE or OpenAI is None:
            raise ImportError("openai package is required. Install with: pip install openai")
        
        super().__init__(api_key)
        
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter")
        
        # Get model from environment variable or use default
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o')
        
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=self.api_key)
    
    def analyze_screenshots(self, messages: list) -> str:
        """Analyze screenshots using OpenAI API"""
        try:
            # gpt-5.x models use max_completion_tokens instead of max_tokens
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.2
            }
            
            if "gpt-5" in self.model.lower():
                kwargs["max_completion_tokens"] = 4000
            else:
                kwargs["max_tokens"] = 4000
            
            logger.info(f"[DEBUG] OpenAI calling model: {self.model}")
            response = self.client.chat.completions.create(**kwargs)
            
            # Debug: log response structure
            logger.info(f"[DEBUG] OpenAI response type: {type(response)}")
            logger.info(f"[DEBUG] OpenAI response.choices: {len(response.choices) if response.choices else 0}")
            if response.choices:
                logger.info(f"[DEBUG] OpenAI choice[0].message: {response.choices[0].message}")
                logger.info(f"[DEBUG] OpenAI content type: {type(response.choices[0].message.content)}")
                logger.info(f"[DEBUG] OpenAI content length: {len(response.choices[0].message.content) if response.choices[0].message.content else 0}")
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
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
        self.google_chart_enabled = os.getenv('GOOGLE_AI_CHART_ENABLED', 'False').lower() == 'true'
        self.google_consolidation_enabled = os.getenv('GOOGLE_AI_CONSOLIDATION_ENABLED', 'False').lower() == 'true'
        self.grok_enabled = os.getenv('GROK_ENABLED', 'False').lower() == 'true'
        self.openai_enabled = os.getenv('OPENAI_ENABLED', 'False').lower() == 'true'
        
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
            if perplexity_key:
                try:
                    self.providers['perplexity'] = PerplexityAnalyzer(perplexity_key)
                    logger.info("Perplexity provider enabled")
                except Exception as e:
                    logger.error(f"Failed to initialize Perplexity analyzer: {e}")
                    self.perplexity_enabled = False
            else:
                logger.warning("PERPLEXITY_ENABLED=True but PERPLEXITY_API_KEY not found")
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
        if self.google_chart_enabled:
            google_key = os.getenv('GOOGLE_AI_API_KEY')
            if google_key:
                try:
                    self.google_analyzer = GoogleAIAnalyzer(google_key)
                    self.providers['google'] = self.google_analyzer
                    logger.info("Google AI chart analyzer enabled")
                except Exception as e:
                    logger.error(f"Failed to initialize Google AI analyzer: {e}")
                    self.google_chart_enabled = False
            else:
                logger.warning("GOOGLE_AI_CHART_ENABLED=True but GOOGLE_AI_API_KEY not found")
                self.google_chart_enabled = False
        
        # Initialize Google AI for consolidation even if chart analysis is disabled
        if self.google_consolidation_enabled and not self.google_analyzer:
            google_key = os.getenv('GOOGLE_AI_API_KEY')
            if google_key:
                try:
                    self.google_analyzer = GoogleAIAnalyzer(google_key)
                    logger.info("Google AI consolidation analyzer enabled")
                except Exception as e:
                    logger.error(f"Failed to initialize Google AI consolidation analyzer: {e}")
                    self.google_consolidation_enabled = False
            else:
                logger.warning("GOOGLE_AI_CONSOLIDATION_ENABLED=True but GOOGLE_AI_API_KEY not found")
                self.google_consolidation_enabled = False
        
        # Check Grok setup
        if self.grok_enabled:
            grok_key = os.getenv('GROK_API_KEY')
            if grok_key:
                try:
                    self.providers['grok'] = GrokAnalyzer(grok_key)
                    logger.info("Grok provider enabled")
                except Exception as e:
                    logger.error(f"Failed to initialize Grok analyzer: {e}")
                    self.grok_enabled = False
            else:
                logger.warning("GROK_ENABLED=True but GROK_API_KEY not found")
                self.grok_enabled = False
        
        # Check OpenAI setup
        if self.openai_enabled:
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key:
                try:
                    self.providers['openai'] = OpenAIAnalyzer(openai_key)
                    logger.info("OpenAI provider enabled")
                except Exception as e:
                    logger.error(f"Failed to initialize OpenAI analyzer: {e}")
                    self.openai_enabled = False
            else:
                logger.warning("OPENAI_ENABLED=True but OPENAI_API_KEY not found")
                self.openai_enabled = False
        
        if not self.providers:
            logger.warning("No AI providers enabled or properly configured. Check API keys and enable flags.")
    
    def _run_single_provider(self, provider_name: str, screenshot_data: dict, output_dir: str, stock_symbol: str):
        """
        Run analysis for a single provider (used for parallel execution)
        
        Returns:
            Tuple of (provider_name, analysis_text, change_analysis)
        """
        logger.info(f"Running analysis with {provider_name.title()}")
        
        try:
            if provider_name == 'google':
                # Use Google AI analyzer for chart analysis
                analysis_text, change_analysis = self._analyze_with_google_ai(
                    screenshot_data, output_dir, stock_symbol
                )
            else:
                # Use custom provider (Perplexity, Claude, Grok, OpenAI, etc.) - skip prior analysis
                analysis_text, change_analysis = self._analyze_with_custom_provider(
                    screenshot_data, output_dir, stock_symbol, provider_name, prior_analysis=None
                )
        except Exception as e:
            logger.error(f"Error running {provider_name} analysis: {e}")
            analysis_text, change_analysis = None, None
        
        return provider_name, analysis_text, change_analysis

    def analyze_with_trend_alerts(self, screenshot_data: dict, output_dir: str = None, stock_symbol: str = None):
        """
        Main analysis method that runs all enabled AI providers IN PARALLEL
        """
        if not self.providers:
            logger.error("No AI providers enabled")
            return None, None
        
        results = {}
        combined_analysis = None
        combined_change_analysis = None
        
        # Run all enabled providers IN PARALLEL using ThreadPoolExecutor
        provider_names = list(self.providers.keys())
        logger.info(f"Starting parallel analysis with {len(provider_names)} providers: {provider_names}")
        
        with ThreadPoolExecutor(max_workers=len(provider_names)) as executor:
            # Submit all provider tasks
            future_to_provider = {
                executor.submit(
                    self._run_single_provider, 
                    provider_name, 
                    screenshot_data, 
                    output_dir, 
                    stock_symbol
                ): provider_name 
                for provider_name in provider_names
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_provider):
                provider_name = future_to_provider[future]
                try:
                    pname, analysis_text, change_analysis = future.result()
                    
                    logger.info(f"[DEBUG PRE-CHECK] {pname}: analysis_text={type(analysis_text).__name__}, change_analysis={type(change_analysis).__name__}")
                    logger.info(f"[DEBUG PRE-CHECK] {pname}: bool(analysis_text)={bool(analysis_text)}, bool(change_analysis)={bool(change_analysis)}")
                    
                    if analysis_text and change_analysis:
                        results[pname] = {
                            'analysis_text': analysis_text,
                            'change_analysis': change_analysis
                        }
                        logger.info(f"[DEBUG] Added {pname} to results (analysis_text length: {len(analysis_text)}, change_analysis keys: {list(change_analysis.keys()) if change_analysis else 'None'})")
                        
                        # For the first successful analysis, use as base
                        if combined_analysis is None:
                            combined_analysis = analysis_text
                            combined_change_analysis = change_analysis
                    else:
                        logger.warning(f"[DEBUG] {pname} returned invalid data - analysis_text: {analysis_text is not None}, change_analysis: {change_analysis is not None}")
                except Exception as e:
                    logger.error(f"Exception getting result from {provider_name}: {e}")
        
        logger.info(f"Parallel analysis complete. Successful providers: {list(results.keys())}")
        
        # Combine all provider results into final output
        if results:
            logger.info(f"[DEBUG] Results contains {len(results)} providers: {list(results.keys())}")
            return self._combine_multi_provider_results(results, screenshot_data, output_dir, stock_symbol)
        else:
            logger.warning("No successful analyses from any provider")
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
            change_analysis = result.get('change_analysis')
            if not change_analysis or not isinstance(change_analysis, dict):
                logger.warning(f"No valid change_analysis for provider {provider_name}, skipping consensus stats.")
                continue
            # Collect probabilities and alerts for consensus
            # Use 'is not None' to include 0 values
            prob = change_analysis.get('trend_change_probability')
            if prob is not None:
                all_probabilities.append(prob)
            if change_analysis.get('has_changes'):
                all_alerts.append({
                    'provider': provider_name,
                    'alert_level': change_analysis.get('alert_level', 'unknown'),
                    'summary': change_analysis.get('summary', ''),
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

        # Generate Google AI consolidated trading decision FIRST (if enabled)
        results_list = [(provider_name, result['analysis_text'], result['change_analysis']) 
                      for provider_name, result in results.items()]
        
        trading_decision = None
        google_ai_wants_email = False
        
        if self.google_consolidation_enabled:
            trading_decision = self._generate_consolidated_trading_decision(results_list, avg_probability, all_alerts, stock_symbol, output_dir, screenshot_data)
            # Parse Google AI's email alert decision from the consolidated decision text
            google_ai_wants_email = self._parse_google_ai_email_decision(trading_decision)
        
        if trading_decision:
            html.append("<div class='divider'></div>")
            html.append("<h2>Google AI Consolidated Trading Decision</h2>")
            html.append(f"<div class='section'><pre style='white-space:pre-wrap;font-family:inherit;font-size:1.08em;background:#f6f8fa;padding:1em;border-radius:6px;border:1px solid #eee'>{trading_decision.strip()}</pre></div>")

        # Add individual provider analyses in desired order: Claude, Perplexity, Google
        provider_order = ['claude', 'perplexity', 'google']
        section_titles = {
            'claude': 'Claude Analysis',
            'perplexity': 'Perplexity Analysis',
            'google': 'Google AI Analysis'
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
            from config import Paths
            print(f"[DEBUG] Attempting to save HTML report for {stock_symbol}...")
            print(f"[DEBUG] Current working directory: {os.getcwd()}")
            print(f"[DEBUG] Data directory: {Paths.DATA_DIR}")
            symbol_dir = os.path.join(Paths.SCREENSHOTS_DIR, stock_symbol)
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
                print("   [EMAIL] Google AI Consensus: Evaluating email alert...")
                email_manager = EmailAlertManager()
                
                if email_manager.is_configured and consensus_change_analysis.get('has_changes', False):
                    print(f"   [EMAIL] Sending email alert from Google AI consensus")
                    print(f"   [DATA] Alert Level: {consensus_change_analysis.get('alert_level', 'unknown').upper()}")
                    print(f"   [DATA] Probability: {consensus_change_analysis.get('trend_change_probability', 0):.1f}%")
                    
                    email_sent = email_manager.send_trend_alert(consensus_change_analysis, ''.join(html), stock_symbol, output_dir)
                    
                    if email_sent:
                        print(f"   [OK] Email alert sent successfully from Google AI consensus")
                    else:
                        print(f"   [WARN] Email alert failed to send")
                        logger.warning("Google AI consensus email alert failed to send")
                elif not email_manager.is_configured:
                    print("   [EMAIL] Email alerts not configured (check .env settings)")
                else:
                    print(f"   [EMAIL] No email sent - no significant changes detected by Google AI consensus")
            except Exception as e:
                print(f"   [ERROR] Error sending Google AI consensus email alert: {e}")
                logger.error(f"Failed to send Google AI consensus email alert: {e}")
        except Exception as e:
            print(f"[ERROR] Failed to write HTML report for {stock_symbol}: {e}")
            import traceback
            traceback.print_exc()
            logger.error(f"Failed to write HTML report for {stock_symbol}: {e}")
        
        # Generate text version with provider headers for the txt file
        text_analysis = []
        
        # Add Google AI trading decision if available
        if trading_decision:
            text_analysis.append("GOOGLE AI CONSOLIDATED TRADING DECISION")
            text_analysis.append("=" * 60)
            text_analysis.append(trading_decision.strip())
            text_analysis.append("")
        
        # Add individual provider analyses with headers
        provider_order = ['claude', 'perplexity', 'google']
        section_titles = {
            'claude': 'CLAUDE ANALYSIS',
            'perplexity': 'PERPLEXITY ANALYSIS',
            'google': 'GOOGLE AI ANALYSIS'
        }
        
        for provider_name in provider_order:
            if provider_name in results:
                result = results[provider_name]
                analysis = result['analysis_text']
                text_analysis.append(section_titles[provider_name])
                text_analysis.append("=" * 60)
                text_analysis.append(analysis.strip())
                text_analysis.append("")
        
        # Add any other providers not in the ordered list (Grok, OpenAI, etc.)
        for provider_name, result in results.items():
            if provider_name not in provider_order:
                analysis = result['analysis_text']
                text_analysis.append(f"{provider_name.upper()} ANALYSIS")
                text_analysis.append("=" * 60)
                text_analysis.append(analysis.strip())
                text_analysis.append("")
        
        # Add consensus summary at the end
        text_analysis.append("MULTI-PROVIDER CONSENSUS SUMMARY")
        text_analysis.append("=" * 60)
        if all_probabilities:
            text_analysis.append(f"Average Trend Change Probability: {avg_probability:.1f}%")
            text_analysis.append(f"Probability Range: {min_probability:.1f}% - {max_probability:.1f}%")
            text_analysis.append(f"Providers Used: {len(results)}")
            text_analysis.append("")
        
        if all_alerts:
            text_analysis.append(f"Alerts from {len(all_alerts)} provider(s):")
            for alert in all_alerts:
                text_analysis.append(f"  - {alert['provider'].title()}: {alert['alert_level'].upper()} ({alert['probability']}%) - {alert['summary']}")
            text_analysis.append("")
        
        combined_text = "\n".join(text_analysis)
        return combined_text, consensus_change_analysis
    
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
                print(f"   [EMAIL] Google AI Decision: SEND EMAIL ALERT (matched: '{pattern}')")
                return True
        
        for pattern in no_patterns:
            if pattern in decision_text:
                from trading_analysis import logger
                logger.info(f"Google AI email decision: DO NOT SEND (matched pattern: '{pattern}')")
                print(f"   [EMAIL] Google AI Decision: NO EMAIL (matched: '{pattern}')")
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
            print("   [EMAIL] Google AI Decision: SEND EMAIL ALERT (based on bullish signals)")
            return True
        
        # If there's significant bearish content with warning keywords, also alert
        if ("WARNING" in decision_text or "CAUTION" in decision_text) and bearish_count > 0:
            from trading_analysis import logger
            logger.info("Google AI email decision: SEND (based on bearish warnings)")
            print("   [EMAIL] Google AI Decision: SEND EMAIL ALERT (based on bearish warnings)")
            return True
        
        # No clear pattern found - default to False for safety
        from trading_analysis import logger
        logger.info("Google AI email decision: UNCLEAR (defaulting to NO)")
        print("   [WARN] Google AI Decision: UNCLEAR (defaulting to NO EMAIL)")
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
            
            # Extract all provider analyses dynamically
            provider_analyses = {}
            for provider_name, analysis_text, change_analysis in results:
                provider_analyses[provider_name.lower()] = analysis_text
            
            # Generate consolidated decision using Google AI with all available providers
            if provider_analyses:
                consolidated_decision = google_analyzer.generate_consolidated_decision_multi(
                    provider_analyses, stock_symbol, output_dir, screenshot_data
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
            
            print(f"   [AI] Analyzing {len(valid_screenshots)} screenshots with Google AI...")
            
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
            
            if 'utbot' in window_types or 'ut bot' in str(window_types).lower() or 'lorentzian' in str(window_types).lower():
                chart_context += """
CHART CONTEXT - UT Bot -Lorentzian Window:
This chart displays the following technical indicators:
- UT Bot Alert: Trend-following indicator with BUY/SELL signals based on ATR trailing stop
- Lorentzian Classification: Machine learning-based trend classification using Lorentzian distance
- Signal Line: Dynamic support/resistance based on ATR
- Trend Direction: Color-coded candles showing bullish (green) or bearish (red) trend

Pay special attention to:
- UT Bot BUY/SELL signals (triangles or arrows marking entry points)
- Lorentzian classification predictions (bullish/bearish probability)
- Signal line crossovers (price crossing above/below the UT Bot line)
- Trend color changes (transition from red to green or vice versa)
- Confluence of UT Bot signals with Lorentzian predictions
- Recent signal history and signal frequency
- ATR-based stop loss levels indicated by the trailing line

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
- For UT Bot -Lorentzian chart: UT Bot BUY/SELL signals, Lorentzian classification, signal line position, trend direction
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
            
            logger.info(f"Successfully analyzed {len(image_data_uris)} screenshots with Google AI")
            self._handle_alerts(change_analysis, analysis_text, stock_symbol, output_dir, 'google')
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
                print(f"   [DATA] Using prior analysis for comparison")
            else:
                print(f"   [DATA] Analyzing current state only (no prior comparison)")

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
            
            print(f"   [AI] Analyzing {len(image_data_uris)} screenshots with {provider_name.title()}...")
            
            # Make API request using our provider
            result = ai_provider.analyze_screenshots(messages)
            logger.info(f"Successfully analyzed {len(image_data_uris)} screenshots with {provider_name}")
            
            # Debug: log raw result length and first 200 chars
            logger.info(f"[DEBUG] {provider_name} raw result length: {len(result) if result else 0}")
            logger.info(f"[DEBUG] {provider_name} raw result preview: {result[:300] if result else 'None'}...")
            
            # Parse response using original method
            analysis_text, change_analysis = self.original_analyzer._parse_response(result, prior_analysis)
            
            # Debug: log parsed result
            logger.info(f"[DEBUG] {provider_name} parsed analysis_text length: {len(analysis_text) if analysis_text else 0}")
            
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
        
        if change_analysis and change_analysis.get('has_changes'):
            alert_level = change_analysis.get('alert_level', 'unknown').upper()
            probability = change_analysis.get('trend_change_probability', 0)
            summary = change_analysis.get('summary', 'N/A')
            print(f"   [ALERT] {alert_level} ALERT{provider_label}: {summary}")
            print(f"   [DATA] Trend Change Probability: {probability}%")
            print(f"   [EMAIL] Email will be sent from Google AI consensus (not individual providers)")
        else:
            probability = change_analysis.get('trend_change_probability', 0) if change_analysis else 0
            print(f"   [OK] No significant trend changes detected{provider_label} (Probability: {probability}%)")
    
    def save_combined_analysis_report(self, screenshot_data, analysis, output_dir, change_analysis):
        """Delegate to original analyzer"""
        return self.original_analyzer.save_combined_analysis_report(screenshot_data, analysis, output_dir, change_analysis)