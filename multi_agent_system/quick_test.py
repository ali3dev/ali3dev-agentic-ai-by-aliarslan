"""
Quick test to verify the system generates actual content
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_system import MultiAgentSystem

def quick_test():
    """Quick test of the system"""
    print("Quick Test - Content Generation")
    print("="*50)
    
    # Initialize system
    system = MultiAgentSystem()
    system.start_session("quick_test")
    
    # Test the specific request
    request = "create a post for my linkedin account (How to optimized profile throuh SEO)"
    
    print(f"Testing: {request}")
    print("-" * 50)
    
    try:
        response = system.process_request(request)
        
        print("Response Generated!")
        print("="*50)
        print(response)
        print("="*50)
        
        # Check for fallback content
        if "Lorem ipsum" in response:
            print("FAILED: Still contains fallback content")
        elif "test fallback" in response.lower():
            print("FAILED: Still contains fallback content")
        else:
            print("SUCCESS: Generated actual content!")
            
        # Check for relevant content
        if "linkedin" in response.lower() or "profile" in response.lower() or "seo" in response.lower():
            print("SUCCESS: Contains relevant content!")
        else:
            print("WARNING: May not contain relevant content")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    quick_test() 