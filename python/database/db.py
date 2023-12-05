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

    def insert_new_favorite(self, student_id: str, parking_name: str, capacity: int) -> None:
        self.cursor.execute(
            "INSERT INTO favorites (fprofileID, parkingName, capacity) VALUES (%s, %s, %s)", (student_id, parking_name, capacity))
        self.connection.commit()

    def insert_new_class(self, student_id: str, course_name: str, building_name: str) -> None:
        self.cursor.execute(
            "INSERT INTO classes (cProfileID, courseName, buildingName) VALUES (%s, %s, %s)", (student_id, course_name, building_name))
        self.connection.commit()

    def get_all_parking_decks(self):
        self.cursor.execute("SELECT * FROM parkingLocations")
        return self.cursor.fetchall()
    
    def get_all_bus_locations(self):
        self.cursor.execute("SELECT * FROM busLocations")
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
    
    def get_all_classes_by_user(self, user_id: str):
        self.cursor.execute("SELECT * FROM classes WHERE cProfileID= %s", (user_id,))
        return self.cursor.fetchall()
    
    def remove_favorite(self, student_id: str, location):
        print(location)
        self.cursor.execute(
            "DELETE FROM favprites WHERE fprofileID = %s  AND parklocation", (student_id, location))
        self.connection.commit()
        return self.cursor.fetchall()

    def get_all_favorites_by_user(self, user_id: str):
        self.cursor.execute(
            "SELECT * FROM favorites WHERE fprofileID = %s", (user_id,))
        return self.cursor.fetchall()

    def get_alerts_by_date(self, daytime: dt.date):
        self.cursor.execute(
            "SELECT * FROM alerts WHERE date > %s", daytime)
        return self.cursor.fetchall()
    
    def get_all_buildings(self):
        self.cursor.execute("SELECT * FROM buildingNames")
        return self.cursor.fetchall()
    
    def delete_class(self, student_id: str, course_name: str, building_name: str) -> None:
        print(student_id)
        self.cursor.execute(
            "DELETE FROM classes WHERE courseName = %s AND buildingName = %s AND cProfileID = %s", (course_name, building_name, student_id))
        self.connection.commit()
        return self.cursor.fetchall()
    
    def delete_favorite(self, student_id: str, parking_name: str, capacity: int) -> None:
        print(student_id)
        self.cursor.execute(
            "DELETE FROM favorites WHERE parkingName = %s AND capacity = %s AND fprofileID = %s", (parking_name, capacity, student_id))
        self.connection.commit()
        return self.cursor.fetchall()
    
    def insert_feedback(self, user_id, feedback):
        self.cursor.execute(
            "INSERT INTO feedbacks (user_id, feedback_text) VALUES (%s, %s)", (user_id, feedback))
        self.connection.commit()
