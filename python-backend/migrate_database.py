#!/usr/bin/env python3
"""
Script to migrate the database to add user_id column
"""
import psycopg2
from config import settings

def migrate_database():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="Hiremind_db",
            user="postgres",
            password="12345"
        )
        cursor = conn.cursor()
        
        # Check if user_id column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'interview' AND column_name = 'user_id'
        """)
        
        if cursor.fetchone() is None:
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
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate_database()
