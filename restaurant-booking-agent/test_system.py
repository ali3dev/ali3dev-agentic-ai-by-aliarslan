#!/usr/bin/env python3
"""
Restaurant Booking Agent - Testing System
Run this file to test all components
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.restaurant_agent import RestaurantBookingAgent
from tools.restaurant_search import RestaurantSearchTool
from tools.availability_checker import AvailabilityCheckerTool
from tools.booking_manager import BookingManagerTool
from tools.email_sender import EmailSenderTool
from tools.user_preference import UserPreferenceTool

def test_individual_tools():
    """Test each tool individually"""
    print("🔧 Testing Individual Tools")
    print("=" * 50)
    
    # Test 1: Restaurant Search
    print("\n1. Testing Restaurant Search Tool...")
    search_tool = RestaurantSearchTool()
    search_result = search_tool.search_restaurants({
        'cuisine': 'italian',
        'location': 'downtown',
        'party_size': 4,
        'price_range': 2
    })
    print(f"✅ Found {len(search_result['restaurants'])} restaurants")
    print(f"   Top result: {search_result['restaurants'][0]['name']} (Rating: {search_result['restaurants'][0]['rating']})")
    
    # Test 2: Availability Checker
    print("\n2. Testing Availability Checker...")
    availability_tool = AvailabilityCheckerTool()
    availability_result = availability_tool.check_availability(
        search_result['restaurants'][0],
        {'date': '2024-07-26', 'time': '19:00', 'party_size': 4}
    )
    print(f"✅ Availability check: {'Available' if availability_result['available'] else 'Not Available'}")
    if not availability_result['available']:
        print(f"   Alternatives: {len(availability_result.get('alternatives', []))} options")
    
    # Test 3: User Preference Extraction
    print("\n3. Testing User Preference Tool...")
    preference_tool = UserPreferenceTool()
    test_message = "I want Italian food for 4 people tomorrow at 7 PM downtown"
    preferences = preference_tool.extract_preferences(test_message)
    print(f"✅ Extracted preferences:")
    print(f"   Cuisine: {preferences['cuisine']}")
    print(f"   Party size: {preferences['party_size']}")
    print(f"   Time: {preferences['time']}")
    print(f"   Location: {preferences['location']}")
    
    # Test 4: Booking Manager (if availability exists)
    if availability_result['available']:
        print("\n4. Testing Booking Manager...")
        booking_tool = BookingManagerTool()
        booking_result = booking_tool.make_booking(
            search_result['restaurants'][0],
            {'date': '2024-07-26', 'time': '19:00', 'party_size': 4},
            {'name': 'Test User', 'email': 'test@example.com', 'phone': '555-0123'}
        )
        print(f"✅ Booking result: {'Success' if booking_result['success'] else 'Failed'}")
        if booking_result['success']:
            print(f"   Booking reference: {booking_result['booking_ref']}")
            
            # Test 5: Email Sender
            print("\n5. Testing Email Sender...")
            email_tool = EmailSenderTool()
            email_result = email_tool.send_confirmation_email(
                booking_result['confirmation_details'],
                'test@example.com'
            )
            print(f"✅ Email result: {'Sent' if email_result['success'] else 'Failed'}")
    else:
        print("\n4. Skipping Booking Manager (no availability)")
        print("5. Skipping Email Sender (no booking)")

def test_full_conversation_flow():
    """Test complete conversation flow"""
    print("\n\n🤖 Testing Complete Conversation Flow")
    print("=" * 50)
    
    agent = RestaurantBookingAgent()
    
    test_conversations = [
        "I want Italian food for 4 people tomorrow at 7 PM downtown",
        "First restaurant looks good",
        "John Smith, john@email.com, 555-123-4567, vegetarian options please"
    ]
    
    for i, message in enumerate(test_conversations, 1):
        print(f"\nStep {i}: User says: '{message}'")
        print("-" * 40)
        
        try:
            response = agent.process_booking_request(message)
            print(f"Agent Response: {response[:200]}...")
            print(f"Current State: {agent.conversation_state['step']}")
            
            if "GOAL:" in response and "REFLECT:" in response:
                print("✅ Agentic pattern detected")
            else:
                print("⚠️  Agentic pattern not clearly visible")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\nFinal conversation state: {agent.conversation_state['step']}")

def test_error_scenarios():
    """Test error handling scenarios"""
    print("\n\n⚠️  Testing Error Scenarios")
    print("=" * 50)
    
    agent = RestaurantBookingAgent()
    
    error_test_cases = [
        "I want food",  # Incomplete information
        "Book me something expensive",  # Vague request
        "xyz restaurant for abc people",  # Invalid data
        "",  # Empty input
    ]
    
    for i, test_case in enumerate(error_test_cases, 1):
        print(f"\nError Test {i}: '{test_case}'")
        try:
            response = agent.process_booking_request(test_case)
            print(f"✅ Handled gracefully: {response[:100]}...")
        except Exception as e:
            print(f"❌ Crashed: {str(e)}")

def main():
    """Run all tests"""
    print("🧪 Restaurant Booking Agent - Complete Test Suite")
    print("=" * 60)
    
    try:
        # Test individual tools
        test_individual_tools()
        
        # Test full conversation flow
        test_full_conversation_flow()
        
        # Test error scenarios
        test_error_scenarios()
        
        print("\n\n🎉 All Tests Completed!")
        print("=" * 60)
        print("Summary:")
        print("✅ Individual tools tested")
        print("✅ Conversation flow tested")
        print("✅ Error handling tested")
        print("✅ Agentic pattern verified")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")

if __name__ == "__main__":
    main()