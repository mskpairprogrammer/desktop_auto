"""
Configurable AI Prompts for Trading Analysis
Edit these prompts to customize AI analysis behavior

To customize prompts:
1. Edit the CHART_CONTEXTS dictionary to add/modify chart-specific instructions
2. Edit BASE_ANALYSIS_PROMPT for the main analysis structure
3. Edit CONSOLIDATION_PROMPT for Google AI consensus logic
"""

import os
from typing import Dict, Optional

# ============================================================================
# CHART-SPECIFIC CONTEXT PROMPTS
# ============================================================================
# Each key corresponds to a window type in the screenshot_data dictionary
# Add or modify chart contexts as needed

CHART_CONTEXTS: Dict[str, str] = {
    "trend_analysis": """
CHART CONTEXT - Trend Analysis Window:
This chart displays LuxAlgo technical indicators. Use the following documentation to analyze it:
- LuxAlgo Signals & Overlays: https://docs.luxalgo.com/docs/algos/signals-overlays/signals
- LuxAlgo Price Action Concepts: https://docs.luxalgo.com/docs/algos/price-action-concepts/introduction

Pay special attention to:
- Signal Quality (Strong Buy/Sell signals)
- Price Action Concepts (Support/Resistance levels, market structure)
- Overlay indicators (trend direction, strength)
- Signal confirmations and divergences
""",

    "heiken_ashi": """
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
""",

    "volume_layout": """
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
""",

    "utbot": """
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
""",

    "workspace": """
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
""",

    # Legacy support for volumeprofile (maps to utbot)
    "volumeprofile": """
CHART CONTEXT - Volume Profile Window:
This chart displays the following technical indicators:
- RVOL (Relative Volume): Volume relative to average
- VOLD Ratio: Volume delta ratio
- MS (Matrix Mod): Overbought/oversold conditions
- TTOB Order Blocks: Trapped trader order blocks

Pay special attention to:
- RVOL levels (high RVOL confirms price moves)
- VOLD ratio for buying/selling pressure
- MS overbought/oversold conditions
- Order block support/resistance zones
""",
}

# ============================================================================
# BASE ANALYSIS PROMPT TEMPLATE
# ============================================================================
# This is the main prompt structure sent to AI providers
# Variables: {num_charts}, {symbol_text}, {chart_context}

BASE_ANALYSIS_PROMPT = """
You are an expert stock market analyst. Analyze these {num_charts} chart screenshots{symbol_text}.

CRITICAL INSTRUCTION: Only analyze what you can clearly see in the screenshots. If a chart window appears blank, contains no data, or is not loaded properly, explicitly state "Chart not loaded" or "No data visible" for that window. DO NOT make assumptions or provide analysis for charts that are not visible or contain no data.

IMPORTANT: Provide a COMPREHENSIVE and DETAILED analysis. Each section should be thorough with specific observations from each chart. Do not summarize or abbreviate - include all relevant details you can observe.

{chart_context}
ANALYSIS FORMAT (provide detailed content for each section):

**MARKET OVERVIEW** (2-3 sentences)
Current price, timeframe, and overall market condition.

**KEY VISIBLE INDICATORS**
Provide DETAILED analysis for each chart. List specific indicators visible with their current readings and interpretations:
- For Trend Analysis chart: LuxAlgo signals, price action concepts, overlays - describe specific signal types, colors, and what they indicate
- For Smoothed Heiken Ashi chart: Heiken Ashi candles, HEMA trend, divergences - describe candle colors, trend direction, any divergence signals
- For Volume Layout chart: Money flow profile, CVD divergence, SQZMOM_LB, MA distance with StdDev bands, +RD/-RD signals - describe each indicator's current state
- For UT Bot -Lorentzian chart: UT Bot BUY/SELL signals, Lorentzian classification, signal line position, trend direction - describe signal types, colors, and ML predictions
- For Symbolik Workspace chart: ATM chart lines, ATM Elliott Waves/Projections, ATM Pressure alerts, TKT analysis/score, Variable Aggressive Sequential (Demark) - describe wave counts, projections, and sequential numbers
- Moving averages, oscillators, volume data, support/resistance levels - include specific price levels where visible

**CRITICAL SIGNALS**
Most important actionable signals (include any +RD or -RD formations, MS overbought/oversold conditions, ATM chart line alignments, Demark Sequential 9s or 13s if present). Be specific about what you see and why it matters.

**TRADING DECISION**
Clear BUY/SELL/HOLD with detailed rationale based on the indicators analyzed above.

**TREND CHANGE EVALUATION**
"""

# ============================================================================
# TREND EVALUATION PROMPTS
# ============================================================================

TREND_EVAL_WITH_PRIOR = """
Compare with prior analysis and evaluate changes.

Prior: {prior_analysis}...

**RESPONSE FORMAT:**
=== ANALYSIS ===
[Your analysis here]

=== TREND_EVALUATION ===
{{
    "alert_level": "critical/high/medium/low",
    "trend_change_probability": 85,
    "confidence_level": "very_high/high/medium/low",
    "summary": "Brief explanation",
    "key_changes": ["change1", "change2"],
    "probability_reasoning": "Why this probability"
}}

Rules: Send email only if probability >= {email_threshold}%
"""

TREND_EVAL_INITIAL = """
This is the INITIAL ANALYSIS.

=== ANALYSIS ===
[Your analysis]

=== TREND_EVALUATION ===
{{
    "alert_level": "info",
    "trend_change_probability": 0,
    "confidence_level": "high",
    "summary": "Initial analysis - no prior data",
    "key_changes": [],
    "probability_reasoning": "First analysis session"
}}
"""

