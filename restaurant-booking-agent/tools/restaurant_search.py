import random

class RestaurantSearchTool:
    def __init__(self):
        self.name = "restaurant_search"
        self.description = "Search restaurants by cuisine, location, price range"
        
        # Realistic restaurant database (simulated)
        self.restaurants_db = [
            {
                'id': 'rest_001',
                'name': "Mario's Trattoria",
                'cuisine': 'italian',
                'location': 'downtown',
                'price_range': 3,
                'rating': 4.8,
                'reviews': 324,
                'address': '123 Main St, Downtown',
                'phone': '(555) 123-4567',
                'specialties': ['pasta', 'pizza', 'wine'],
                'capacity': 80
            },
            {
                'id': 'rest_002', 
                'name': "Bella Vista",
                'cuisine': 'italian',
                'location': 'downtown',
                'price_range': 2,
                'rating': 4.6,
                'reviews': 198,
                'address': '456 Oak Ave, Downtown',
                'phone': '(555) 234-5678',
                'specialties': ['seafood', 'risotto'],
                'capacity': 60
            },
            {
                'id': 'rest_003',
                'name': "Dragon Palace",
                'cuisine': 'chinese',
                'location': 'downtown',
                'price_range': 2,
                'rating': 4.5,
                'reviews': 267,
                'address': '789 Pine St, Downtown',
                'phone': '(555) 345-6789',
                'specialties': ['dim sum', 'peking duck'],
                'capacity': 100
            },
            {
                'id': 'rest_004',
                'name': "Giuseppe's Fine Dining",
                'cuisine': 'italian',
                'location': 'uptown',
                'price_range': 4,
                'rating': 4.9,
                'reviews': 156,
                'address': '321 Elite Blvd, Uptown',
                'phone': '(555) 456-7890',
                'specialties': ['truffle', 'aged steaks'],
                'capacity': 40
            },
            {
                'id': 'rest_005',
                'name': "Spice Garden",
                'cuisine': 'indian',
                'location': 'downtown',
                'price_range': 2,
                'rating': 4.4,
                'reviews': 203,
                'address': '654 Curry Lane, Downtown',
                'phone': '(555) 567-8901',
                'specialties': ['tandoor', 'biryani'],
                'capacity': 70
            },
            {
                'id': 'rest_006',
                'name': "Tokyo Sushi Bar",
                'cuisine': 'japanese',
                'location': 'downtown',
                'price_range': 3,
                'rating': 4.7,
                'reviews': 289,
                'address': '987 Sakura St, Downtown',
                'phone': '(555) 678-9012',
                'specialties': ['sushi', 'ramen'],
                'capacity': 50
            },
            {
                'id': 'rest_007',
                'name': "Casa Mexico",
                'cuisine': 'mexican',
                'location': 'downtown',
                'price_range': 2,
                'rating': 4.3,
                'reviews': 178,
                'address': '147 Taco Ave, Downtown',
                'phone': '(555) 789-0123',
                'specialties': ['tacos', 'margaritas'],
                'capacity': 90
            }
        ]
    
    def search_restaurants(self, query_params):
        """Search restaurants based on user preferences"""
        try:
            results = []
            
            for restaurant in self.restaurants_db:
                match_score = 0
                
                # Check cuisine match
                if query_params.get('cuisine'):
                    if restaurant['cuisine'].lower() == query_params['cuisine'].lower():
                        match_score += 3
                
                # Check location match  
                if query_params.get('location'):
                    if query_params['location'].lower() in restaurant['location'].lower():
                        match_score += 2
                
                # Check price range (±1 range acceptable)
                if query_params.get('price_range'):
                    price_diff = abs(restaurant['price_range'] - query_params['price_range'])
                    if price_diff == 0:
                        match_score += 2
                    elif price_diff == 1:
                        match_score += 1
                
                # Check capacity for party size
                if query_params.get('party_size'):
                    if restaurant['capacity'] >= query_params['party_size']:
                        match_score += 1
                
                if match_score > 0:
                    restaurant_copy = restaurant.copy()
                    restaurant_copy['match_score'] = match_score
                    results.append(restaurant_copy)
            
            # Sort by match score, then rating
            results.sort(key=lambda x: (x['match_score'], x['rating']), reverse=True)
            
            return {
                'status': 'success',
                'restaurants': results[:6],  # Top 6 matches
                'total_found': len(results),
                'search_params': query_params
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Search failed: {str(e)}"
            }