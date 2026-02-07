@echo off
cd /d "%~dp0"
echo Starting Chemical Visualizer System...

echo 1. Launching Backend Server...
start "Visualizer Backend" run_backend.bat

echo Waiting 8 seconds for backend to initialize...
timeout /t 8 >nul

echo 2. Launching Web Frontend...
start "Visualizer Web" run_web.bat

echo 3. Launching Desktop Frontend...
start "Visualizer Desktop" run_desktop.bat

echo.
echo All components have been launched in separate windows.
echo - Backend: http://localhost:8000
echo - Web App: http://localhost:5173
echo.
pause
