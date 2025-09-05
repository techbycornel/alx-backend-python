#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """
    Generator that streams user ages one by one from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:   # yields one row at a time
        yield row["age"]

    connection.close()


def average_age():
    """
    Calculate average age using the generator without loading all ages in memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        return 0

    avg = total_age / count
    print(f"Average age of users: {avg:.2f}")
    return avg


if __name__ == "__main__":
    average_age()
