class Favorite:
    def __init__(self, db):
        self.db = db

    def get_user_favorites(self, user_id):
        return self.db.get_all_favorites_by_user(user_id)
