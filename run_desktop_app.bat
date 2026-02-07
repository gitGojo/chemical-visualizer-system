@echo off
echo Starting Chemical Equipment Visualizer - Desktop Application
echo.
echo Checking if dependencies are installed...
python -c "import PyQt5, requests, matplotlib" 2>nul
if errorlevel 1 (
    echo Dependencies not found. Installing...
    pip install -r desktop-app\requirements.txt
    echo.
)

echo Starting desktop application...
python desktop-app\main.py
