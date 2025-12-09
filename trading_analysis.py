"""
AI Trading Analysis module for screenshot analysis with email alerts
Supports multiple AI providers through a unified interface
"""
# Standard library imports
import logging
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any

# Local imports
from utils import encode_image_to_base64, ensure_directory_exists
from prompts import get_analysis_prompt

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
        
        # Get model from environment variable or use default
        self.model = os.getenv('PERPLEXITY_MODEL', 'sonar-pro')
        
        # Initialize the OpenAI client with Perplexity's endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.perplexity.ai"
        )
    
    def encode_image_to_base64(self, image_path: str) -> str:
        """
        Encode an image file to base64 string (delegates to shared utility)
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image as data URI
        """
        return encode_image_to_base64(image_path)
    
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
            
            print(f"   [AI] Analyzing {len(image_data_uris)} screenshots...")
            
            # Make API request
            completion = self.client.chat.completions.create(
                model=self.model,
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
            
            # Display change detection results (email sending moved to Google AI consensus)
            if change_analysis['has_changes']:
                alert_level = change_analysis['alert_level'].upper()
                probability = change_analysis.get('trend_change_probability', 0)
                print(f"   [ALERT] {alert_level}: {change_analysis['summary']}")
                print(f"   [DATA] Trend Change Probability: {probability}%")
                print(f"   [EMAIL] Email will be sent from Google AI consensus (not individual providers)")
            else:
                probability = change_analysis.get('trend_change_probability', 0)
                print(f"   [OK] No significant trend changes detected (Probability: {probability}%)")
            
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
        """Create analysis prompt using centralized configurable prompts"""
        return get_analysis_prompt(window_types, prior_analysis, stock_symbol)
    
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
                        # 'has_changes' is only relevant for consensus/Google AI, not Perplexity/Claude
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
            
            ensure_directory_exists(output_dir)
            
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
                    
                    f.write(f"[DATA] Trend Change Probability: {probability}%\n")
                    f.write(f"[>>] Confidence Level: {confidence.upper()}\n")
                    f.write(f"[ALERT] Status: {'ALERT' if has_changes else 'NO ALERT'} ({alert_level.upper()})\n")
                    
                    if 'summary' in change_analysis:
                        f.write(f"[SUMMARY] {change_analysis['summary']}\n")
                    
                    f.write(f"\n")
                
                f.write(f"Combined Analysis Results:\n")
                f.write(f"=" * 40 + "\n")
                f.write(analysis)
                f.write(f"\n\n")
            
            logger.info(f"Combined analysis report saved: {report_path}")
            print(f"   [REPORT] Saved to: {os.path.basename(report_path)}")
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
        if not self.is_configured:
            logger.warning("Email not configured - skipping alert")
            return False
        
        if not change_analysis.get('has_changes', False):
            logger.info("No significant changes - no email needed")
            return True
        
        try:
            subject = self._create_email_subject(change_analysis, stock_symbol)
            body = self._create_email_body(change_analysis, current_analysis, stock_symbol)
            
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = self.email_to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Use context manager to ensure connection is properly closed
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.sendmail(self.email_user, self.email_to, msg.as_string())
            
            logger.info(f"Email sent successfully to {self.email_to}")
            print(f"   [EMAIL] Alert sent to {self.email_to}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            print(f"   [ERROR] Email authentication failed - check credentials")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending email: {e}")
            print(f"   [ERROR] Failed to send email: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email: {e}")
            print(f"   [ERROR] Failed to send email: {e}")
            return False
    
    def _create_email_subject(self, change_analysis: Dict[str, Any], stock_symbol: str) -> str:
        """Create email subject line"""
        alert_level = change_analysis.get('alert_level', 'low').upper()
        symbol_text = f" - {stock_symbol}" if stock_symbol else ""
        
        if alert_level == 'CRITICAL':
            return f"[CRITICAL] STOCK ALERT{symbol_text} - Major Trend Changes"
        elif alert_level == 'HIGH':
            return f"[WARN] HIGH STOCK ALERT{symbol_text} - Significant Changes"
        elif alert_level == 'MEDIUM':
            return f"[DATA] MEDIUM STOCK ALERT{symbol_text} - Notable Changes"
        else:
            return f"[INFO] Stock Update{symbol_text} - Changes Detected"
    
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
        body += f"\n---\nThis alert was generated automatically by AI Trading Analysis."
        
        return body