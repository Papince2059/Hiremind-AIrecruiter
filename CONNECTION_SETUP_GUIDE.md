# Frontend-Backend Connection Setup Guide

## Overview
This guide explains how to connect the React frontend with the Python FastAPI backend for the AI Recruiter application.

## Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm
- PostgreSQL database (optional, SQLite will be used by default)

## Backend Setup (Python FastAPI)

### 1. Navigate to Backend Directory
```bash
cd python-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the `python-backend` directory:
```env
# Database
DATABASE_URL=sqlite:///./recruiter.db

# API Keys (optional for testing)
OPENAI_API_KEY=your_openai_key_here
VAPI_API_KEY=your_vapi_key_here
VAPI_ASSISTANT_ID=your_assistant_id_here

# OAuth2 (optional for testing)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# JWT
SECRET_KEY=your-secret-key-here
```

### 5. Start Backend Server
```bash
python main.py
```
The backend will run on `http://localhost:8080`

## Frontend Setup (React + Vite)

### 1. Navigate to Frontend Directory
```bash
cd userpanel
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Frontend Server
```bash
npm run dev
```
The frontend will run on `http://localhost:5173`

## Quick Start (Windows)
Use the provided batch file:
```bash
start_services.bat
```

## API Endpoints

### Authentication
- `GET /api/user` - Get current user info
- `POST /logout` - Logout user
- `GET /oauth2/authorization/google` - Google OAuth redirect
- `GET /oauth2/authorization/github` - GitHub OAuth redirect

### Interviews
- `GET /api/interviews/my` - Get user's interviews
- `GET /api/interviews/{id}` - Get specific interview
- `POST /api/interviews/create-with-questions` - Create interview with AI questions
- `POST /api/interviews/{id}/feedback` - Submit interview feedback

### AI Services
- `POST /api/ai/questions` - Generate AI questions
- `POST /api/ai/feedback` - Generate AI feedback

## Testing Connection

### 1. Test Backend
```bash
cd python-backend
python test_connection.py
```

### 2. Test Frontend
Open `http://localhost:5173` in your browser

### 3. Test Full Flow
1. Open frontend in browser
2. Try to access dashboard (should redirect to login)
3. Create a new interview
4. Test interview flow

## Troubleshooting

### Common Issues

1. **Backend not starting**
   - Check if port 8080 is available
   - Verify Python dependencies are installed
   - Check database connection

2. **Frontend not connecting to backend**
   - Verify backend is running on port 8080
   - Check CORS settings in backend
   - Verify API endpoints are accessible

3. **Authentication issues**
   - The current setup uses mock authentication for testing
   - For production, implement proper OAuth2 flow

4. **Database issues**
   - SQLite database will be created automatically
   - For PostgreSQL, update DATABASE_URL in .env

### Debug Steps

1. **Check Backend Logs**
   ```bash
   # Look for error messages in terminal where backend is running
   ```

2. **Check Frontend Console**
   ```bash
   # Open browser developer tools and check console for errors
   ```

3. **Test API Endpoints**
   ```bash
   # Use curl or Postman to test endpoints directly
   curl http://localhost:8080/api/user
   ```

## Production Considerations

1. **Authentication**: Implement proper OAuth2 flow
2. **Database**: Use PostgreSQL for production
3. **Security**: Add proper CORS, rate limiting, and security headers
4. **Environment**: Use proper environment variables and secrets management
5. **Deployment**: Consider using Docker for containerization

## File Structure
```
Hiremind/
├── python-backend/          # FastAPI backend
│   ├── main.py             # Main application
│   ├── auth.py             # Authentication logic
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── routers/            # API routers
│   └── requirements.txt    # Python dependencies
├── userpanel/              # React frontend
│   ├── src/                # Source code
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
└── start_services.bat      # Quick start script
```

## Support
If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure both services are running on correct ports
4. Check browser console and backend logs for errors
