import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: str = "app_data.db"):
        self.db_path = db_path
        Path(self.db_path).touch(exist_ok=True)

    def connect(self):
        return sqlite3.connect(self.db_path)

    def execute(self, query: str, params: tuple = ()):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def fetch_all(self, query: str, params: tuple = ()):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = ()):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()