from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:12345@localhost:5432/Hiremind_db"
    
    # API Keys
    vapi_api_key: str = os.getenv("VAPI_API_KEY", "")
    vapi_assistant_id: str = os.getenv("VAPI_ASSISTANT_ID", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # OAuth2
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    github_client_id: str = os.getenv("GITHUB_CLIENT_ID", "")
    github_client_secret: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"
    
    class Config:
        env_file = ".env"

settings = Settings()
