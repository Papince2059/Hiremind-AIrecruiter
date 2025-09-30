from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import User as UserSchema, Token
from auth import create_access_token, get_or_create_user, get_current_user
from config import settings
import httpx
import json

router = APIRouter()

@router.post("/google", response_model=Token)
async def google_auth(request: dict, db: Session = Depends(get_db)):
    """Authenticate user with Google OAuth token"""
    try:
        token = request.get("token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token is required"
            )
        
        # Verify Google token
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={token}"
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Google token"
                )
            
            user_info = response.json()
            email = user_info.get("email")
            name = user_info.get("name")
            picture = user_info.get("picture")
            
            if not email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email not provided by Google"
                )
            
            # Get or create user
            user = get_or_create_user(email, name, picture, "google", db)
            
            # Create access token
            access_token = create_access_token(data={"sub": user.email})
            
            return {"access_token": access_token, "token_type": "bearer"}
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

# Add OAuth2 authorization endpoints for frontend compatibility
@router.get("/oauth2/authorization/google")
async def google_oauth_redirect():
    """Google OAuth2 authorization redirect - frontend compatibility"""
    # This would typically redirect to Google's OAuth2 consent screen
    # For now, return a message indicating the frontend should handle this
    return {"message": "Redirect to Google OAuth2 consent screen"}

@router.get("/oauth2/authorization/github")
async def github_oauth_redirect():
    """GitHub OAuth2 authorization redirect - frontend compatibility"""
    # This would typically redirect to GitHub's OAuth2 consent screen
    # For now, return a message indicating the frontend should handle this
    return {"message": "Redirect to GitHub OAuth2 consent screen"}

@router.post("/github", response_model=Token)
async def github_auth(request: dict, db: Session = Depends(get_db)):
    """Authenticate user with GitHub OAuth"""
    try:
        code = request.get("code")
        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code is required"
            )
        
        # Exchange code for access token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": settings.github_client_id,
                    "client_secret": settings.github_client_secret,
                    "code": code
                },
                headers={"Accept": "application/json"}
            )
            
            if token_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to exchange GitHub code"
                )
            
            token_data = token_response.json()
            access_token = token_data.get("access_token")
            
            if not access_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No access token received from GitHub"
                )
            
            # Get user info from GitHub
            user_response = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"token {access_token}"}
            )
            
            if user_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to get user info from GitHub"
                )
            
            user_info = user_response.json()
            email = user_info.get("email")
            name = user_info.get("name") or user_info.get("login")
            picture = user_info.get("avatar_url")
            
            if not email:
                # Try to get email from GitHub API
                email_response = await client.get(
                    "https://api.github.com/user/emails",
                    headers={"Authorization": f"token {access_token}"}
                )
                if email_response.status_code == 200:
                    emails = email_response.json()
                    primary_email = next((e for e in emails if e.get("primary")), None)
                    if primary_email:
                        email = primary_email.get("email")
            
            if not email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email not available from GitHub"
                )
            
            # Get or create user
            user = get_or_create_user(email, name, picture, "github", db)
            
            # Create access token
            jwt_token = create_access_token(data={"sub": user.email})
            
            return {"access_token": jwt_token, "token_type": "bearer"}
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"GitHub authentication failed: {str(e)}"
        )

@router.get("/me", response_model=UserSchema)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.post("/logout")
async def logout():
    """Logout user (client-side token removal)"""
    return {"message": "Successfully logged out"}
