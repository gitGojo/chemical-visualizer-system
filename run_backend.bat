@echo off
echo Starting Chemical Visualizer Backend...

:: Change to the directory where this script is located
cd /d "%~dp0"

:: Now navigate to the backend folder
if exist "backend" (
    cd backend
) else (
    echo ERROR: 'backend' directory not found in "%~dp0"
    pause
    exit /b
)

:: Check if requirements.txt exists
if not exist requirements.txt (
    echo ERROR: requirements.txt not found in %CD%
    pause
    exit /b
)

echo Installing dependencies...
python -m pip install -r requirements.txt

echo Applying migrations...
python manage.py makemigrations
python manage.py migrate

echo Creating superuser (you can skip if already exists)...
python manage.py createsuperuser --noinput --username admin --email admin@example.com 2>NUL
if %errorlevel% equ 0 (
    echo Admin user created with username 'admin'.
    echo IMPORTANT: You need to set a password manually later if needed, or use the default setup.
    echo Default password is NOT set.
    python manage.py shell -c "from django.contrib.auth.models import User; u=User.objects.get(username='admin'); u.set_password('admin123'); u.save()"
    echo Admin password set to 'admin123'.
) else (
    echo Admin user 'admin' already exists.
)

echo Starting Server...
python manage.py runserver
pause
