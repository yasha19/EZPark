import mysql.connector
import datetime as dt

class Database:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host='sql9.freesqldatabase.com',
            user='sql9656653',
            password='TiLR6twahS',
            database='sql9656653'
        )
        self.cursor = self.connection.cursor()

    def insert_new_favorite(self, student_id: int, parking_name:str) -> None:
        self.cursor.execute(
            "INSERT INTO favorites (favoritesID, fprofileID, parkingName) VALUES (?, ?, ?)", (None, student_id, parking_name))
        self.connection.commit()

    def insert_new_class(self, student_id: int, building_name: str) -> None:
        self.cursor.execute(
            "INSERT INTO classes (classesID, cProfileID, buildingName) VALUES (?, ?, ?)", (None, student_id, building_name))
        self.connection.commit()

    def get_all_parking_decks(self):
        self.cursor.execute("SELECT * FROM parking")
        return self.cursor.fetchall()
    
    def get_profile_by_id(self, user_id: str):
        self.cursor.execute("SELECT * FROM profile where email = ?", (user_id))
        return self.cursor.fetchall()
    
    def update_profile(self, profile):
        self.cursor.execute("UPDATE profile SET rec = ? AND comType = ? WHERE userID = ?", (profile.rec, profile.comType, profile.userId))

    def get_all_classes_by_user(self, user_id: int):
        self.cursor.execute("SELECT * FROM classes WHERE cProfileID= ?", (user_id))
        return self.cursor.fetchall()

    def get_all_favorites_by_user(self, user_id: int):
        self.cursor.execute(
            "SELECT * FROM favorites WHERE fprofileID = ?", (user_id))
        return self.cursor.fetchall()

    def get_alerts_by_date(self, daytime: dt.date):
        self.cursor.execute(
            "SELECT * FROM alerts WHERE date > ?", daytime)
        return self.cursor.fetchall()
    
    def get_all_buildings(self):
        self.cursor.execute("SELECT * FROM buildingNames")
        return self.cursor.fetchall()