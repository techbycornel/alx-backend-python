#!/usr/bin/python3
"""
0-stream_users.py
Generator that streams rows from user_data table one by one.
"""

import mysql.connector


def stream_users():
    """Generator that yields users from the database one by one"""
    # connect to DB
    conn = mysql.connector.connect(
        host="localhost",
        user="root",        # change if needed
        password="Password6$",  # change if needed
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)  # return rows as dicts

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:  # only one loop
        yield row  # generator yields one row at a time

    cursor.close()
    conn.close()
