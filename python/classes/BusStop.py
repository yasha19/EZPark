"""
this is the class for representing bus stops
"""

class BusStop():
    def __init__(self, name, routes):
        self.name = name
        self.routes = routes

    def get_name(self):
        return self.name
    
    def get_routes(self):
        return self.routes