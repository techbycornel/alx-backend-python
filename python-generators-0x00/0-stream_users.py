#!/usr/bin/python3
"""
0-stream_users.py
Generator that streams rows from user_data table one by one.
"""

import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that fetches rows from user_data one by one."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",         # update if needed
            password="Password6$",
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)  # dictionary=True gives dict instead of tuple
        cursor.execute("SELECT * FROM user_data;")

        for row in cursor:
            yield row  # yields one row at a time

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error while streaming users: {e}")
