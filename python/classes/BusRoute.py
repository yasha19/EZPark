"""
this is the class for representing bus routes
"""

class BusRoute():
    def __init__(self, route_id, stops):
        self.route_id = route_id
        self.stops = stops

    def get_route_id(self):
        return self.route_id
    
    def get_stops(self):
        return self.stops