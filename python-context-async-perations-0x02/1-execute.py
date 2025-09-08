#!/usr/bin/env python3
"""
Task 1: Reusable query context manager
"""

import sqlite3


class ExecuteQuery:
    """Context manager that executes a given SQL query with parameters."""

    def __init__(self, query, params=(), db_name="users.db"):
        self.query = query
        self.params = params
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(query, params) as result:
        for row in result:
            print(row)
