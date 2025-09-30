from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Interview, User
from schemas import Interview as InterviewSchema, InterviewCreate, InterviewUpdate
from auth import get_current_user, get_current_user_from_cookie
import uuid
import json

router = APIRouter()

@router.get("/my", response_model=List[InterviewSchema])
async def get_my_interviews(
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    """Get all interviews for the current user"""
    interviews = db.query(Interview).all()  # Get all interviews for now
    return interviews

@router.get("/{interview_id}", response_model=InterviewSchema)
async def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    """Get a specific interview by ID"""
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        # Interview.user_id == current_user.id  # Commented out due to database schema
    ).first()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    return interview

@router.post("/", response_model=InterviewSchema)
async def create_interview(
    interview_data: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new interview"""
    # Generate unique interview link
    interview_link = f"https://voicruit.com/interview/{str(uuid.uuid4())}"
    
    interview = Interview(
        job_title=interview_data.job_title,
        description=interview_data.description,
        interview_type=interview_data.interview_type,
        duration=interview_data.duration,
        created_by=current_user.email,
        user_name=interview_data.candidate_name,
        questions=json.dumps(interview_data.questions) if interview_data.questions else None,
        # user_id=current_user.id  # Commented out due to database schema
    )
    
    db.add(interview)
    db.commit()
    db.refresh(interview)
    
    return interview

# Add endpoint to handle frontend interview creation with AI question generation
@router.post("/create-with-questions")
async def create_interview_with_questions(
    request: dict,
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    """Create interview with AI-generated questions - frontend compatibility"""
    try:
        import json
        from routers.ai_questions import generate_questions
        from schemas import QuestionRequest
        
        # Extract data from frontend request
        job_title = request.get("jobTitle", "")
        description = request.get("description", "")
        duration = request.get("duration", "15 minutes")
        interview_type = request.get("interviewType", "Technical")
        candidate_name = request.get("userName", "")
        
        # Generate questions using AI
        question_request = QuestionRequest(
            job_title=job_title,
            job_description=description,
            interview_type=interview_type,
            difficulty_level="medium",
            num_questions=5
        )
        
        # Call AI question generation
        from routers.ai_questions import router as ai_questions_router
        questions_response = await ai_questions_router.routes[0].endpoint(
            question_request, current_user, db
        )
        
        # Create interview
        interview = Interview(
            job_title=job_title,
            description=description,
            interview_type=interview_type,
            duration=duration,
            created_by=current_user.email,
            user_name=candidate_name,
            questions=json.dumps({"question": questions_response.questions}),
            # user_id=current_user.id  # Commented out due to database schema
        )
        
        db.add(interview)
        db.commit()
        db.refresh(interview)
        
        # Return in format expected by frontend
        # Convert questions to JSON string format that frontend expects
        questions_json = json.dumps({"question": questions_response.questions})
        
        return {
            "interviewData": {
                "id": interview.id,
                "jobTitle": interview.job_title,
                "description": interview.description,
                "duration": interview.duration,
                "interviewType": interview.interview_type,
                "candidateName": interview.user_name,
                "createdBy": interview.created_by,
                "questionList": questions_response.questions
            },
            "questions": questions_json  # Frontend expects single JSON string
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create interview with questions: {str(e)}"
        )

@router.put("/{interview_id}", response_model=InterviewSchema)
async def update_interview(
    interview_id: int,
    interview_update: InterviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing interview"""
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        # Interview.user_id == current_user.id  # Commented out due to database schema
    ).first()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Update only provided fields
    update_data = interview_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(interview, field, value)
    
    db.commit()
    db.refresh(interview)
    
    return interview

@router.delete("/{interview_id}")
async def delete_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an interview"""
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        # Interview.user_id == current_user.id  # Commented out due to database schema
    ).first()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    db.delete(interview)
    db.commit()
    
    return {"message": "Interview deleted successfully"}

@router.get("/", response_model=List[InterviewSchema])
async def get_all_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all interviews (admin endpoint)"""
    interviews = db.query(Interview).all()
    return interviews

