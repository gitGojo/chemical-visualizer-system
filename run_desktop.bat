@echo off
echo Starting Desktop Frontend...
cd /d "%~dp0"

if exist "desktop-frontend" (
    cd desktop-frontend
) else (
    echo ERROR: 'desktop-frontend' directory not found.
    pause
    exit /b
)

echo Installing dependencies...
python -m pip install -r requirements.txt

echo Starting Application...
python main.py
pause
