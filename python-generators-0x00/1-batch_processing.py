#!/usr/bin/python3
"""
Batch processing for user_data table
"""

import mysql.connector
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """
    Generator that fetches users in batches of `batch_size`.
    Yields one user at a time as a dictionary.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    offset = 0

    while True:
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s",
            (batch_size, offset)
        )
        rows = cursor.fetchall()
        if not rows:
            break
        for row in rows:  # Yield each user individually
            yield row
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches and prints users over age 25.
    """
    batch = []
    for user in stream_users_in_batches(batch_size):
        if user['age'] > 25:
            batch.append(user)
        # Process the batch in chunks
        if len(batch) >= batch_size:
            for u in batch:
                print(u)
            batch = []

    # Print remaining users in the last batch
    for u in batch:
        print(u)
