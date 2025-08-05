import re
from datetime import datetime, timedelta

class UserPreferenceTool:
    def __init__(self):
        self.name = "user_preference"
        self.description = "Manage user dining preferences and history"
    
    def extract_preferences(self, user_message):
        """Extract dining preferences from user message"""
        preferences = {
            'cuisine': None,
            'location': None,
            'party_size': None,
            'budget': None,
            'date': None,
            'time': None,
            'special_requirements': []
        }
        
        message_lower = user_message.lower()
        
        # Extract cuisine types
        cuisine_keywords = {
            'italian': ['italian', 'pasta', 'pizza', 'trattoria'],
            'chinese': ['chinese', 'dim sum', 'kung pao'],
            'mexican': ['mexican', 'tacos', 'burrito'],
            'indian': ['indian', 'curry', 'tandoor', 'biryani'],
            'japanese': ['japanese', 'sushi', 'ramen'],
            'french': ['french', 'bistro', 'wine']
        }
        
        for cuisine, keywords in cuisine_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                preferences['cuisine'] = cuisine
                break
        
        # Extract party size
        party_patterns = [
            r'(\d+)\s*(?:people|person|pax)',
            r'party\s*of\s*(\d+)',
            r'table\s*for\s*(\d+)'
        ]
        
        for pattern in party_patterns:
            match = re.search(pattern, message_lower)
            if match:
                preferences['party_size'] = int(match.group(1))
                break
        
        # Extract location
        if 'downtown' in message_lower:
            preferences['location'] = 'downtown'
        elif 'uptown' in message_lower:
            preferences['location'] = 'uptown'
        
        # Extract date
        if 'today' in message_lower:
            preferences['date'] = datetime.now().strftime('%Y-%m-%d')
        elif 'tomorrow' in message_lower:
            preferences['date'] = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Extract time
        time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*([ap]m)', message_lower)
        if time_match:
            hour = int(time_match.group(1))
            minute = time_match.group(2) if time_match.group(2) else '00'
            ampm = time_match.group(3)
            
            if ampm == 'pm' and hour != 12:
                hour += 12
            elif ampm == 'am' and hour == 12:
                hour = 0
            
            preferences['time'] = f"{hour:02d}:{minute}"
        
        # Extract special requirements
        special_keywords = ['vegetarian', 'vegan', 'birthday', 'anniversary']
        for keyword in special_keywords:
            if keyword in message_lower:
                preferences['special_requirements'].append(keyword)
        
        return preferences
    
    def validate_preferences(self, preferences):
        """Validate and suggest missing required preferences"""
        missing = []
        suggestions = []
        
        if not preferences.get('party_size'):
            missing.append('party_size')
            suggestions.append("How many people will be dining?")
        
        if not preferences.get('date'):
            missing.append('date')
            suggestions.append("What date would you like? (today, tomorrow, or specific date)")
        
        if not preferences.get('time'):
            missing.append('time')
            suggestions.append("What time would you prefer? (e.g., 7 PM)")
        
        return {
            'valid': len(missing) == 0,
            'missing': missing,
            'suggestions': suggestions
        }