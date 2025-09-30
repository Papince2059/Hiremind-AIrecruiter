# 🔧 Voicruit Python Backend - Complete Setup Guide

This guide will walk you through setting up all the required API keys and configurations for the Voicruit Python backend.

## 📋 Prerequisites

- Python 3.8+ installed
- PostgreSQL database running
- Internet connection for API key generation

## 🔑 Step-by-Step Configuration

### 1. OpenAI API Key Setup

**Purpose**: Generate AI-powered interview questions and feedback

**Steps**:
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to "API Keys" in the left sidebar
4. Click "Create new secret key"
5. Name it "Voicruit Backend"
6. Copy the key (starts with `sk-`)
7. Add to your `.env` file:
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

**Cost**: ~$0.002 per 1K tokens (very affordable for testing)

### 2. Vapi AI API Key Setup

**Purpose**: Voice interaction and conversation management

**Steps**:
1. Visit [Vapi AI Dashboard](https://dashboard.vapi.ai/)
2. Sign up for an account
3. Go to "API Keys" section
4. Generate a new API key
5. Copy the key
6. Add to your `.env` file:
   ```env
   VAPI_API_KEY=your-vapi-key-here
   VAPI_ASSISTANT_ID=your-assistant-id-here
   ```

**Note**: You may need to create an assistant first in the Vapi dashboard.

### 3. Google OAuth2 Setup

**Purpose**: User authentication with Google accounts

**Steps**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable APIs:
   - Go to "APIs & Services" → "Library"
   - Search and enable "Google+ API"
   - Search and enable "People API"
4. Create OAuth credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client IDs"
   - Application type: "Web application"
   - Name: "Voicruit Backend"
   - Authorized redirect URIs: `http://localhost:8080/login/oauth2/code/google`
5. Copy Client ID and Client Secret
6. Add to your `.env` file:
   ```env
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```

### 4. GitHub OAuth2 Setup

**Purpose**: Alternative authentication with GitHub accounts

**Steps**:
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the form:
   - Application name: "Voicruit"
   - Homepage URL: `http://localhost:3000`
   - Application description: "AI Voice Recruiter Platform"
   - Authorization callback URL: `http://localhost:8080/login/oauth2/code/github`
4. Click "Register application"
5. Copy Client ID and Client Secret
6. Add to your `.env` file:
   ```env
   GITHUB_CLIENT_ID=your-github-client-id
   GITHUB_CLIENT_SECRET=your-github-client-secret
   ```

### 5. JWT Secret Key Generation

**Purpose**: Secure token signing for authentication

**Generate a secure secret key**:
```python
import secrets
print(secrets.token_urlsafe(32))
```

Or use this online generator: https://generate-secret.vercel.app/32

Add to your `.env` file:
```env
SECRET_KEY=your-generated-secret-key-here
```

### 6. Database Configuration

**Setup PostgreSQL**:
1. Install PostgreSQL on your system
2. Create a database:
   ```sql
   CREATE DATABASE recruiter_db;
   CREATE USER postgres WITH PASSWORD '12345';
   GRANT ALL PRIVILEGES ON DATABASE recruiter_db TO postgres;
   ```
3. Update your `.env` file:
   ```env
   DATABASE_URL=postgresql://postgres:12345@localhost:5432/recruiter_db
   ```

## 📄 Complete .env File Example

Create a `.env` file in the `python-backend` directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:12345@localhost:5432/recruiter_db

# API Keys
VAPI_API_KEY=your-vapi-api-key-here
VAPI_ASSISTANT_ID=your-vapi-assistant-id-here
OPENAI_API_KEY=sk-your-openai-key-here

# OAuth2 Configuration
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
GITHUB_CLIENT_ID=your-github-client-id-here
GITHUB_CLIENT_SECRET=your-github-client-secret-here

# JWT Configuration
SECRET_KEY=your-generated-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 🚀 Testing Your Configuration

### 1. Install Dependencies
```bash
cd Voicruiter/python-backend
pip install -r requirements.txt
```

### 2. Test Database Connection
```bash
python -c "
from database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Database connection successful!')
"
```

### 3. Test API Keys
```bash
python -c "
import openai
import os
from dotenv import load_dotenv
load_dotenv()

# Test OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
print('OpenAI API key loaded successfully!')

# Test other keys
print(f'Vapi key: {os.getenv(\"VAPI_API_KEY\")[:10]}...')
print(f'Google Client ID: {os.getenv(\"GOOGLE_CLIENT_ID\")[:10]}...')
"
```

### 4. Run the Application
```bash
python main.py
```

Visit `http://localhost:8080/docs` to see the API documentation.

## 🔧 Troubleshooting

### Common Issues:

1. **Database Connection Error**:
   - Ensure PostgreSQL is running
   - Check database credentials
   - Verify database exists

2. **OAuth2 Errors**:
   - Check redirect URIs match exactly
   - Ensure APIs are enabled in Google Cloud Console
   - Check client ID and secret are correct

3. **OpenAI API Errors**:
   - Verify API key is correct
   - Check you have credits in your OpenAI account
   - Ensure you're using the correct model

4. **Import Errors**:
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+)
   - Verify virtual environment is activated

## 💰 Cost Estimation

- **OpenAI API**: ~$5-10/month for moderate usage
- **Vapi AI**: Check their pricing at https://vapi.ai/pricing
- **Google OAuth**: Free
- **GitHub OAuth**: Free
- **PostgreSQL**: Free (self-hosted)

## 🆘 Need Help?

If you encounter issues:

1. Check the logs for specific error messages
2. Verify all environment variables are set correctly
3. Test each API key individually
4. Ensure all services are running (PostgreSQL, etc.)

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Vapi AI Documentation](https://docs.vapi.ai/)
- [Google OAuth2 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
