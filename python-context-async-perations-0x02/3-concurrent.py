#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries using aiosqlite
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    """Run both queries concurrently."""
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\nAll Users:")
    for user in users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
