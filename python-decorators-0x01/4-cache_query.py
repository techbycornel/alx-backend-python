#!/usr/bin/env python3
import sqlite3
import functools

query_cache = {}


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# Cache decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else args[0]
        if query in query_cache:
            print("[CACHE] Returning cached result")
            return query_cache[query]
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("[CACHE] Caching new result")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will use the cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
