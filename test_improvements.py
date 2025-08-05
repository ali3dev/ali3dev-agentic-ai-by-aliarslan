#!/usr/bin/env python3
"""
Test script to verify system improvements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_system import MultiAgentSystem

def test_system_improvements():
    """Test the improved system"""
    print("Testing System Improvements")
    print("="*50)
    
    # Initialize system
    system = MultiAgentSystem()
    system.start_session("test_user")
    
    # Test cases
    test_cases = [
        "create a post for my insta (How to optimized Upwork profile through SEO)",
        "Write a blog post about renewable energy",
        "Research AI trends and create a report"
    ]
    
    for i, test_request in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_request}")
        print("-" * 40)
        
        try:
            response = system.process_request(test_request)
            
            # Check if response is not just fallback
            if "Lorem ipsum" in response or "test fallback" in response.lower():
                print("FAILED: Response is fallback content")
                print(f"Response preview: {response[:200]}...")
            elif len(response) < 300:
                print("FAILED: Response too short")
                print(f"Response length: {len(response)} characters")
            elif "GOAL" not in response:
                print("FAILED: Missing GOAL keyword")
            else:
                print("PASSED: Good response generated")
                print(f"Response length: {len(response)} characters")
                print(f"Response preview: {response[:200]}...")
                
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    print("\n" + "="*50)
    print("Testing Complete")

if __name__ == "__main__":
    test_system_improvements() 