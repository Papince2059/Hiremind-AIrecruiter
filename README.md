# Hiremind – AI Voice Recruiter

Hiremind is an AI-powered voice-based interview platform that streamlines the hiring process by conducting automated voice interviews tailored to different interview types. Built using React frontend and Python FastAPI backend with Vapi AI integration.

## 🚀 Features

- 🎙️ AI-driven voice interviews (Technical, Behavioral, Experience-based)
- 🧠 Custom interview generation with OpenAI
- 📞 Web interview calls via Vapi AI integration
- 👤 Candidate management and interview flow
- ✅ Interview completion and AI feedback generation
- 🔐 OAuth2 authentication (Google, GitHub)
- 🗄️ PostgreSQL database

## 🏗️ System Architecture

### High-Level System Flow

```mermaid
graph TB
    subgraph "Frontend (React + Vite)"
        A[User Dashboard] --> B[Create Interview]
        B --> C[Interview Form]
        C --> D[AI Question Generation]
        D --> E[Interview Preview]
        E --> F[Interview Link Generation]
        F --> G[Share with Candidate]
    end
    
    subgraph "Backend (FastAPI + Python)"
        H[Authentication Service]
        I[Interview Management]
        J[AI Question Service]
        K[AI Feedback Service]
        L[Database Service]
    end
    
    subgraph "External Services"
        M[OpenAI API]
        N[Vapi AI]
        O[Google OAuth]
        P[GitHub OAuth]
    end
    
    subgraph "Database"
        Q[(PostgreSQL)]
    end
    
    A --> H
    B --> I
    D --> J
    J --> M
    I --> L
    L --> Q
    H --> O
    H --> P
    G --> N
```

### Detailed Component Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant AI as OpenAI
    participant V as Vapi AI
    participant DB as Database
    
    Note over U,DB: Interview Creation Flow
    
    U->>F: Access Dashboard
    F->>B: GET /api/auth/me
    B->>DB: Verify User
    DB-->>B: User Data
    B-->>F: User Info
    
    U->>F: Create New Interview
    F->>F: Fill Interview Form
    F->>B: POST /api/interviews/
    B->>B: Validate Data
    B->>AI: Generate Questions
    AI-->>B: Questions Array
    B->>DB: Save Interview
    DB-->>B: Interview ID
    B-->>F: Interview Created
    
    Note over U,DB: Interview Execution Flow
    
    U->>F: Access Interview Link
    F->>B: GET /api/interviews/{id}
    B->>DB: Fetch Interview
    DB-->>B: Interview Data
    B-->>F: Interview Details
    
    F->>V: Initialize Voice Call
    V-->>F: Call Session
    F->>V: Start Interview
    V->>V: Conduct AI Interview
    V-->>F: Interview Complete
    
    Note over U,DB: Feedback Generation Flow
    
    F->>B: POST /api/ai/feedback
    B->>AI: Analyze Interview
    AI-->>B: Feedback Analysis
    B->>DB: Save Feedback
    DB-->>B: Feedback Saved
    B-->>F: Feedback Available
```

## 🛠️ Tech Stack

| Frontend           | Backend               | AI/Voice APIs       | Database  |
|--------------------|------------------------|----------------------|-----------|
| React 19 + Vite    | Python FastAPI        | Vapi AI, OpenAI      | PostgreSQL|
| Tailwind CSS       | SQLAlchemy + JWT      |                      |           |

## 🚀 Quick Start

### Prerequisites

Before running the application, ensure you have:

- **Node.js** (v16 or higher)
- **Python** (3.8 or higher)
- **PostgreSQL** database
- **OpenAI API Key**
- **Vapi AI API Key** (for voice interviews)
- **Google OAuth Credentials** (optional)
- **GitHub OAuth Credentials** (optional)

### Option 1: Automated Setup (Windows)
```bash
# Run the provided batch file
start_services.bat
```

### Option 2: Manual Setup

#### Backend Setup
```bash
# Navigate to backend directory
cd python-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your actual values

# Run database migrations (if needed)
python migrate_database.py

# Start the backend server
python main.py
```

#### Frontend Setup
```bash
# Navigate to frontend directory (new terminal)
cd userpanel

# Install dependencies
npm install

# Start the development server
npm run dev
```

### Option 3: Using Batch Files (Windows)
```bash
# Start both services
start_services.bat

# Or start individually
start_backend.bat
start_frontend.bat
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `python-backend` directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/recruiter_db

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
VAPI_API_KEY=your_vapi_api_key_here

# OAuth2 Configuration (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Setup

1. **Install PostgreSQL** on your system
2. **Create a database**:
   ```sql
   CREATE DATABASE recruiter_db;
   ```
3. **Update the DATABASE_URL** in your `.env` file
4. **Run migrations** (if needed):
   ```bash
   cd python-backend
   python migrate_database.py
   ```

## 📱 Application Flow

### 1. User Authentication
- Users can sign in with Google or GitHub OAuth
- JWT tokens are used for session management
- Authentication state is maintained in localStorage

### 2. Interview Creation
- **Step 1**: Fill out interview form (job title, description, duration, type)
- **Step 2**: AI generates relevant questions based on job requirements
- **Step 3**: Preview and customize questions
- **Step 4**: Generate shareable interview link

### 3. Interview Execution
- Candidates access the interview via the generated link
- Voice interview is conducted using Vapi AI
- Real-time audio processing and response analysis
- Interview session is recorded for feedback generation

### 4. Feedback Generation
- AI analyzes the interview transcript
- Generates comprehensive feedback report
- Provides scoring and recommendations
- Feedback is stored and accessible to recruiters

## 🏗️ Project Structure

```
Hiremind/
├── userpanel/                 # React Frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/            # Application pages
│   │   ├── utils/            # Utility functions
│   │   └── assets/           # Static assets
│   ├── package.json          # Frontend dependencies
│   └── vite.config.js        # Vite configuration
├── python-backend/           # FastAPI Backend
│   ├── routers/              # API route handlers
│   ├── models.py             # Database models
│   ├── schemas.py            # Pydantic schemas
│   ├── auth.py               # Authentication logic
│   ├── main.py               # Application entry point
│   └── requirements.txt      # Python dependencies
├── start_services.bat        # Windows batch file to start both services
├── start_backend.bat         # Backend startup script
├── start_frontend.bat        # Frontend startup script
└── README.md                 # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/google` - Google OAuth authentication
- `POST /api/auth/github` - GitHub OAuth authentication
- `GET /api/auth/me` - Get current user information
- `POST /api/auth/logout` - Logout user

### Interview Management
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

## 🛠️ Development

### Frontend Development
```bash
cd userpanel
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### Backend Development
```bash
cd python-backend
python main.py       # Start development server
python -m pytest    # Run tests
python migrate_database.py  # Run database migrations
```

### Code Quality
- **Frontend**: ESLint for JavaScript/React linting
- **Backend**: Black for Python formatting, Flake8 for linting
- **Database**: SQLAlchemy ORM with PostgreSQL

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
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "main.py"]
```

## 🧪 Testing

### Manual Testing
- **Frontend**: Access http://localhost:5173
- **Backend API**: Access http://localhost:8080/docs (Swagger UI)
- **Database**: Verify PostgreSQL connection

### API Testing
```bash
# Health check
curl http://localhost:8080/health

# Get user interviews (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8080/api/interviews/my
```

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Ensure database exists

2. **Authentication Issues**
   - Verify OAuth credentials in .env
   - Check JWT secret key
   - Clear browser localStorage

3. **AI Integration Issues**
   - Verify OpenAI API key
   - Check Vapi AI API key
   - Ensure API quotas are not exceeded

4. **CORS Issues**
   - Check allowed origins in backend
   - Verify frontend URL matches backend configuration

## 📚 Documentation

- **[Connection Setup Guide](CONNECTION_SETUP_GUIDE.md)** - Complete setup instructions
- **[Backend Setup](python-backend/SETUP_GUIDE.md)** - Detailed backend configuration
- **[Backend README](python-backend/README.md)** - Backend-specific documentation

## 🔗 URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs

## 📸 Screenshots

<img width="1896" height="870" alt="Dashboard" src="https://github.com/user-attachments/assets/5b4b01f6-210b-4d36-8a97-dcdc0c39a538" />
<img width="1899" height="823" alt="Create Interview" src="https://github.com/user-attachments/assets/77769e12-4be5-45f8-ae67-c4247a15e62b" />
<img width="1912" height="871" alt="Interview Room" src="https://github.com/user-attachments/assets/6c3fd27b-7530-4566-9c14-378d2fee61ef" />

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

[Papince Kumar Gupta](https://github.com/Papince2059)

## 🙏 Acknowledgments

- **OpenAI** for AI question generation and feedback analysis
- **Vapi AI** for voice interview capabilities
- **FastAPI** for the robust backend framework
- **React** for the modern frontend framework







