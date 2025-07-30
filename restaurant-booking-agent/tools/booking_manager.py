import random
import uuid
from datetime import datetime

class BookingManagerTool:
    def __init__(self):
        self.name = "booking_manager"
        self.description = "Handle restaurant reservation bookings"
        self.bookings_db = {}
    
    def make_booking(self, restaurant_info, booking_details, user_info):
        """Make actual restaurant reservation (simulated)"""
        try:
            booking_ref = f"BK{uuid.uuid4().hex[:8].upper()}"
            booking_success = random.random() < 0.95  # 95% success rate
            
            if booking_success:
                booking_record = {
                    'booking_ref': booking_ref,
                    'restaurant_id': restaurant_info['id'],
                    'restaurant_name': restaurant_info['name'],
                    'restaurant_address': restaurant_info['address'],
                    'restaurant_phone': restaurant_info['phone'],
                    'user_name': user_info['name'],
                    'user_email': user_info['email'],
                    'user_phone': user_info['phone'],
                    'date': booking_details['date'],
                    'time': booking_details['time'],
                    'party_size': booking_details['party_size'],
                    'special_requests': user_info.get('special_requests', ''),
                    'status': 'confirmed',
                    'created_at': datetime.now().isoformat(),
                    'table_type': self._assign_table_type(booking_details['party_size'])
                }
                
                self.bookings_db[booking_ref] = booking_record
                
                return {
                    'success': True,
                    'booking_ref': booking_ref,
                    'confirmation_details': booking_record,
                    'restaurant_confirmation': f"REST{random.randint(1000, 9999)}"
                }
            else:
                return {
                    'success': False,
                    'error': 'Restaurant booking system temporarily unavailable.'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': f"Booking failed: {str(e)}"
            }
    
    def _assign_table_type(self, party_size):
        """Assign appropriate table type"""
        if party_size <= 2:
            return "Intimate table by the window"
        elif party_size <= 4:
            return "Standard dining table"
        elif party_size <= 6:
            return "Large family table"
        else:
            return "Private dining room"
    
    def get_booking(self, booking_ref):
        """Retrieve booking details"""
        return self.bookings_db.get(booking_ref)