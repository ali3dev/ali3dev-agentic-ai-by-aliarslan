#!/usr/bin/env python3
"""
Restaurant Booking Agent - Interactive System
Run this file to start the interactive booking assistant
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.restaurant_agent import RestaurantBookingAgent

def main():
    """Interactive restaurant booking system"""
    agent = RestaurantBookingAgent()
    
    print("🍽️ Restaurant Booking Assistant")
    print("=" * 50)
    print("I can help you find and book restaurants!")
    print("Just tell me what you're looking for...")
    print("\nExample: 'I want Italian food for 4 people tomorrow at 7 PM downtown'")
    print("Type 'quit' to exit, 'reset' to start over\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("\n👋 Thank you for using Restaurant Booking Assistant!")
            break
        
        elif user_input.lower() == 'reset':
            agent.reset_conversation()
            print("\n🔄 Conversation reset. Tell me about your new booking request!")
            continue
        
        elif not user_input:
            print("Please tell me what you're looking for!")
            continue
        
        print("\n🤖 Agent is thinking...")
        
        try:
            response = agent.process_booking_request(user_input)
            print(f"\nAgent: {response}")
            
            # Show current step for debugging
            print(f"\n[Debug - Current step: {agent.conversation_state['step']}]")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'reset' to start over.")

if __name__ == "__main__":
    main()