from datetime import datetime as dt
from python.database.db import Database

class UserSession:
    def __init__(self, username: str):
        self.username = username

class Sessions:
    def __init__(self):
        self.sessions = {}

    def add_new_session(self, username: str) -> None:
        if len(username) > 0:
            self.sessions[username] = UserSession(username)

    def get_session(self, username: str) -> UserSession:
        if len(username) > 0:
            return self.sessions[username]

    def remove_session(self, username: str) -> None:
        del self.sessions[username]

    def get_all_sessions(self) -> dict:
        return self.sessions
