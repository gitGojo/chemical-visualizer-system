# Chemical Equipment Parameter Visualizer - Backend

This is the backend for the Chemical Equipment Parameter Visualizer, built with Django and Django REST Framework.

## Requirements
- Python 3.8+

## Setup Instructions

To avoid environment confusion, always use `python -m` to ensure you are using the same Python interpreter for installation and running the server.

1.  **Install Dependencies**:
    Run this command in the `backend` directory:
    ```bash
    cd backend
    python -m pip install -r requirements.txt
    ```

2.  **Database Migration**:
    Initialize the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3.  **Create Admin User**:
    (Optional) Create a user for the API:
    ```bash
    python manage.py createsuperuser
    ```

4.  **Run Server**:
    Start the development server:
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://localhost:8000/`.

**Troubleshooting**:
If you still see "Couldn't import Django", ensure you are running `python manage.py runserver` from the same terminal window where you ran `python -m pip install ...`.
