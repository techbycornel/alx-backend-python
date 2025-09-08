import sqlite3

def setup_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Drop table if it exists (so you can rerun without errors)
    cursor.execute("DROP TABLE IF EXISTS users")

    # Create users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    # Insert sample users
    sample_users = [
        ("Alice", 25),
        ("Bob", 30),
        ("Charlie", 22),
        ("David", 45),
        ("Eve", 50),
    ]

    cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", sample_users)

    conn.commit()
    conn.close()
    print("✅ Database setup complete! 'users' table created with sample data.")

if __name__ == "__main__":
    setup_database()
