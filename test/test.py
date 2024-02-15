import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from aisqlite import AISQLite

if __name__ == "__main__":
    db = AISQLite('test2')

    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    db.execute("""
    INSERT INTO users (username, email) VALUES (?, ?)
    """, ('sampleuser', 'sampleuser@example.com'))

    db.execute("""
    INSERT INTO users (username, email) VALUES (?, ?)
    """, ('sampleuse2', 'sampleuser2@example.com'))

    db.execute("""
    INSERT INTO users (username, email) VALUES (?, ?)
    """, ('sampleuse3', 'sampleuser3@example.com'))

    users = db.execute_and_fetch("SELECT * FROM users", num=50)
    print("Users:", users)
