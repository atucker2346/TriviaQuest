import sqlite3
import os

def add_scoreboard_tables():
    """Add scoreboard tables to the existing database"""
    
    # Get the database path
    db_path = os.path.join(os.path.dirname(__file__), "questions.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create players table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    """)
    
    # Create index for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_scores_player_id 
        ON scores(player_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_scores_played_at 
        ON scores(played_at DESC)
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Scoreboard tables created successfully!")

if __name__ == "__main__":
    add_scoreboard_tables()
