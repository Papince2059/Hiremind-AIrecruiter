#!/usr/bin/env python3
"""
Voicruit Backend Configuration Setup Script
This script helps you set up all the required API keys and configurations
"""

import os
import secrets
import subprocess
import sys
from pathlib import Path

def generate_secret_key():
    """Generate a secure JWT secret key"""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Create .env file with template values"""
    env_content = f"""# Database Configuration
DATABASE_URL=postgresql://postgres:12345@localhost:5432/recruiter_db

# API Keys
VAPI_API_KEY=your_vapi_api_key_here
VAPI_ASSISTANT_ID=your_vapi_assistant_id_here
OPENAI_API_KEY=your_openai_api_key_here

# OAuth2 Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here

# JWT Configuration
SECRET_KEY={generate_secret_key()}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with template configuration")
    print("🔑 Generated secure JWT secret key")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import sqlalchemy
        import openai
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Make sure PostgreSQL is running and database exists")
        return False

def main():
    """Main setup function"""
    print("🚀 Voicruit Python Backend Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Please run this script from the python-backend directory")
        sys.exit(1)
    
    # Create .env file
    if not Path(".env").exists():
        create_env_file()
    else:
        print("✅ .env file already exists")
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Test database connection
    print("\n🔍 Testing database connection...")
    test_database_connection()
    
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your actual API keys")
    print("2. See SETUP_GUIDE.md for detailed instructions")
    print("3. Run: python main.py")
    print("4. Visit: http://localhost:8080/docs")
    
    print("\n🔗 Quick Links:")
    print("- OpenAI API: https://platform.openai.com/api-keys")
    print("- Vapi AI: https://dashboard.vapi.ai/")
    print("- Google OAuth: https://console.cloud.google.com/")
    print("- GitHub OAuth: https://github.com/settings/developers")

if __name__ == "__main__":
    main()
