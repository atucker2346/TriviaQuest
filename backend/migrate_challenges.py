import sqlite3
import os

def migrate_challenges():
    """Add challenge mode tables"""
    
    db_path = os.path.join(os.path.dirname(__file__), "questions.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Starting challenge mode migration...")
    
    # Create challenge_rooms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS challenge_rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            question_ids TEXT NOT NULL,
            created_by INTEGER NOT NULL,
            max_players INTEGER DEFAULT 10,
            status TEXT DEFAULT 'waiting',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES players(id)
        )
    """)
    print("✓ Created challenge_rooms table")
    
    # Create challenge_participants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS challenge_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            status TEXT DEFAULT 'waiting',
            score INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 0,
            time_taken INTEGER,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (challenge_id) REFERENCES challenge_rooms(id),
            FOREIGN KEY (player_id) REFERENCES players(id),
            UNIQUE(challenge_id, player_id)
        )
    """)
    print("✓ Created challenge_participants table")
    
    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_challenge_rooms_code 
        ON challenge_rooms(room_code)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_challenge_participants_challenge 
        ON challenge_participants(challenge_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_challenge_participants_player 
        ON challenge_participants(player_id)
    """)
    
    print("✓ Created performance indexes")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Challenge mode migration completed successfully!")

if __name__ == "__main__":
    migrate_challenges()

