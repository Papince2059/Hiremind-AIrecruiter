#!/usr/bin/env python3
"""
Voicruit Automated Setup Script
This script helps you set up the complete Voicruit application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_prerequisites():
    """Check if required software is installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    try:
        python_version = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python: {python_version.stdout.strip()}")
    except:
        print("❌ Python not found. Please install Python 3.8+")
        return False
    
    # Check Node.js
    try:
        node_version = subprocess.run(["node", "--version"], capture_output=True, text=True)
        print(f"✅ Node.js: {node_version.stdout.strip()}")
    except:
        print("❌ Node.js not found. Please install Node.js 16+")
        return False
    
    # Check PostgreSQL
    try:
        psql_version = subprocess.run(["psql", "--version"], capture_output=True, text=True)
        print(f"✅ PostgreSQL: {psql_version.stdout.strip()}")
    except:
        print("❌ PostgreSQL not found. Please install PostgreSQL")
        return False
    
    return True

def setup_database():
    """Set up the database"""
    print("🗄️ Setting up database...")
    
    # Create database
    db_commands = [
        "psql -U postgres -c 'CREATE DATABASE recruiter_db;'",
        "psql -U postgres -c 'GRANT ALL PRIVILEGES ON DATABASE recruiter_db TO postgres;'"
    ]
    
    for command in db_commands:
        if not run_command(command, f"Database setup: {command}"):
            print("⚠️ Database setup failed. Please create database manually:")
            print("   psql -U postgres")
            print("   CREATE DATABASE recruiter_db;")
            print("   \\q")
            return False
    
    return True

def install_dependencies():
    """Install Python and Node.js dependencies"""
    print("📦 Installing dependencies...")
    
    # Install Python dependencies
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Install Node.js dependencies
    if not run_command("npm install", "Installing Node.js dependencies"):
        return False
    
    return True

def create_env_file():
    """Create environment file"""
    print("⚙️ Creating environment configuration...")
    
    env_content = """# Database Configuration
DATABASE_URL=postgresql://postgres:12345@localhost:5432/recruiter_db

# API Keys (Get these from respective services)
VAPI_API_KEY=your_vapi_api_key_here
VAPI_ASSISTANT_ID=your_vapi_assistant_id_here
OPENAI_API_KEY=your_openai_api_key_here

# OAuth2 Configuration (Optional for testing)
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here

# JWT Configuration
SECRET_KEY=your-generated-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
"""
    
    env_file = Path("python-backend/.env")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file with template configuration")
    else:
        print("✅ .env file already exists")
    
    return True

def test_connection():
    """Test database connection"""
    print("🧪 Testing database connection...")
    
    test_script = """
import sys
sys.path.append('python-backend')
from database import engine
from sqlalchemy import text
try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✅ Database connection successful!')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    sys.exit(1)
"""
    
    if not run_command(f"{sys.executable} -c \"{test_script}\"", "Testing database connection"):
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Voicruit Automated Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites not met. Please install required software.")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("⚠️ Database setup failed. Please set up manually.")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed.")
        sys.exit(1)
    
    # Create environment file
    if not create_env_file():
        print("❌ Environment configuration failed.")
        sys.exit(1)
    
    # Test connection
    if not test_connection():
        print("❌ Database connection test failed.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Edit python-backend/.env with your actual API keys")
    print("2. Start backend: cd python-backend && python main.py")
    print("3. Start frontend: cd userpanel && npm run dev")
    print("4. Visit: http://localhost:5173")
    print("\n🔗 Useful URLs:")
    print("- Backend API: http://localhost:8080")
    print("- API Docs: http://localhost:8080/docs")
    print("- Frontend: http://localhost:5173")

if __name__ == "__main__":
    main()
