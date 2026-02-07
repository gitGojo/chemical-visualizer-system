@echo off
echo Starting Build Process...

REM Setup the working directory to the script location
cd /d "%~dp0"

REM Check if PyInstaller is installed using python -m
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Failed to install PyInstaller. Exiting.
        pause
        exit /b
    )
)

echo Cleaning up previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q *.spec 2>nul
del /q *.spec 2>nul

echo Building Executable...
REM Using python -m PyInstaller to ensure we use the module installed in the current python environment
python -m PyInstaller --onefile --noconsole --name "ChemicalVisualizer" desktop-frontend/main.py

if %errorlevel% equ 0 (
    echo.
    echo Build Successful!
    echo The executable is located at: %~dp0dist\ChemicalVisualizer.exe
    echo.
    echo You can move this file anywhere on your computer.
) else (
    echo.
    echo Build Failed.
)

pause
