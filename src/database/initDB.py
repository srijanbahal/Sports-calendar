import sqlite3
import os

def create_database():
    """Create the tournaments database and table"""
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect('data/tournaments.db')
    cursor = conn.cursor()
    
    # Create tournaments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sport TEXT NOT NULL,
            level TEXT NOT NULL,
            start_date DATE,
            end_date DATE,
            official_url TEXT,
            streaming_links TEXT,
            image_url TEXT,
            summary TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sport ON tournaments(sport)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_level ON tournaments(level)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_start_date ON tournaments(start_date)')
    
    conn.commit()
    conn.close()
    print("Database created successfully!")

if __name__ == "__main__":
    create_database()