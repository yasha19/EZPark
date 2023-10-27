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

    def insert_new_favorite(self, student_email: str) -> None:
        self.cursor.execute(
            "INSERT INTO favorites () VALUES (?, ?, ?)", ())
        self.connection.commit()

    def insert_new_class(self, student_email: str) -> None:
        self.cursor.execute(
            "INSERT INTO classes () VALUES (?, ?, ?)", ())
        self.connection.commit()

    def get_all_parking_decks(self):
        self.cursor.execute("SELECT * FROM parking")
        return self.cursor.fetchall()
    
    def get_preference_by_user(self, student_email: str):
        self.cursor.execute("SELECT * FROM preferences where student_email = ?", student_email)
        return self.cursor.fetchall()

    def get_all_classes_by_user(self, student_email: str):
        self.cursor.execute("SELECT * FROM classes WHERE id = ?", student_email)
        return self.cursor.fetchall()

    def get_all_favorites_by_user(self, student_email: str):
        self.cursor.execute(
            "SELECT * FROM favorites WHERE id = ?", student_email)
        return self.cursor.fetchall()

    def get_alerts_by_date(self, daytime: dt.date):
        self.cursor.execute(
            "SELECT * FROM alerts WHERE date > ?", daytime)
        return self.cursor.fetchall()