from database.db import Database

class Favorites:
    def __init__(self):
        self.db = Database()

    def get_all_favorites_by_user(self, user_id):
        """ Retrieve all favorites for a given user """
        return self.db.get_all_favorites_by_user(user_id)

    def add_favorite(self, student_id, parking_name):
        """ Add a new favorite for a user """
        self.db.insert_new_favorite(student_id, parking_name)

    #def remove_favorite(self, user_id, favorite_id):
        #""" Remove a favorite for a user """
        # implement a method in the Database class for this
        # self.db.delete_favorite(user_id, favorite_id)

    #def update_favorite(self, user_id, favorite_id, new_parking_name):
        #""" Update an existing favorite for a user """
        # implement a method in the Database class for this
        # self.db.update_favorite(user_id, favorite_id, new_parking_name)
