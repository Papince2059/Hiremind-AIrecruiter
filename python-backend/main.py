from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

from database import get_db, engine, Base
from models import Interview, User
from routers import auth, interviews, ai_feedback, ai_questions
from auth import get_current_user, get_current_user_from_cookie
from config import settings

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Voicruit API",
    description="AI Voice Recruiter Backend API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(interviews.router, prefix="/api/interviews", tags=["Interviews"])
app.include_router(ai_feedback.router, prefix="/api/ai", tags=["AI Feedback"])
app.include_router(ai_questions.router, prefix="/api/ai", tags=["AI Questions"])

# Add user endpoint for frontend compatibility
@app.get("/api/user")
async def get_current_user_info(current_user: User = Depends(get_current_user_from_cookie)):
    """Get current user information - frontend compatibility endpoint"""
    return current_user

# Add logout endpoint for frontend compatibility  
@app.post("/logout")
async def logout():
    """Logout user (client-side token removal) - frontend compatibility endpoint"""
    return {"message": "Successfully logged out"}

@app.get("/")
async def root():
    return {"message": "Voicruit API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )
