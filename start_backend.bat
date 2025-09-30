@echo off
echo 🚀 Starting Hiremind Backend...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist "python-backend\.env" (
    echo ❌ Environment file not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Start the backend server
echo 🔄 Starting FastAPI server...
cd python-backend
python main.py

pause

