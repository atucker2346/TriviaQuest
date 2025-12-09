import sqlite3
import os
from datetime import date

def migrate_database():
    """Add new tables and columns for enhanced features"""
    
    db_path = os.path.join(os.path.dirname(__file__), "questions.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Starting database migration...")
    
    # Add time_limit column to questions table
    try:
        cursor.execute("""
            ALTER TABLE questions ADD COLUMN time_limit INTEGER DEFAULT 30
        """)
        print("✓ Added time_limit column to questions")
    except sqlite3.OperationalError:
        print("- time_limit column already exists")
    
    # Create daily_challenges table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE UNIQUE NOT NULL,
            category TEXT NOT NULL,
            question_ids TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created daily_challenges table")
    
    # Create daily_challenge_scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_challenge_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            time_taken INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (challenge_id) REFERENCES daily_challenges(id),
            FOREIGN KEY (player_id) REFERENCES players(id),
            UNIQUE(challenge_id, player_id)
        )
    """)
    print("✓ Created daily_challenge_scores table")
    
    # Create player_streaks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_streaks (
            player_id INTEGER PRIMARY KEY,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_played_date DATE,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    """)
    print("✓ Created player_streaks table")
    
    # Add time_taken column to scores table
    try:
        cursor.execute("""
            ALTER TABLE scores ADD COLUMN time_taken INTEGER
        """)
        print("✓ Added time_taken column to scores")
    except sqlite3.OperationalError:
        print("- time_taken column already exists")
    
    # Add hints_used column to scores table
    try:
        cursor.execute("""
            ALTER TABLE scores ADD COLUMN hints_used INTEGER DEFAULT 0
        """)
        print("✓ Added hints_used column to scores")
    except sqlite3.OperationalError:
        print("- hints_used column already exists")
    
    # Create indexes for better performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_daily_challenges_date 
        ON daily_challenges(date DESC)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_daily_challenge_scores_player 
        ON daily_challenge_scores(player_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_daily_challenge_scores_challenge 
        ON daily_challenge_scores(challenge_id)
    """)
    
    print("✓ Created performance indexes")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database migration completed successfully!")

if __name__ == "__main__":
    migrate_database()
