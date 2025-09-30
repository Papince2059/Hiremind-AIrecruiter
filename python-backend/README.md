# Voicruit Python Backend

A FastAPI-based backend for the Voicruit AI Voice Recruiter platform. This Python backend provides the same functionality as the original Java Spring Boot backend, including OAuth2 authentication, interview management, and AI-powered question generation and feedback.

## 🚀 Features

- **FastAPI Framework**: Modern, fast, and easy-to-use Python web framework
- **OAuth2 Authentication**: Google and GitHub OAuth integration
- **PostgreSQL Database**: Robust data persistence with SQLAlchemy ORM
- **AI Integration**: OpenAI-powered question generation and feedback analysis
- **JWT Security**: Secure token-based authentication
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **RESTful API**: Clean and well-documented API endpoints

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with OAuth2 (Google, GitHub)
- **AI Integration**: OpenAI GPT-3.5-turbo
- **Security**: Passlib for password hashing, python-jose for JWT
- **HTTP Client**: httpx for external API calls

## 📦 Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database
- OpenAI API key
- Google OAuth credentials (optional)
- GitHub OAuth credentials (optional)

### Setup

1. **Clone the repository**
   ```bash
   cd Voicruiter/python-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

5. **Database setup**
   ```bash
   # Create PostgreSQL database
   createdb recruiter_db
   
   # The application will automatically create tables on first run
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8080`

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://postgres:12345@localhost:5432/recruiter_db

# API Keys
VAPI_API_KEY=your_vapi_api_key
OPENAI_API_KEY=your_openai_api_key

# OAuth2
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# JWT
SECRET_KEY=your-secret-key-here
```

### Database Schema

The application uses the following main models:

- **User**: User authentication and profile information
- **Interview**: Interview sessions with questions, feedback, and status

## 📚 API Endpoints

### Authentication
- `POST /api/auth/google` - Google OAuth authentication
- `POST /api/auth/github` - GitHub OAuth authentication
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout user

### Interviews
- `GET /api/interviews/my` - Get user's interviews
- `GET /api/interviews/{id}` - Get specific interview
- `POST /api/interviews/` - Create new interview
- `PUT /api/interviews/{id}` - Update interview
- `DELETE /api/interviews/{id}` - Delete interview

### AI Features
- `POST /api/ai/questions` - Generate interview questions
- `POST /api/ai/questions/custom` - Generate custom questions
- `POST /api/ai/feedback` - Generate interview feedback
- `GET /api/ai/feedback/{id}` - Get interview feedback
- `POST /api/ai/feedback/analyze` - Analyze interview performance

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **OAuth2 Integration**: Google and GitHub OAuth support
- **CORS Configuration**: Secure cross-origin requests
- **Password Hashing**: Bcrypt password hashing
- **Input Validation**: Pydantic model validation

## 🧪 Testing

### Manual Testing

Use the FastAPI automatic documentation:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

### API Testing with curl

```bash
# Health check
curl http://localhost:8080/health

# Get user interviews (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8080/api/interviews/my
```

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use secure environment variable management
2. **Database**: Use production PostgreSQL instance
3. **HTTPS**: Enable SSL/TLS in production
4. **CORS**: Configure allowed origins for production domains
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Logging**: Configure proper logging for production

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python", "main.py"]
```

## 🔄 Migration from Java Backend

This Python backend is designed to be a drop-in replacement for the Java Spring Boot backend:

- **Same API endpoints**: Compatible with existing frontend
- **Same data models**: Compatible database schema
- **Same authentication**: OAuth2 and JWT support
- **Same AI integration**: OpenAI and Vapi AI support

## 📝 Development

### Project Structure

```
python-backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration settings
├── database.py            # Database connection and session
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── auth.py                # Authentication utilities
├── routers/               # API route handlers
│   ├── __init__.py
│   ├── auth.py           # Authentication routes
│   ├── interviews.py     # Interview management routes
│   ├── ai_questions.py   # AI question generation
│   └── ai_feedback.py    # AI feedback generation
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
└── README.md            # This file
```

### Adding New Features

1. Create new router files in `routers/` directory
2. Add corresponding schemas in `schemas.py`
3. Update models in `models.py` if needed
4. Include new routers in `main.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the Voicruit platform. See the main project for license information.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs for error messages
3. Ensure all environment variables are set correctly
4. Verify database connectivity

## 🔗 Related

- [Voicruit Frontend](../userpanel/) - React frontend application
- [Voicruit Java Backend](../backend/) - Original Java Spring Boot backend
