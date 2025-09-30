from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import QuestionRequest, QuestionResponse
from auth import get_current_user
import openai
import json
from config import settings

router = APIRouter()

# OpenAI API key is now set per client instance

@router.post("/questions", response_model=QuestionResponse)
async def generate_questions(
    request: QuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI-powered interview questions"""
    try:
        # Create prompt for question generation
        prompt = f"""
        Generate {request.num_questions} interview questions for a {request.job_title} position.
        
        Job Description: {request.job_description or 'Not provided'}
        Interview Type: {request.interview_type}
        Difficulty Level: {request.difficulty_level}
        
        Please generate questions that are:
        1. Relevant to the job title and description
        2. Appropriate for the interview type (technical, behavioral, experience-based)
        3. Matched to the difficulty level ({request.difficulty_level})
        4. Professional and clear
        
        Return the questions as a JSON array with the following format:
        [
            {{
                "question": "Question text here",
                "type": "technical/behavioral/experience",
                "difficulty": "easy/medium/hard",
                "expected_answer_length": "short/medium/long"
            }}
        ]
        """
        
        # Check if API keys are valid before attempting API calls
        if not settings.openai_api_key or settings.openai_api_key == "":
            print("No OpenAI API key provided, using fallback questions")
            questions = [
                {"text": f"What is your experience with {request.job_title}?", "type": request.interview_type, "difficulty": request.difficulty_level},
                {"text": f"Describe a challenging project you worked on related to {request.job_title}", "type": request.interview_type, "difficulty": request.difficulty_level},
                {"text": f"How do you stay updated with the latest trends in {request.job_title}?", "type": request.interview_type, "difficulty": request.difficulty_level},
                {"text": f"What tools and technologies do you use for {request.job_title}?", "type": request.interview_type, "difficulty": request.difficulty_level},
                {"text": f"Tell me about a time you had to learn a new technology for {request.job_title}", "type": request.interview_type, "difficulty": request.difficulty_level}
            ]
            return QuestionResponse(questions=questions)
        
        # Call OpenAI API (with fallback for testing)
        try:
            client = openai.OpenAI(api_key=settings.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert HR professional and technical interviewer. Generate high-quality interview questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
        except Exception as e:
            # Try Groq as fallback when OpenAI fails
            print(f"OpenAI API error: {e}")
            try:
                from groq import Groq
                groq_client = Groq(api_key="gsk_your_groq_api_key_here")  # You'll need to set this
                response = groq_client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": "You are an expert HR professional and technical interviewer. Generate high-quality interview questions."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                print("Successfully used Groq as fallback")
            except Exception as groq_error:
                print(f"Groq API error: {groq_error}")
                # Final fallback: return mock questions
                questions = [
                    {"text": f"What is your experience with {request.job_title}?", "type": request.interview_type, "difficulty": request.difficulty_level},
                    {"text": f"Describe a challenging project you worked on related to {request.job_title}", "type": request.interview_type, "difficulty": request.difficulty_level},
                    {"text": f"How do you stay updated with the latest trends in {request.job_title}?", "type": request.interview_type, "difficulty": request.difficulty_level},
                    {"text": f"What tools and technologies do you use for {request.job_title}?", "type": request.interview_type, "difficulty": request.difficulty_level},
                    {"text": f"Tell me about a time you had to learn a new technology for {request.job_title}", "type": request.interview_type, "difficulty": request.difficulty_level}
                ]
                return QuestionResponse(questions=questions)
        
        # Parse the response
        content = response.choices[0].message.content.strip()
        
        # Try to extract JSON from the response
        try:
            # Find JSON array in the response
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                questions = json.loads(json_str)
            else:
                # Fallback: create questions from the text
                questions = [{"text": content, "type": request.interview_type, "difficulty": request.difficulty_level}]
        except json.JSONDecodeError:
            # Fallback: create a single question from the response
            questions = [{"text": content, "type": request.interview_type, "difficulty": request.difficulty_level}]
        
        return QuestionResponse(questions=questions)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate questions: {str(e)}"
        )

@router.post("/questions/custom")
async def generate_custom_questions(
    job_title: str,
    job_description: str,
    interview_type: str,
    difficulty_level: str = "medium",
    num_questions: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate custom questions with more control"""
    try:
        # Create a more detailed prompt
        prompt = f"""
        As an expert interviewer, create {num_questions} interview questions for a {job_title} position.
        
        Job Details:
        - Title: {job_title}
        - Description: {job_description}
        - Interview Type: {interview_type}
        - Difficulty: {difficulty_level}
        
        Requirements:
        1. Questions should be specific to {job_title}
        2. Match the {interview_type} interview style
        3. Be appropriate for {difficulty_level} level
        4. Include a mix of open-ended and specific questions
        5. Consider both technical skills and soft skills
        
        Format each question with:
        - The question text
        - Question type (technical/behavioral/experience)
        - Difficulty level
        - Expected answer length
        - Key points to evaluate
        
        Return as a structured JSON array.
        """
        
        client = openai.OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior HR professional with expertise in technical and behavioral interviewing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.6
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON response
        try:
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                questions = json.loads(json_str)
            else:
                # Create fallback questions
                questions = [{"text": content, "type": interview_type, "difficulty": difficulty_level}]
        except json.JSONDecodeError:
            questions = [{"text": content, "type": interview_type, "difficulty": difficulty_level}]
        
        return {"questions": questions, "job_title": job_title, "interview_type": interview_type}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate custom questions: {str(e)}"
        )
