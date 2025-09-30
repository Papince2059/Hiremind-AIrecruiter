@echo off
echo Starting AI Recruiter Services...

echo.
echo Starting Python Backend...
cd python-backend
start "Backend Server" cmd /k "python main.py"

echo.
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting Frontend...
cd ..\userpanel
start "Frontend Server" cmd /k "npm run dev"

echo.
echo Both services are starting...
echo Backend: http://localhost:8080
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit...
pause > nul
