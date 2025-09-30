#!/usr/bin/env python3
"""
Generate SECRET_KEY and test database connection
"""

import os
import secrets
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_secret_key():
    """Generate a secure SECRET_KEY"""
    return secrets.token_urlsafe(32)

def test_database_connection():
    """Test database connection"""
    try:
        database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:12345@localhost:5432/hiremind_db')
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
        print("Database connection successful!")
        print(f"   Database URL: {database_url}")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def main():
    print("Generating SECRET_KEY for your .env file...")
    print("=" * 50)
    
    # Generate SECRET_KEY
    secret_key = generate_secret_key()
    print(f"SECRET_KEY={secret_key}")
    print()
    
    print("Add this to your python-backend/.env file:")
    print("-" * 30)
    print(f"SECRET_KEY={secret_key}")
    print()
    
    print("Testing database connection...")
    if test_database_connection():
        print("Everything is ready!")
    else:
        print("Please check your DATABASE_URL in .env file")
    
    print()
    print("Complete .env file should look like:")
    print("-" * 30)
    print("# Database Configuration")
    print("DATABASE_URL=postgresql://postgres:Papince$2059@localhost:5432/hiremind_db")
    print()
    print("# JWT Configuration")
    print(f"SECRET_KEY={secret_key}")
    print("ALGORITHM=HS256")
    print("ACCESS_TOKEN_EXPIRE_MINUTES=30")
    print()
    print("# API Keys (Get these from respective services)")
    print("OPENAI_API_KEY=your_openai_api_key_here")
    print("VAPI_API_KEY=your_vapi_api_key_here")
    print()
    print("# CORS Configuration")
    print("ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000")

if __name__ == "__main__":
    main()