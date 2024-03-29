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
        
    def update_favorites(self, student_id: str, parking_name: str, capacity: int) -> None:
        self.cursor.execute(
            "UPDATE favorites SET capacity = %s WHERE fprofileID = %s AND parkingName= %s", (capacity, student_id, parking_name))
        self.connection.commit()

    def insert_new_class(self, student_id: str, course_name: str, building_name: str) -> None:
        self.cursor.execute(
            "INSERT INTO classes (cProfileID, courseName, buildingName) VALUES (%s, %s, %s)", (student_id, course_name, building_name))
        self.connection.commit()

    def get_all_parking_decks(self):
        self.cursor.execute("SELECT * FROM parkingLocations")
        return self.cursor.fetchall()
    
    def get_specific_parking_deck(self, parking_name: str):
        self.cursor.execute("SELECT capacity FROM parkingLocations WHERE shortName = %s", (parking_name,))
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
            "DELETE FROM favorites WHERE fprofileID = %s  AND parklocation", (student_id, location))
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
    
    def delete_favorite(self, student_id: str, parking_name: str, capacity: int) -> None:
        print(student_id)
        self.cursor.execute(
            "DELETE FROM favorites WHERE parkingName = %s AND capacity = %s AND fprofileID = %s", (parking_name, capacity, student_id))
        self.connection.commit()

    def get_all_capacities(self, column):
        self.cursor.execute("SELECT location, "+ column +" FROM capacity")
        return self.cursor.fetchall()
    
    def change_capacities(self, capacities) -> None:
        for cap in capacities:
            self.cursor.execute("UPDATE parkingLocations SET capacity = %s WHERE shortName = %s", (cap[1], cap[0]))
        self.connection.commit()
        
    def get_capcities(self):
        self.cursor.execute("SELECT * FROM parkingLocations")
        return self.cursor.fetchall()
    
    def insert_feedback(self, email, feedback, time):
        self.cursor.execute("INSERT INTO feedback (email, feedback, time) VALUES (%s, %s, %s)", (email, feedback, time))
        self.connection.commit()