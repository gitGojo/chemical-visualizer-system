Chemical Equipment Data Visualizer
A full-stack application for visualizing chemical equipment data using a Django REST backend, React web frontend, and a PyQt5 desktop application.

Project Structure

chemical_visualizer/
??? backend/                  # Django backend (REST API)
??? web-frontend/             # React web application
??? desktop-frontend/         # PyQt5 desktop application source
??? build/                    # PyInstaller build files (auto-generated)
??? dist/                     # Generated desktop executable (.exe)
??? ChemicalVisualizer.spec   # PyInstaller spec file
??? build_exe.bat             # Script to build desktop EXE
??? run_all.bat               # Run backend + web frontend
??? run_backend.bat           # Run backend only
??? run_web.bat               # Run web frontend only
??? run_desktop.bat           # Run desktop application
??? run_desktop_app.bat       # Alternate desktop runner
??? sample_data.csv           # Sample CSV input
??? sample_equipment_data.csv # Sample equipment CSV
??? verify_backend_health.py  # Backend health check
??? README.md                 # Project documentation

?? Prerequisites
Make sure you have the following installed:
* Python 3.10+
* Node.js 18+
* npm
* Git
* Windows OS (for .exe)

?? How to Run the Project
?? Option 1: Run Everything Automatically
run_all.bat
This will:
* Start the backend
* Start the web frontend

?? Option 2: Run Components Manually
1?? Start Backend (Required)
run_backend.bat
Wait until you see:
Starting development server at http://127.0.0.1:8000/

2?? Start Web Frontend
run_web.bat
Open in browser:
http://localhost:5173

3?? Start Desktop Application
run_desktop.bat
?? Important:
The backend must be running before launching the desktop app.

??? Desktop Executable (.exe)
A standalone Windows executable is available.
?? Location:
dist/ChemicalVisualizer.exe
To use:
1. Start backend using run_backend.bat
2. Double-click ChemicalVisualizer.exe

?? Application Features
Web Application
* CSV upload
* Equipment statistics
* Bar charts & pie charts
* Upload history table
* PDF report download
Desktop Application
* Login screen
* CSV upload
* Summary statistics
* Equipment distribution chart
* Native Windows UI

?? Sample Data
You can test the application using:
* sample_data.csv
* sample_equipment_data.csv

?? Demo Video
Click here to watch the demo video



