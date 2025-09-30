#!/usr/bin/env python3
"""
Script to add user_id column to the interview table
"""
import sqlite3
import os

def add_user_id_column():
    # Connect to the database
    db_path = "interview.db"  # Adjust path as needed
    if not os.path.exists(db_path):
        print("Database file not found. Creating new database...")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if user_id column already exists
        cursor.execute("PRAGMA table_info(interview)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("Adding user_id column to interview table...")
            cursor.execute("ALTER TABLE interview ADD COLUMN user_id INTEGER")
            
            # Set default user_id to 1 for existing records
            cursor.execute("UPDATE interview SET user_id = 1 WHERE user_id IS NULL")
            
            conn.commit()
            print("✅ Successfully added user_id column")
        else:
            print("✅ user_id column already exists")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_user_id_column()