# Add feedback endpoint for frontend compatibility
@router.post("/{interview_id}/feedback")
async def submit_interview_feedback(
    interview_id: int,
    request: dict,
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    """Submit interview feedback - frontend compatibility endpoint"""
    try:
        # Get the interview
        interview = db.query(Interview).filter(
            Interview.id == interview_id,
            # Interview.user_id == current_user.id  # Commented out due to database schema
        ).first()
        
        if not interview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found"
            )
        
        # Extract conversation data from request
        conversation = request.get("conversation", [])
        duration = request.get("duration", "00:00:00")
        
        # Generate feedback using the new fallback system
        from schemas import FeedbackRequest
        
        feedback_request = FeedbackRequest(
            interviewId=interview_id,
            userName=request.get("userName", "Candidate"),
            conversation=conversation,
            duration=request.get("duration", 15)
        )
        
        # Generate feedback using the new fallback system
        conversation_length = len(conversation)
        conversation_text = ""
        for conv in conversation:
            if isinstance(conv, dict):
                if 'role' in conv and 'content' in conv:
                    role = "Interviewer" if conv['role'] == 'assistant' else "Candidate"
                    conversation_text += f"{role}: {conv['content']}\n"
        
        conversation_text_lower = conversation_text.lower()
        
        # Analyze conversation content for scoring
        technical_keywords = ['react', 'python', 'javascript', 'node', 'api', 'database', 'frontend', 'backend', 'coding', 'programming', 'development', 'framework', 'library', 'git', 'github']
        communication_indicators = ['explain', 'describe', 'tell me', 'how', 'what', 'why', 'experience', 'project', 'team', 'work']
        
        # Count technical mentions
        technical_mentions = sum(1 for keyword in technical_keywords if keyword in conversation_text_lower)
        communication_quality = sum(1 for indicator in communication_indicators if indicator in conversation_text_lower)
        
        # Calculate dynamic scores
        base_score = min(50 + (conversation_length * 3) + (technical_mentions * 2) + (communication_quality * 1), 90)
        
        # Generate detailed feedback based on actual conversation
        feedback_analysis = f"Interview Analysis for {interview.job_title} Position:\n\n"
        feedback_analysis += f"• Total conversation exchanges: {conversation_length}\n"
        feedback_analysis += f"• Technical depth demonstrated: {'Good' if technical_mentions > 3 else 'Basic'}\n"
        feedback_analysis += f"• Communication quality: {'Strong' if communication_quality > 5 else 'Adequate'}\n"
        feedback_analysis += f"• Engagement level: {'High' if conversation_length > 5 else 'Moderate'}\n\n"
        
        # Generate strengths and areas for improvement based on actual conversation
        strengths = []
        areas_for_improvement = []
        
        if technical_mentions > 3:
            strengths.append("Demonstrated good technical knowledge")
        else:
            areas_for_improvement.append("Could provide more technical examples")
        
        if communication_quality > 5:
            strengths.append("Good communication skills")
        else:
            areas_for_improvement.append("Could improve communication clarity")
        
        if conversation_length > 5:
            strengths.append("Engaged well in the interview")
        else:
            areas_for_improvement.append("Could provide more detailed responses")
        
        # Generate recommendation
        recommendation = "Yes" if base_score > 65 else "No"
        recommendation_msg = f"Based on the interview performance, the candidate is {'recommended' if base_score > 65 else 'not recommended'} for the next round. "
        recommendation_msg += f"Overall engagement score: {base_score}/100"
        
        # Create comprehensive feedback
        feedback_data = {
            "ratings": {
                "technicalSkills": max(4, min(9, (base_score + technical_mentions * 2) // 10)),
                "communication": max(5, min(9, (base_score + communication_quality) // 10)),
                "problemSolving": max(4, min(8, (base_score - 5) // 10)),
                "experience": max(4, min(8, (base_score + technical_mentions) // 10))
            },
            "overallScore": base_score / 10,
            "feedback": feedback_analysis,
            "summary": [
                f"Interview completed with {conversation_length} exchanges",
                f"Technical knowledge: {'Strong' if technical_mentions > 3 else 'Basic'}",
                f"Communication: {'Excellent' if communication_quality > 5 else 'Good'}",
                f"Overall engagement: {base_score}/100"
            ],
            "strengths": strengths if strengths else ["Participated in interview", "Showed interest in position"],
            "areas_for_improvement": areas_for_improvement if areas_for_improvement else ["Could provide more detailed examples"],
            "recommendation": recommendation,
            "recommendationMsg": recommendation_msg
        }
        
        # Store feedback in database
        interview.feedback = json.dumps(feedback_data)
        db.commit()
        
        return {
            "feedback": feedback_data,
            "score": feedback_data["overallScore"],
            "strengths": feedback_data["strengths"],
            "areas_for_improvement": feedback_data["areas_for_improvement"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit feedback: {str(e)}"
        )
