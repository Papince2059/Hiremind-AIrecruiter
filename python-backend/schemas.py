from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    picture: Optional[str] = None
    provider: str = "google"

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Interview schemas
class InterviewBase(BaseModel):
    job_title: str
    description: Optional[str] = None
    duration: str = "15 Min"
    interview_type: str
    created_by: Optional[str] = None
    user_name: Optional[str] = None
    questions: Optional[str] = None
    feedback: Optional[str] = None
    
    class Config:
        from_attributes = True

class InterviewCreate(InterviewBase):
    pass

class InterviewUpdate(BaseModel):
    job_title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    interview_type: Optional[str] = None
    created_by: Optional[str] = None
    user_name: Optional[str] = None
    questions: Optional[str] = None
    feedback: Optional[str] = None

class Interview(InterviewBase):
    id: int
    created_at: Optional[datetime] = None  # Made optional to handle existing records
    # user_id: int  # Commented out due to database schema

    class Config:
        from_attributes = True
        populate_by_name = True

# AI Question Generation schemas
class QuestionRequest(BaseModel):
    job_title: str
    job_description: Optional[str] = None
    interview_type: str
    difficulty_level: str = "medium"
    num_questions: int = 5

class QuestionResponse(BaseModel):
    questions: List[Dict[str, Any]]

# AI Feedback schemas
class FeedbackRequest(BaseModel):
    interviewId: int
    userName: str
    conversation: List[Dict[str, Any]]
    duration: int

class FeedbackResponse(BaseModel):
    feedback: str
    score: int
    strengths: List[str]
    areas_for_improvement: List[str]

# OAuth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
