# Chemical Equipment Visualizer - Desktop Application

A standalone PyQt5 desktop application for uploading CSV files and visualizing chemical equipment data.

## Prerequisites

- Python 3.7 or higher
- Backend server running at `http://127.0.0.1:8000`

## Installation

1. Navigate to the desktop-app directory:
```bash
cd desktop-app
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. **Ensure the backend server is running** at `http://127.0.0.1:8000`

2. Run the desktop application:
```bash
python main.py
```

## Usage

### Upload CSV File
1. Click the **"Upload CSV"** button
2. Select a CSV file from your file system
3. The file will be uploaded to the backend API
4. A success message will appear if the upload is successful

### View Summary Statistics
1. After uploading a CSV file, click the **"Get Summary"** button
2. The application will display:
   - Total equipment count
   - Average flowrate
   - Average pressure
   - Average temperature
3. A bar chart showing equipment type distribution will be generated

## Features

- **CSV Upload**: Upload CSV files containing chemical equipment data
- **Summary Statistics**: View key metrics from the uploaded data
- **Data Visualization**: Bar chart showing equipment type distribution
- **Error Handling**: Clear error messages for connection issues or failed requests

## Troubleshooting

### "Connection Error" message
- Ensure the backend server is running at `http://127.0.0.1:8000`
- Check that the backend API endpoints are accessible:
  - POST `/api/upload/`
  - GET `/api/summary/`

### "Upload Failed" message
- Verify the CSV file format is correct
- Check backend server logs for detailed error information

## Technical Details

- **Framework**: PyQt5
- **HTTP Client**: requests
- **Visualization**: matplotlib
- **Backend API**: Django REST API at `http://127.0.0.1:8000`
