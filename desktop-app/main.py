"""
PyQt5 Desktop Application for Chemical Equipment Data Visualization
Interfaces with backend API at http://127.0.0.1:8000
"""

import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QFileDialog, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChemicalVisualizerApp(QMainWindow):
    """Main application window for the Chemical Equipment Visualizer"""
    
    def __init__(self):
        super().__init__()
        self.backend_url = "http://127.0.0.1:8000"
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 900, 700)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("Chemical Equipment Data Analyzer")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.setStyleSheet("padding: 10px; font-size: 14px;")
        self.upload_btn.clicked.connect(self.upload_csv)
        button_layout.addWidget(self.upload_btn)
        
        self.summary_btn = QPushButton("Get Summary")
        self.summary_btn.setStyleSheet("padding: 10px; font-size: 14px;")
        self.summary_btn.clicked.connect(self.get_summary)
        button_layout.addWidget(self.summary_btn)
        
        main_layout.addLayout(button_layout)
        
        # Summary display area
        summary_label = QLabel("Summary Statistics:")
        summary_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(summary_label)
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMaximumHeight(150)
        self.summary_text.setStyleSheet("font-size: 12px; padding: 5px;")
        main_layout.addWidget(self.summary_text)
        
        # Chart area
        chart_label = QLabel("Equipment Type Distribution:")
        chart_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(chart_label)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)
        
        # Initial message
        self.summary_text.setText("Click 'Upload CSV' to upload a data file, then 'Get Summary' to view statistics.")
    
    def upload_csv(self):
        """Handle CSV file upload"""
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            # Prepare file for upload
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(
                    f"{self.backend_url}/api/upload/",
                    files=files,
                    timeout=10
                )
            
            if response.status_code == 200:
                QMessageBox.information(
                    self,
                    "Success",
                    "CSV file uploaded successfully!"
                )
                self.summary_text.setText("File uploaded successfully. Click 'Get Summary' to view statistics.")
            else:
                QMessageBox.warning(
                    self,
                    "Upload Failed",
                    f"Failed to upload file. Status code: {response.status_code}\n{response.text}"
                )
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self,
                "Connection Error",
                "Could not connect to backend server at http://127.0.0.1:8000\n"
                "Please ensure the backend server is running."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred: {str(e)}"
            )
    
    def get_summary(self):
        """Retrieve and display summary statistics"""
        try:
            response = requests.get(
                f"{self.backend_url}/api/summary/",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Display summary statistics
                summary_text = f"""
Total Equipment Count: {data.get('total_count', 'N/A')}
Average Flowrate: {data.get('avg_flowrate', 'N/A'):.2f}
Average Pressure: {data.get('avg_pressure', 'N/A'):.2f}
Average Temperature: {data.get('avg_temperature', 'N/A'):.2f}
                """.strip()
                
                self.summary_text.setText(summary_text)
                
                # Generate chart
                self.generate_chart(data)
                
            else:
                QMessageBox.warning(
                    self,
                    "Request Failed",
                    f"Failed to retrieve summary. Status code: {response.status_code}\n{response.text}"
                )
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self,
                "Connection Error",
                "Could not connect to backend server at http://127.0.0.1:8000\n"
                "Please ensure the backend server is running."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred: {str(e)}"
            )
    
    def generate_chart(self, data):
        """Generate equipment type distribution chart"""
        # Clear previous chart
        self.figure.clear()
        
        # Get equipment type distribution
        equipment_types = data.get('equipment_type_distribution', {})
        
        if not equipment_types:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   horizontalalignment='center',
                   verticalalignment='center',
                   transform=ax.transAxes)
            self.canvas.draw()
            return
        
        # Create bar chart
        ax = self.figure.add_subplot(111)
        
        types = list(equipment_types.keys())
        counts = list(equipment_types.values())
        
        bars = ax.bar(types, counts, color='steelblue', alpha=0.7)
        
        ax.set_xlabel('Equipment Type', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10)
        
        self.figure.tight_layout()
        self.canvas.draw()


def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = ChemicalVisualizerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
