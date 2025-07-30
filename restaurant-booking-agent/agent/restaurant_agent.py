import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import sys
sys.path.append('..')

from tools.restaurant_search import RestaurantSearchTool
from tools.availability_checker import AvailabilityCheckerTool
from tools.booking_manager import BookingManagerTool
from tools.email_sender import EmailSenderTool
from tools.user_preference import UserPreferenceTool

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class RestaurantBookingAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.tools = {
            'restaurant_search': RestaurantSearchTool(),
            'availability_checker': AvailabilityCheckerTool(),
            'booking_manager': BookingManagerTool(),
            'email_sender': EmailSenderTool(),
            'user_preference': UserPreferenceTool()
        }
        self.conversation_state = {
            'step': 'initial',
            'preferences': {},
            'search_results': [],
            'selected_restaurant': None,
            'booking_details': {},
            'user_info': {}
        }
    
    def process_booking_request(self, user_input):
        """Main agentic processing with GOAL→THINK→PLAN→ACT→REFLECT pattern"""
        
        tool_results = self._execute_required_tools(user_input)
        
        prompt = f"""
                You are a professional restaurant booking assistant. Use the agentic pattern:

                GOAL: Help user complete restaurant reservation
                THINK: Analyze user input and current conversation state  
                PLAN: Determine next steps in booking process
                ACT: Use tool results and provide helpful response
                REFLECT: Check if we're making progress toward booking

                Current State: {self.conversation_state['step']}
                User Preferences: {json.dumps(self.conversation_state['preferences'], indent=2)}
                User Input: {user_input}
                Tool Results: {json.dumps(tool_results, indent=2)}

                Guidelines:
                - Always follow GOAL→THINK→PLAN→ACT→REFLECT format
                - Be conversational and helpful
                - Ask for missing information when needed
                - Provide clear options and recommendations
                - Confirm important details before proceeding

                Respond in the agentic format and guide user to next step.
        """
        
        try:
            response = self.model.generate_content(prompt)
            self._update_conversation_state(tool_results, user_input)
            return response.text
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _execute_required_tools(self, user_input):
        """Execute tools based on current conversation state"""
        tool_results = {}
        current_step = self.conversation_state['step']
        
        try:
            if current_step == 'initial':
                # Extract preferences
                tool_results['preferences'] = self.tools['user_preference'].extract_preferences(user_input)
                validation = self.tools['user_preference'].validate_preferences(tool_results['preferences'])
                tool_results['validation'] = validation
                
                # Search if we have enough info
                if validation['valid'] and tool_results['preferences'].get('cuisine'):
                    search_params = {
                        'cuisine': tool_results['preferences']['cuisine'],
                        'location': tool_results['preferences'].get('location', 'downtown'),
                        'party_size': tool_results['preferences']['party_size'],
                        'price_range': tool_results['preferences'].get('budget', 2)
                    }
                    tool_results['restaurant_search'] = self.tools['restaurant_search'].search_restaurants(search_params)
            
            elif current_step == 'search_results':
                # User selecting restaurant
                selected_index = self._extract_restaurant_selection(user_input)
                if selected_index < len(self.conversation_state['search_results']):
                    selected_restaurant = self.conversation_state['search_results'][selected_index]
                    self.conversation_state['selected_restaurant'] = selected_restaurant
                    
                    booking_details = {
                        'date': self.conversation_state['preferences']['date'],
                        'time': self.conversation_state['preferences']['time'],
                        'party_size': self.conversation_state['preferences']['party_size']
                    }
                    
                    tool_results['availability'] = self.tools['availability_checker'].check_availability(
                        selected_restaurant, booking_details
                    )
            
            elif current_step == 'collect_user_info':
                # Extract user contact info
                user_info = self._extract_user_info(user_input)
                tool_results['user_info'] = user_info
                
                if user_info.get('name') and user_info.get('email') and user_info.get('phone'):
                    booking_result = self.tools['booking_manager'].make_booking(
                        self.conversation_state['selected_restaurant'],
                        self.conversation_state['booking_details'],
                        user_info
                    )
                    tool_results['booking'] = booking_result
                    
                    if booking_result['success']:
                        email_result = self.tools['email_sender'].send_confirmation_email(
                            booking_result['confirmation_details'],
                            user_info['email']
                        )
                        tool_results['email'] = email_result
        
        except Exception as e:
            tool_results['error'] = f"Tool execution error: {str(e)}"
        
        return tool_results
    
    def _extract_restaurant_selection(self, user_input):
        """Extract which restaurant user selected"""
        user_lower = user_input.lower()
        
        if '1' in user_input or 'first' in user_lower:
            return 0
        elif '2' in user_input or 'second' in user_lower:
            return 1
        elif '3' in user_input or 'third' in user_lower:
            return 2
        
        return 0  # Default to first
    
    def _extract_user_info(self, user_input):
        """Extract user contact information"""
        import re
        user_info = {}
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', user_input)
        if email_match:
            user_info['email'] = email_match.group()
        
        # Extract phone
        phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', user_input)
        if phone_match:
            user_info['phone'] = phone_match.group()
        
        # Extract name
        name_match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', user_input)
        if name_match:
            user_info['name'] = name_match.group()
        
        return user_info
    
    def _update_conversation_state(self, tool_results, user_input):
        """Update conversation state based on tool results"""
        if 'preferences' in tool_results:
            self.conversation_state['preferences'].update(tool_results['preferences'])
        
        if 'restaurant_search' in tool_results and tool_results['restaurant_search']['status'] == 'success':
            self.conversation_state['search_results'] = tool_results['restaurant_search']['restaurants']
            self.conversation_state['step'] = 'search_results'
        
        if 'availability' in tool_results:
            if tool_results['availability']['available']:
                self.conversation_state['booking_details'] = {
                    'date': tool_results['availability']['date'],
                    'time': tool_results['availability']['time'],
                    'party_size': tool_results['availability']['party_size']
                }
                self.conversation_state['step'] = 'collect_user_info'
        
        if 'user_info' in tool_results:
            self.conversation_state['user_info'].update(tool_results['user_info'])
        
        if 'booking' in tool_results and tool_results['booking']['success']:
            self.conversation_state['step'] = 'confirmed'
    
    def reset_conversation(self):
        """Reset conversation for new booking"""
        self.conversation_state = {
            'step': 'initial',
            'preferences': {},
            'search_results': [],
            'selected_restaurant': None,
            'booking_details': {},
            'user_info': {}
        }
