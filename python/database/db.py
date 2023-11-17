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

    def insert_new_favorite(self, student_id: str, parking_name:str) -> None:
        self.cursor.execute(
            "INSERT INTO favorites (favoritesID, fprofileID, parkingName) VALUES (%s, %s, %s)", (None, student_id, parking_name))
        self.connection.commit()

    def insert_new_class(self, student_id: str, building_name: str) -> None:
        self.cursor.execute(
            "INSERT INTO classes (cProfileID, buildingName) VALUES (%s, %s)", (student_id, building_name))
        self.connection.commit()

    def get_all_parking_decks(self):
        self.cursor.execute("SELECT * FROM parking")
        return self.cursor.fetchall()
    
    def get_profile_by_id(self, user_id: str):
        # user_id_tuple = tuple(user_id,)
        self.cursor.execute("SELECT * FROM profile where gid = %s", (user_id,))
        return self.cursor.fetchone()
    
    def insert_new_profile(self, user_id: str, FName: str, LName: str, email: str ):
        self.cursor.execute("INSERT INTO profile (gid, FName, LName, email) VALUES (%s, %s, %s, %s)", (user_id, FName, LName, email))
        self.connection.commit()
        return self.cursor.fetchall()
    
    def update_profile(self, profile):
        self.cursor.execute("UPDATE profile SET rec = %s, comType = %s WHERE userID = %s", (profile.rec, profile.comType, profile.userId))
        return self.cursor.fetchall()

    def get_all_classes_by_user(self, user_id: int):
        self.cursor.execute("SELECT * FROM classes WHERE cProfileID= %s", (user_id))
        return self.cursor.fetchall()

    def get_all_favorites_by_user(self, user_id: int):
        self.cursor.execute(
            "SELECT * FROM favorites WHERE fprofileID = %s", (user_id))
        return self.cursor.fetchall()

    def get_alerts_by_date(self, daytime: dt.date):
        self.cursor.execute(
            "SELECT * FROM alerts WHERE date > %s", daytime)
        return self.cursor.fetchall()
    
    def get_all_buildings(self):
        self.cursor.execute("SELECT * FROM buildingNames")
        return self.cursor.fetchall()