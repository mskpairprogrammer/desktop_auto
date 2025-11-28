#!/usr/bin/env python3
"""
Test script to independently test each of the 3 AI analysis providers
"""
import os
import sys
from dotenv import load_dotenv
from ai_analysis import PerplexityAnalyzer, ClaudeAnalyzer, GoogleAIAnalyzer
from utils import encode_image_to_base64

# Load environment variables
load_dotenv()

def test_provider(provider_name, analyzer, screenshot_data):
    """Test a single provider with screenshots"""
    print(f"\n{'='*60}")
    print(f"Testing {provider_name.upper()}")
    print(f"{'='*60}")
    
    try:
        # Build content array with text and images
        content = [{"type": "text", "text": "Analyze these trading charts briefly."}]
        
        for window_type, image_path in screenshot_data.items():
            if image_path and os.path.exists(image_path):
                try:
                    image_uri = encode_image_to_base64(image_path)
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": image_uri}
                    })
                    print(f"  ✓ Encoded {window_type}: {image_path}")
                except Exception as e:
                    print(f"  ✗ Failed to encode {window_type}: {e}")
        
        print(f"\n  Sending request to {provider_name}...")
        result = analyzer.analyze_screenshots(content)
        
        if result:
            print(f"\n  ✓ {provider_name} responded successfully!")
            print(f"\n  Response preview (first 500 chars):")
            print(f"  {result[:500]}...")
            return True
        else:
            print(f"  ✗ {provider_name} returned empty response")
            return False
            
    except Exception as e:
        print(f"  ✗ Error testing {provider_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("Individual AI Provider Test Suite")
    print("=" * 60)
    
    # Get screenshot paths (use SNAP as example)
    symbol = "SNAP"
    screenshot_dir = "screenshots"
    symbol_dir = os.path.join(screenshot_dir, symbol)
    
    screenshot_data = {
        'trend_analysis': os.path.join(symbol_dir, f"{symbol}_luxoalgo.png"),
        'heiken_ashi': os.path.join(symbol_dir, f"{symbol}_heiken.png"),
        'volume_layout': os.path.join(symbol_dir, f"{symbol}_volume_layout.png"),
        'volumeprofile': os.path.join(symbol_dir, f"{symbol}_rvol.png"),
        'workspace': os.path.join(symbol_dir, f"{symbol}_symbolik.png"),
    }
    
    # Check if screenshots exist
    print(f"\nChecking for screenshot files in {symbol_dir}:")
    all_exist = True
    for window_type, path in screenshot_data.items():
        if os.path.exists(path):
            print(f"  ✓ {window_type}: {path}")
        else:
            print(f"  ✗ {window_type}: NOT FOUND - {path}")
            all_exist = False
    
    if not all_exist:
        print(f"\n⚠️  Some screenshots are missing. Using available screenshots only.")
        screenshot_data = {k: v for k, v in screenshot_data.items() if os.path.exists(v)}
    
    if not screenshot_data:
        print(f"\n✗ No screenshots found! Please run the main program first to capture screenshots.")
        return
    
    results = {}
    
    # Test Perplexity
    print(f"\n\n1. TESTING PERPLEXITY ANALYZER")
    try:
        perplexity_key = os.getenv('PERPLEXITY_API_KEY')
        if not perplexity_key:
            print("  ✗ PERPLEXITY_API_KEY not set in .env")
        else:
            perplexity = PerplexityAnalyzer(perplexity_key)
            results['perplexity'] = test_provider('Perplexity', perplexity, screenshot_data)
    except Exception as e:
        print(f"  ✗ Failed to initialize Perplexity: {e}")
        results['perplexity'] = False
    
    # Test Claude
    print(f"\n\n2. TESTING CLAUDE ANALYZER")
    try:
        claude_key = os.getenv('ANTHROPIC_API_KEY')
        if not claude_key:
            print("  ✗ ANTHROPIC_API_KEY not set in .env")
        else:
            claude = ClaudeAnalyzer(claude_key)
            results['claude'] = test_provider('Claude', claude, screenshot_data)
    except Exception as e:
        print(f"  ✗ Failed to initialize Claude: {e}")
        results['claude'] = False
    
    # Test Google AI
    print(f"\n\n3. TESTING GOOGLE AI ANALYZER")
    try:
        google_key = os.getenv('GOOGLE_AI_API_KEY')
        if not google_key:
            print("  ✗ GOOGLE_AI_API_KEY not set in .env")
        else:
            google = GoogleAIAnalyzer(google_key)
            results['google'] = test_provider('Google AI', google, screenshot_data)
    except Exception as e:
        print(f"  ✗ Failed to initialize Google AI: {e}")
        results['google'] = False
    
    # Summary
    print(f"\n\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    for provider, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {provider.upper()}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"\nTotal: {passed}/{total} providers working")

if __name__ == "__main__":
    main()
