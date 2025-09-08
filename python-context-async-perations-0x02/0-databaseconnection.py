#!/usr/bin/env python3
"""
Task 0: Custom class-based context manager for database connection
"""

import sqlite3


class DatabaseConnection:
    """Custom context manager for handling SQLite DB connection."""

    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
