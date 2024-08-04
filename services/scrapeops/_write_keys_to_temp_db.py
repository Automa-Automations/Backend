import sqlite3
import time

# File containing the keys
keys_file = "keys.txt"

# Connect to the SQLite database (change the path if necessary)
conn = sqlite3.connect("sqlite.db")
cursor = conn.cursor()

# Ensure the table exists
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS api_keys (
    key TEXT NOT NULL PRIMARY KEY,
    expired BOOLEAN NOT NULL,
    created_at INTEGER NOT NULL
)
"""
)

# Read keys from the file
with open(keys_file, "r") as file:
    keys = file.readlines()

# Current Unix timestamp
current_timestamp = int(time.time())

# Insert keys into the database
for key in keys:
    key = key.strip()
    if key:
        cursor.execute(
            """
        INSERT OR IGNORE INTO api_keys (key, expired, created_at)
        VALUES (?, ?, ?)
        """,
            (key, False, current_timestamp),
        )

# Commit changes and close the connection
conn.commit()
conn.close()