# ============================================================================
# GOOGLE AI CONSOLIDATION PROMPT
# ============================================================================

CONSOLIDATION_PROMPT = """
You are an expert financial analyst tasked with creating a consolidated trading decision based on analyses from multiple AI providers.

**SYMBOL:** {symbol}

**INDIVIDUAL AI PROVIDER ANALYSES:**
{all_analyses}

**YOUR TASK:**
1. Review all provider analyses above
2. Identify consensus and disagreements
3. Weight the most reliable signals
4. Create a FINAL consolidated analysis

**REQUIRED OUTPUT FORMAT:**

=== CONSOLIDATED ANALYSIS ===

**CONSENSUS OVERVIEW**
Summary of where providers agree/disagree.

**KEY TECHNICAL LEVELS**
- Support: [levels from multiple providers]
- Resistance: [levels from multiple providers]

**SIGNAL ALIGNMENT**
Which signals are confirmed across multiple providers vs single-provider signals.

**CONSOLIDATED TRADING DECISION**
[STRONG BUY / BUY / HOLD / SELL / STRONG SELL]
Confidence: [HIGH/MEDIUM/LOW]
Rationale: [Why this decision based on multi-provider consensus]

**RISK ASSESSMENT**
Key risks and stop-loss recommendations.

=== EMAIL ALERT DECISION ===

Based on the consolidated analysis above, should an email alert be sent to notify the trader?

Consider:
- Significance of the signals (are there actionable opportunities?)
- Provider consensus (do multiple providers agree?)
- Risk/reward profile
- Urgency of the situation

**EMAIL ALERT DECISION: [YES/NO]**
**REASON:** [Brief explanation for the decision]

If YES, the email should highlight:
- Primary trading signal
- Key support/resistance levels
- Recommended action
- Risk considerations
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_chart_context(window_types: list) -> str:
    """
    Build chart context string from window types
    
    Args:
        window_types: List of window type strings (e.g., ['trend_analysis', 'heiken_ashi'])
    
    Returns:
        Combined chart context string
    """
    chart_context = ""
    window_types_lower = [w.lower() for w in window_types]
    window_types_str = str(window_types).lower()
    
    for key, context in CHART_CONTEXTS.items():
        # Check if this chart type is in the window types
        if key in window_types_lower:
            chart_context += context + "\n"
        # Special handling for utbot variations
        elif key == "utbot" and ("ut bot" in window_types_str or "lorentzian" in window_types_str):
            chart_context += context + "\n"
    
    return chart_context


def get_analysis_prompt(window_types: list, prior_analysis: Optional[str] = None, 
                        stock_symbol: Optional[str] = None) -> str:
    """
    Generate the complete analysis prompt
    
    Args:
        window_types: List of chart window types
        prior_analysis: Optional previous analysis for comparison
        stock_symbol: Optional stock symbol
    
    Returns:
        Complete formatted prompt string
    """
    symbol_text = f" for {stock_symbol}" if stock_symbol else ""
    email_threshold = int(os.getenv('EMAIL_ALERT_THRESHOLD', '60'))
    
    chart_context = get_chart_context(window_types)
    
    base_prompt = BASE_ANALYSIS_PROMPT.format(
        num_charts=len(window_types),
        symbol_text=symbol_text,
        chart_context=chart_context
    )
    
    if prior_analysis:
        trend_prompt = TREND_EVAL_WITH_PRIOR.format(
            prior_analysis=prior_analysis[:500],
            email_threshold=email_threshold
        )
    else:
        trend_prompt = TREND_EVAL_INITIAL
    
    return base_prompt + trend_prompt


def get_consolidation_prompt(symbol: str, all_analyses: str) -> str:
    """
    Generate the consolidation prompt for Google AI
    
    Args:
        symbol: Stock symbol
        all_analyses: Combined analyses from all providers
    
    Returns:
        Formatted consolidation prompt
    """
    return CONSOLIDATION_PROMPT.format(
        symbol=symbol,
        all_analyses=all_analyses
    )


# ============================================================================
# CUSTOM PROMPT LOADING (Optional)
# ============================================================================
# You can override prompts by creating a prompts_custom.py file
# or setting environment variables

def load_custom_prompts():
    """
    Load custom prompts from prompts_custom.py if it exists
    This allows users to override default prompts without modifying this file
    """
    try:
        from prompts_custom import (
            CHART_CONTEXTS as CUSTOM_CHART_CONTEXTS,
            BASE_ANALYSIS_PROMPT as CUSTOM_BASE_PROMPT,
            CONSOLIDATION_PROMPT as CUSTOM_CONSOLIDATION_PROMPT
        )
        
        global CHART_CONTEXTS, BASE_ANALYSIS_PROMPT, CONSOLIDATION_PROMPT
        
        if CUSTOM_CHART_CONTEXTS:
            CHART_CONTEXTS.update(CUSTOM_CHART_CONTEXTS)
        if CUSTOM_BASE_PROMPT:
            BASE_ANALYSIS_PROMPT = CUSTOM_BASE_PROMPT
        if CUSTOM_CONSOLIDATION_PROMPT:
            CONSOLIDATION_PROMPT = CUSTOM_CONSOLIDATION_PROMPT
            
        print("[CONFIG] Loaded custom prompts from prompts_custom.py")
    except ImportError:
        pass  # No custom prompts file, use defaults


# Load custom prompts on module import
load_custom_prompts()
