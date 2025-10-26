"""
Perplexity API integration module for screenshot analysis with email alerts
"""
import base64
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
import logging
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    print("Warning: openai package not installed. Please install it with: pip install openai")
    OpenAI = None
    OPENAI_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerplexityAnalyzer:
    """Class to handle screenshot analysis using Perplexity API via OpenAI-compatible interface"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Perplexity analyzer
        
        Args:
            api_key: Perplexity API key. If None, will try to get from environment variable
        """
        if not OPENAI_AVAILABLE or OpenAI is None:
            raise ImportError("openai package is required. Install with: pip install openai")
        
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        
        if not self.api_key:
            raise ValueError("Perplexity API key is required. Set PERPLEXITY_API_KEY environment variable or pass api_key parameter")
        
        # Initialize the OpenAI client with Perplexity's endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.perplexity.ai"
        )
    
    def encode_image_to_base64(self, image_path: str) -> str:
        """
        Encode an image file to base64 string
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image as data URI
        """
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            
            # Determine the MIME type based on file extension
            file_ext = os.path.splitext(image_path)[1].lower()
            if file_ext == '.png':
                mime_type = 'image/png'
            elif file_ext in ['.jpg', '.jpeg']:
                mime_type = 'image/jpeg'
            else:
                mime_type = 'image/png'  # Default to PNG
            
            image_data_uri = f"data:{mime_type};base64,{base64_image}"
            return image_data_uri
            
        except Exception as e:
            logger.error(f"Error encoding image {image_path}: {e}")
            raise
    
    def analyze_with_trend_alerts(self, screenshot_data: Dict[str, str], output_dir: str = None, stock_symbol: str = None):
        """
        Analyze screenshots with trend change detection and email alerts
        
        Args:
            screenshot_data: Dictionary with window_type as key and image_path as value
            output_dir: Directory where analysis reports are stored
            stock_symbol: Optional stock symbol for alerts
            
        Returns:
            Tuple of (combined analysis result as string, trend change analysis dict), or (None, None) if analysis failed
        """
        try:
            # Filter out None/empty paths
            valid_screenshots = {k: v for k, v in screenshot_data.items() if v and os.path.exists(v)}
            
            if not valid_screenshots:
                logger.warning("No valid screenshots found for analysis")
                return None, None

            # Load prior analysis for comparison
            prior_analysis = self._load_prior_analysis(output_dir, valid_screenshots, stock_symbol)
            
            if prior_analysis:
                print(f"   📋 Loaded prior analysis for comparison")
            else:
                print(f"   📋 No prior analysis found - this will be the initial analysis")

            # Encode all images
            image_data_uris = {}
            for window_type, image_path in valid_screenshots.items():
                try:
                    image_data_uris[window_type] = self.encode_image_to_base64(image_path)
                except Exception as e:
                    logger.error(f"Failed to encode {window_type} image {image_path}: {e}")
                    continue
            
            if not image_data_uris:
                logger.error("Failed to encode any images")
                return None, None
            
            # Create comprehensive prompt
            prompt = self._create_analysis_prompt(list(image_data_uris.keys()), prior_analysis, stock_symbol)
            
            # Build content array with text prompt and all images
            content = [{"type": "text", "text": prompt}]
            
            # Add all images to the content
            for window_type, image_uri in image_data_uris.items():
                content.append({
                    "type": "image_url", 
                    "image_url": {"url": image_uri}
                })
            
            print(f"   🤖 Analyzing {len(image_data_uris)} screenshots...")
            
            # Make API request
            completion = self.client.chat.completions.create(
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
            
            # Parse the response
            analysis_text, change_analysis = self._parse_response(result, prior_analysis)
            
            # Display change detection results
            if change_analysis['has_changes']:
                alert_level = change_analysis['alert_level'].upper()
                probability = change_analysis.get('trend_change_probability', 0)
                print(f"   🚨 {alert_level} ALERT: {change_analysis['summary']}")
                print(f"   📊 Trend Change Probability: {probability}%")
                
                # Send email alert if configured
                email_manager = EmailAlertManager()
                if email_manager.is_configured:
                    email_sent = email_manager.send_trend_alert(change_analysis, analysis_text, stock_symbol, output_dir)
                    if not email_sent:
                        print(f"   ⚠️ Email alert failed to send")
                else:
                    print(f"   📧 Email alerts not configured")
            else:
                probability = change_analysis.get('trend_change_probability', 0)
                print(f"   ✅ No significant trend changes detected (Probability: {probability}%)")
            
            return analysis_text, change_analysis
            
        except Exception as e:
            logger.error(f"Error in trend analysis: {e}")
            return None, None
    
    def _load_prior_analysis(self, output_dir: str, valid_screenshots: Dict[str, str], current_stock_symbol: str = None) -> Optional[str]:
        """Load the previous analysis report for comparison"""
        try:
            if output_dir is None:
                for path in valid_screenshots.values():
                    if path and os.path.exists(path):
                        output_dir = os.path.dirname(path)
                        break
                
                if output_dir is None:
                    output_dir = "screenshots"
            
            prior_report_path = os.path.join(output_dir, "combined_analysis_latest.txt")
            
            if os.path.exists(prior_report_path):
                with open(prior_report_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract just the analysis part
                analysis_start = content.find("Combined Analysis Results:")
                if analysis_start != -1:
                    equals_line = content.find("=" * 40, analysis_start)
                    if equals_line != -1:
                        analysis_content = content[equals_line + 40:].strip()
                        if analysis_content:
                            logger.info("Loaded prior analysis for comparison")
                            return analysis_content
                
                logger.info("Prior analysis file found but could not extract content")
                return None
            else:
                logger.info("No prior analysis file found")
                return None
                
        except Exception as e:
            logger.warning(f"Error loading prior analysis: {e}")
            return None
    
    def _create_analysis_prompt(self, window_types: list, prior_analysis: str = None, stock_symbol: str = None) -> str:
        """Create analysis prompt"""
        symbol_text = f" for {stock_symbol}" if stock_symbol else ""
        email_threshold = int(os.getenv('EMAIL_ALERT_THRESHOLD', '60'))
        
        # Create chart-specific context
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

Pay special attention to:
- Smoothed Heiken Ashi candle colors (bullish/bearish trends)
- HEMA trend direction and crossovers
- Divergence signals (bullish/bearish divergences)
- Trend strength and momentum
- Reversal patterns indicated by divergences

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
        
        base_prompt = f"""
You are an expert stock market analyst. Analyze these {len(window_types)} chart screenshots{symbol_text}.

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
- Moving averages, oscillators, volume data, support/resistance levels

**CRITICAL SIGNALS**
Most important actionable signals (include any +RD or -RD formations, MS overbought/oversold conditions if present)

**TRADING DECISION**
Clear BUY/SELL/HOLD with rationale

**TREND CHANGE EVALUATION**
"""

        if prior_analysis:
            trend_prompt = f"""
Compare with prior analysis and evaluate changes.

Prior: {prior_analysis[:500]}...

**RESPONSE FORMAT:**
=== ANALYSIS ===
[Your analysis here]

=== TREND_EVALUATION ===
{{
    "send_email": true/false,
    "alert_level": "critical/high/medium/low",
    "trend_change_probability": 85,
    "confidence_level": "very_high/high/medium/low",
    "summary": "Brief explanation",
    "key_changes": ["change1", "change2"],
    "probability_reasoning": "Why this probability"
}}

Rules: Send email only if probability >= {email_threshold}%
"""
        else:
            trend_prompt = f"""
This is the INITIAL ANALYSIS.

=== ANALYSIS ===
[Your analysis]

=== TREND_EVALUATION ===
{{
    "send_email": false,
    "alert_level": "info",
    "trend_change_probability": 0,
    "confidence_level": "high",
    "summary": "Initial analysis - no prior data",
    "key_changes": [],
    "probability_reasoning": "First analysis session"
}}
"""
        
        return base_prompt + trend_prompt
    
    def _parse_response(self, response: str, prior_analysis: str = None) -> tuple:
        """Parse the response to extract analysis and trend evaluation"""
        try:
            import json
            
            if "=== ANALYSIS ===" in response and "=== TREND_EVALUATION ===" in response:
                analysis_section = response.split("=== ANALYSIS ===")[1].split("=== TREND_EVALUATION ===")[0].strip()
                trend_section = response.split("=== TREND_EVALUATION ===")[1].strip()
                
                json_start = trend_section.find('{')
                json_end = trend_section.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = trend_section[json_start:json_end]
                    trend_data = json.loads(json_str)
                    
                    change_analysis = {
                        'has_changes': trend_data.get('send_email', False),
                        'change_type': 'consolidated_evaluation',
                        'alert_level': trend_data.get('alert_level', 'low'),
                        'trend_change_probability': trend_data.get('trend_change_probability', 0),
                        'confidence_level': trend_data.get('confidence_level', 'low'),
                        'summary': trend_data.get('summary', 'No summary'),
                        'key_changes': trend_data.get('key_changes', []),
                        'probability_reasoning': trend_data.get('probability_reasoning', 'No reasoning')
                    }
                    
                    return analysis_section, change_analysis
            
            # Fallback
            fallback_change_analysis = {
                'has_changes': False,
                'change_type': 'parsing_fallback',
                'alert_level': 'low',
                'trend_change_probability': 0,
                'confidence_level': 'low',
                'summary': 'Analysis completed',
                'key_changes': [],
                'probability_reasoning': 'Could not parse structured response'
            }
            
            return response, fallback_change_analysis
            
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            fallback_change_analysis = {
                'has_changes': False,
                'change_type': 'error',
                'alert_level': 'low',
                'trend_change_probability': 0,
                'confidence_level': 'low',
                'summary': f'Error: {e}',
                'key_changes': [],
                'probability_reasoning': 'Parsing error'
            }
            return response if response else "Analysis failed", fallback_change_analysis
    
    def save_combined_analysis_report(self, screenshot_data: Dict[str, str], analysis: str, output_dir: str = None, change_analysis: Dict[str, Any] = None) -> str:
        """Save the combined analysis report"""
        try:
            if output_dir is None:
                for path in screenshot_data.values():
                    if path and os.path.exists(path):
                        output_dir = os.path.dirname(path)
                        break
                
                if output_dir is None:
                    output_dir = "screenshots"
            
            os.makedirs(output_dir, exist_ok=True)
            
            report_filename = "combined_analysis_latest.txt"
            report_path = os.path.join(output_dir, report_filename)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"Combined Screenshot Analysis Report\n")
                f.write(f"=" * 60 + "\n")
                f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Screenshots Analyzed: {len([v for v in screenshot_data.values() if v])}\n\n")
                
                f.write("Screenshot Sources:\n")
                f.write("-" * 30 + "\n")
                for window_type, image_path in screenshot_data.items():
                    if image_path:
                        f.write(f"- {window_type.replace('_', ' ').title()}: {os.path.basename(image_path)}\n")
                
                if change_analysis:
                    f.write(f"\nTrend Change Analysis:\n")
                    f.write(f"-" * 30 + "\n")
                    probability = change_analysis.get('trend_change_probability', 0)
                    confidence = change_analysis.get('confidence_level', 'unknown')
                    has_changes = change_analysis.get('has_changes', False)
                    alert_level = change_analysis.get('alert_level', 'info')
                    
                    f.write(f"📊 Trend Change Probability: {probability}%\n")
                    f.write(f"🎯 Confidence Level: {confidence.upper()}\n")
                    f.write(f"🚨 Alert Status: {'ALERT' if has_changes else 'NO ALERT'} ({alert_level.upper()})\n")
                    
                    if 'summary' in change_analysis:
                        f.write(f"📋 Summary: {change_analysis['summary']}\n")
                    
                    f.write(f"\n")
                
                f.write(f"Combined Analysis Results:\n")
                f.write(f"=" * 40 + "\n")
                f.write(analysis)
                f.write(f"\n\n")
            
            logger.info(f"Combined analysis report saved: {report_path}")
            print(f"   📄 Report saved to: {os.path.basename(report_path)}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            raise


class EmailAlertManager:
    """Class to handle email alerts for trend changes"""
    
    def __init__(self):
        """Initialize email settings from environment variables"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_to = os.getenv('EMAIL_TO')
        
        self.is_configured = all([
            self.email_user,
            self.email_password, 
            self.email_to
        ])
        
        if not self.is_configured:
            logger.warning("Email alerts not configured. Set EMAIL_USER, EMAIL_PASSWORD, and EMAIL_TO in .env file")
    
    def send_trend_alert(self, change_analysis: Dict[str, Any], current_analysis: str, stock_symbol: str = None, output_dir: str = None) -> bool:
        """Send email alert for detected trend changes"""
        try:
            if not self.is_configured:
                logger.warning("Email not configured - skipping alert")
                return False
            
            if not change_analysis.get('has_changes', False):
                logger.info("No significant changes - no email needed")
                return True
            
            subject = self._create_email_subject(change_analysis, stock_symbol)
            body = self._create_email_body(change_analysis, current_analysis, stock_symbol)
            
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = self.email_to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_user, self.email_to, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {self.email_to}")
            print(f"   📧 Email alert sent to {self.email_to}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            print(f"   ✗ Failed to send email: {e}")
            return False
    
    def _create_email_subject(self, change_analysis: Dict[str, Any], stock_symbol: str) -> str:
        """Create email subject line"""
        alert_level = change_analysis.get('alert_level', 'low').upper()
        symbol_text = f" - {stock_symbol}" if stock_symbol else ""
        
        if alert_level == 'CRITICAL':
            return f"🚨 CRITICAL STOCK ALERT{symbol_text} - Major Trend Changes"
        elif alert_level == 'HIGH':
            return f"⚠️ HIGH STOCK ALERT{symbol_text} - Significant Changes"
        elif alert_level == 'MEDIUM':
            return f"📊 MEDIUM STOCK ALERT{symbol_text} - Notable Changes"
        else:
            return f"📈 Stock Update{symbol_text} - Changes Detected"
    
    def _create_email_body(self, change_analysis: Dict[str, Any], current_analysis: str, stock_symbol: str) -> str:
        """Create email body content"""
        symbol_text = f" for {stock_symbol}" if stock_symbol else ""
        probability = change_analysis.get('trend_change_probability', 0)
        confidence = change_analysis.get('confidence_level', 'unknown')
        
        body = f"""
Stock Analysis Alert{symbol_text}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ALERT LEVEL: {change_analysis.get('alert_level', 'unknown').upper()}

TREND CHANGE PROBABILITY: {probability}% (Confidence: {confidence.upper()})

SUMMARY:
{change_analysis.get('summary', 'No summary available')}

REASONING:
{change_analysis.get('probability_reasoning', 'No reasoning provided')}

KEY CHANGES:
"""
        
        key_changes = change_analysis.get('key_changes', [])
        if key_changes:
            for change in key_changes:
                body += f"- {change}\n"
        else:
            body += "- No specific changes identified\n"
        
        body += f"\n{'='*60}\n"
        body += f"COMPLETE ANALYSIS REPORT\n"
        body += f"{'='*60}\n\n"
        body += f"{current_analysis}\n"
        body += f"\n---\nThis alert was generated automatically by Perplexity AI."
        
        return body
