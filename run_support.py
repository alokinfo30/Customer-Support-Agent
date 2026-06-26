#!/usr/bin/env python
"""
Run Customer Support Agent
Run: python run_support.py
"""

import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run the customer support agent"""
    print("=" * 70)
    print("🤖 MULTI-AGENT CUSTOMER SUPPORT")
    print("=" * 70)
    print("Six Key Elements:")
    print("  1. 🔄 Role Playing - Each agent has a distinct role")
    print("  2. 🎯 Focus - Clear goals and backstories")
    print("  3. 🛠️ Tools - Agents use search and scrape tools")
    print("  4. 🤝 Cooperation - Agents work together")
    print("  5. 🛡️ Guardrails - Clear boundaries and expectations")
    print("  6. 🧠 Memory - Agents remember past interactions")
    print("=" * 70)
    
    try:
        from app.crew import SupportCrew
        crew = SupportCrew()
        
        # Test with a sample inquiry
        print("\n📝 Processing sample inquiry...")
        result = crew.process_inquiry(
            customer="DeepLearningAI",
            person="Andrew Ng",
            inquiry="I need help with setting up a Crew and kicking it off, specifically how can I add memory to my crew? Can you provide guidance?"
        )
        
        if result['status'] == 'success':
            print("\n✅ Support processed successfully!")
            print(f"Response:\n{result['response'][:500]}...")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()