import random
from datetime import datetime, timedelta

class AvailabilityCheckerTool:
    def __init__(self):
        self.name = "availability_checker"
        self.description = "Check real-time availability at restaurants"
    
    def check_availability(self, restaurant_info, booking_details):
        """Check if restaurant has availability (simulated)"""
        try:
            restaurant_id = restaurant_info['id']
            requested_time = booking_details['time']
            party_size = booking_details['party_size']
            date = booking_details['date']
            
            # Simulate realistic availability
            availability_chance = self._calculate_availability_chance(restaurant_info, booking_details)
            is_available = random.random() < availability_chance
            
            if is_available:
                return {
                    'available': True,
                    'restaurant': restaurant_info['name'],
                    'date': date,
                    'time': requested_time,
                    'party_size': party_size,
                    'table_type': self._suggest_table_type(party_size),
                    'estimated_duration': '2 hours'
                }
            else:
                alternatives = self._find_alternative_slots(restaurant_info, booking_details)
                return {
                    'available': False,
                    'restaurant': restaurant_info['name'],
                    'requested_time': requested_time,
                    'alternatives': alternatives,
                    'reason': 'Fully booked at requested time'
                }
        
        except Exception as e:
            return {
                'available': False,
                'error': f"Availability check failed: {str(e)}"
            }
    
    def _calculate_availability_chance(self, restaurant, booking):
        """Calculate realistic availability chance"""
        base_chance = 0.7
        
        # Popular restaurants have lower availability
        if restaurant['rating'] > 4.7:
            base_chance -= 0.2
        
        # Peak hours (7-8 PM) have lower availability
        hour = int(booking['time'].split(':')[0])
        if 19 <= hour <= 20:
            base_chance -= 0.3
        elif 18 <= hour <= 21:
            base_chance -= 0.1
        
        # Large parties have lower availability
        if booking['party_size'] > 6:
            base_chance -= 0.2
        elif booking['party_size'] > 4:
            base_chance -= 0.1
        
        return max(0.1, min(0.9, base_chance))
    
    def _suggest_table_type(self, party_size):
        """Suggest appropriate table type"""
        if party_size <= 2:
            return "Window table for two"
        elif party_size <= 4:
            return "Standard table for four"
        elif party_size <= 6:
            return "Large table for six"
        else:
            return "Private dining area"
    
    def _find_alternative_slots(self, restaurant, booking):
        """Find alternative available time slots"""
        alternatives = []
        requested_hour = int(booking['time'].split(':')[0])
        
        for offset in [-2, -1, 1, 2]:
            alt_hour = requested_hour + offset
            if 17 <= alt_hour <= 22:
                alt_time = f"{alt_hour}:00"
                alternatives.append({
                    'time': alt_time,
                    'availability': 'Available',
                    'note': f"Alternative to {booking['time']}"
                })
        
        return alternatives[:3]