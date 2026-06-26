#!/usr/bin/env python
"""
Test OpenRouter integration for Customer Support
Run: python test_openrouter.py
"""

import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_openrouter():
    """Test OpenRouter integration"""
    print("=" * 70)
    print("🤖 CUSTOMER SUPPORT - OPENROUTER TEST")
    print("=" * 70)
    
    print("\n📋 Environment Configuration:")
    print("-" * 70)
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key:
        print(f"✅ OpenRouter API Key: {api_key[:10]}...{api_key[-10:]}")
    else:
        print("❌ OpenRouter API Key NOT FOUND!")
        print("\n   Get your key from: https://openrouter.ai/keys")
        return False
    
    print(f"   Primary Model: {os.getenv('OPENROUTER_PRIMARY_MODEL', 'openai/gpt-4o-mini')}")
    print(f"   Fallback Models: {os.getenv('OPENROUTER_FALLBACK_MODELS', 'Default fallbacks')}")
    print(f"   Support Agent Model: {os.getenv('SUPPORT_AGENT_MODEL', 'Using primary')}")
    print(f"   QA Agent Model: {os.getenv('QA_AGENT_MODEL', 'Using primary')}")
    print(f"   Escalation Agent Model: {os.getenv('ESCALATION_AGENT_MODEL', 'Using primary')}")
    print(f"   Analytics Agent Model: {os.getenv('ANALYTICS_AGENT_MODEL', 'Using primary')}")
    
    print("\n🔄 Testing models...")
    print("-" * 70)
    
    try:
        from app.model_manager import model_manager
        
        results = model_manager.test_providers()
        
        print("\n📊 Model Status:")
        print("-" * 70)
        available_count = 0
        
        for model, available in results.items():
            status = "✅ AVAILABLE" if available else "❌ UNAVAILABLE"
            print(f"{model:45} : {status}")
            if available:
                available_count += 1
        
        print("-" * 70)
        print(f"\n📈 SUMMARY: {available_count}/{len(results)} models available")
        
        if available_count == 0:
            print("\n❌ No models available! Check:")
            print("   1. OpenRouter API key is valid")
            print("   2. You have internet connection")
            print("   3. Add credits if using paid models")
        else:
            print(f"\n✅ OpenRouter is working! Available models:")
            for model, available in results.items():
                if available:
                    print(f"   → {model}")
        
        # Test a sample inquiry
        print("\n🧪 Testing sample inquiry...")
        print("-" * 70)
        
        from app.crew import SupportCrew
        crew = SupportCrew()
        
        result = crew.process_inquiry(
            customer="TestCustomer",
            person="Test Person",
            inquiry="How do I install CrewAI?",
            use_tools=False  # Disable tools for quick test
        )
        
        if result['status'] == 'success':
            print("✅ Sample inquiry processed successfully!")
            print(f"Response preview: {result['response'][:200]}...")
        else:
            print(f"❌ Sample inquiry failed: {result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 70)
        return available_count > 0
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_openrouter()
    sys.exit(0 if success else 1)