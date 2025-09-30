@echo off
echo 🚀 Starting Hiremind Frontend...
echo.

REM Check if node_modules exists
if not exist "userpanel\node_modules" (
    echo ❌ Node.js dependencies not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Start the frontend server
echo 🔄 Starting Vite development server...
cd userpanel
npm run dev

pause

