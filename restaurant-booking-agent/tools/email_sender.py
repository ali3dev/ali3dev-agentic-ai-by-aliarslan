import random
from datetime import datetime

class EmailSenderTool:
    def __init__(self):
        self.name = "email_sender"
        self.description = "Send booking confirmation emails"
        self.sent_emails = []
    
    def send_confirmation_email(self, booking_details, user_email):
        """Send professional booking confirmation email (simulated)"""
        try:
            email_content = self._create_email_content(booking_details)
            email_success = random.random() < 0.98  # 98% success rate
            
            if email_success:
                email_record = {
                    'to': user_email,
                    'subject': f"Booking Confirmed - {booking_details['restaurant_name']}",
                    'content': email_content,
                    'sent_at': datetime.now().isoformat(),
                    'status': 'delivered'
                }
                
                self.sent_emails.append(email_record)
                
                return {
                    'success': True,
                    'message': 'Confirmation email sent successfully',
                    'email_id': f"EMAIL{len(self.sent_emails):04d}"
                }
            else:
                return {
                    'success': False,
                    'error': 'Email delivery temporarily unavailable. Booking is still confirmed.'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': f"Email sending failed: {str(e)}"
            }
    
    def _create_email_content(self, booking):
        """Create professional email content"""
        return f"""
🍽️ BOOKING CONFIRMED!

Dear {booking['user_name']},

Your restaurant reservation has been confirmed:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 RESTAURANT: {booking['restaurant_name']}
📅 DATE: {booking['date']}
🕐 TIME: {booking['time']}
👥 PARTY SIZE: {booking['party_size']} people
🔖 BOOKING REF: {booking['booking_ref']}
📍 ADDRESS: {booking['restaurant_address']}
📞 PHONE: {booking['restaurant_phone']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANT INFORMATION:
- Please arrive 10-15 minutes early
- Bring your booking reference: {booking['booking_ref']}
- Table will be held for 15 minutes past reservation time
- Contact restaurant directly for any changes

{f"SPECIAL REQUESTS: {booking['special_requests']}" if booking.get('special_requests') else ""}

Thank you for using our booking service!
Have a wonderful dining experience! 🎉
        """.strip()