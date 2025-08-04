import sqlite3

DB_PATH = "mindease.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        emotion TEXT,
        score REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def log_conversation(user_input, bot_response, emotion, score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO sessions (user_input, bot_response, emotion, score) VALUES (?, ?, ?, ?)",
        (user_input, bot_response, emotion, score)
    )
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT emotion, COUNT(*) AS count FROM sessions GROUP BY emotion")
    data = c.fetchall()
    conn.close()
    return data
