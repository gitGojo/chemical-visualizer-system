# Chemical Equipment Parameter Visualizer - Web Frontend

React + Vite frontend for visualizing chemical equipment data.

## Setup

1.  **Install Dependencies**:
    ```bash
    cd web-frontend
    npm install
    ```

2.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    Access at `http://localhost:5173`.

## Features
- **Authentication**: Basic Login.
- **Upload**: Upload CSV files to the backend.
- **Dashboard**: View summary statistics and charts (Bar, Pie).
- **History**: View history of last 5 uploads.
- **Report**: Download PDF summary.

## Configuration
- API URL is set to `http://localhost:8000/api/` in `src/api.js`.
