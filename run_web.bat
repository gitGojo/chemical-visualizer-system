@echo off
echo Starting Web Frontend...
cd /d "%~dp0"

if exist "web-frontend" (
    cd web-frontend
) else (
    echo ERROR: 'web-frontend' directory not found.
    pause
    exit /b
)

if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

echo Starting Vite Server...
echo Access the app at http://localhost:5173
call npm run dev
pause
