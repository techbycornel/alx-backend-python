#!/usr/bin/python3
import uuid

"""
seed.py
Setup script for ALX_prodev database and user_data table.
"""

import mysql.connector
import csv


def connect_db():
    """Connects to the MySQL server (not a specific DB)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # <-- update if needed
            password="Password6$"   # <-- update if needed
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error while connecting: {err}")
        return None


def create_database(connection):
    """Creates ALX_prodev database if it doesn’t exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()


def connect_to_prodev():
    """Connects directly to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # <-- update if needed
            password="Password6$",  # <-- update if needed
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error while connecting to ALX_prodev: {err}")
        return None


def create_table(connection):
    """Creates user_data table if not exists."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()


def insert_data(connection, csv_file):
    """Insert data from CSV file if not already inserted."""
    try:
        cursor = connection.cursor()

        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Generate UUID since CSV has no user_id
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # Check if email already exists (avoid duplicates)
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (user_id, name, email, age))

        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")

