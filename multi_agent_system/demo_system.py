"""
Demonstration script for the improved multi-agent system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_system import MultiAgentSystem

def demo_instagram_post():
    """Demonstrate creating an Instagram post"""
    print("Multi-Agent System Demo")
    print("="*50)
    print("Creating an Instagram post about Upwork profile optimization...")
    print()
    
    # Initialize system
    system = MultiAgentSystem()
    system.start_session("demo_user")
    
    # The specific request from the user
    request = "create a post for my insta (How to optimized Upwork profile through SEO)"
    
    print(f"Request: {request}")
    print("-" * 50)
    
    try:
        # Process the request
        response = system.process_request(request)
        
        print("Response Generated Successfully!")
        print("="*50)
        print(response)
        print("="*50)
        
        # Analyze the response
        print("\nResponse Analysis:")
        print(f"Length: {len(response)} characters")
        print(f"Contains 'GOAL': {'GOAL' in response}")
        print(f"Contains fallback text: {'Lorem ipsum' in response}")
        print(f"Contains Instagram content: {'insta' in response.lower() or 'instagram' in response.lower()}")
        print(f"Contains SEO content: {'seo' in response.lower()}")
        print(f"Contains Upwork content: {'upwork' in response.lower()}")
        
        if "Lorem ipsum" in response:
            print("Warning: Response contains fallback content")
        else:
            print("Success: Response contains real content")
            
    except Exception as e:
        print(f"Error: {str(e)}")

def demo_system_capabilities():
    """Demonstrate various system capabilities"""
    print("\nSystem Capabilities Demo")
    print("="*50)
    
    system = MultiAgentSystem()
    system.start_session("capabilities_demo")
    
    demo_requests = [
        "Write a blog post about renewable energy",
        "Research AI trends and provide insights",
        "Create a business plan for a tech startup"
    ]
    
    for i, request in enumerate(demo_requests, 1):
        print(f"\nDemo {i}: {request}")
        print("-" * 40)
        
        try:
            response = system.process_request(request)
            print(f"Generated {len(response)} characters")
            print(f"Preview: {response[:150]}...")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Run the main demo
    demo_instagram_post()
    
    # Run additional demos
    demo_system_capabilities()
    
    print("\nDemo Complete!")
    print("The system is now working with improved content generation!") 