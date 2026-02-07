# Chemical Equipment Parameter Visualizer - Desktop Frontend

PyQt5 desktop application for analyzing equipment data.

## Setup

1.  **Install Dependencies**:
    ```bash
    cd desktop-frontend
    pip install -r requirements.txt
    ```

2.  **Run Application**:
    ```bash
    python main.py
    ```

## Requirements
- Python 3.8+
- Running Backend server at `http://localhost:8000/`

## Features
- **Login**: Secure access via Basic Auth.
- **Charts**: Matplotlib integration for data visualization.
- **Upload**: Desktop-native file dialog for CSV upload.
- **History**: Tabular view of past uploads.
