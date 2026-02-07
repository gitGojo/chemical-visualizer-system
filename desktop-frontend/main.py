import sys
import requests
import base64
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_URL = "http://localhost:8000/api/"

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Chemical Visualizer")
        self.setFixedSize(450, 350)
        self.setStyleSheet("background-color: #0b0b0b; color: #e0e0e0;")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(18)
        layout.setContentsMargins(32, 28, 32, 28)
        
        title = QLabel("Chemical Visualizer")
        title.setStyleSheet("color: #e0e0e0;")
        font = title.font()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        layout.addSpacing(15)
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("""
            background-color: #1a1a1a; 
            color: #e0e0e0; 
            border: 1px solid #333;
            border-radius: 4px;
            padding: 8px;
            font-size: 13px;
        """)
        self.username.setFixedHeight(42)
        layout.addWidget(self.username)
        
        layout.addSpacing(12)
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("""
            background-color: #1a1a1a; 
            color: #e0e0e0; 
            border: 1px solid #333;
            border-radius: 4px;
            padding: 8px;
            font-size: 13px;
        """)
        self.password.setFixedHeight(42)
        layout.addWidget(self.password)
        
        layout.addSpacing(12)
        
        self.btn_login = QPushButton("Login")
        self.btn_login.setStyleSheet("""
            background-color: #1a1a1a; 
            color: #e0e0e0; 
            border: 1px solid #333;
            border-radius: 4px;
            padding: 10px;
            font-size: 13px;
            font-weight: bold;
            margin-top: 10px;
        """)
        self.btn_login.setFixedHeight(42)
        self.btn_login.clicked.connect(self.attempt_login)
        layout.addWidget(self.btn_login)
        
        self.setLayout(layout)


    def attempt_login(self):
        username = self.username.text()
        password = self.password.text()
        auth = requests.auth.HTTPBasicAuth(username, password)
        try:
            r = requests.get(API_URL + "summary/", auth=auth)
            if r.status_code in [200, 404]:
                self.open_dashboard(username, password)
            elif r.status_code in [401, 403]:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials")
            else:
                self.open_dashboard(username, password)
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Could not connect: {e}")

    def open_dashboard(self, username, password):
        self.dashboard = DashboardWindow(username, password)
        self.dashboard.show()
        self.close()

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor="#0b0b0b")
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor("#0b0b0b")
        self.axes.tick_params(colors="white", which="both")
        for spine in self.axes.spines.values():
            spine.set_color("white")
        self.axes.xaxis.label.set_color("white")
        self.axes.yaxis.label.set_color("white")
        
        super(MplCanvas, self).__init__(fig)
        self.setStyleSheet("background-color: #0b0b0b;")
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

class Card(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("background-color: #1a1a1a; border: 1px solid #333;")

class DashboardWindow(QMainWindow):
    def __init__(self, username, password):
        super().__init__()
        self.auth = requests.auth.HTTPBasicAuth(username, password)
        self.setWindowTitle("Chemical Equipment Dashboard")
        self.resize(1000, 800)
        self.setStyleSheet("background-color: #0b0b0b; color: #e0e0e0;")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: #0b0b0b; border: none;")
        self.setCentralWidget(scroll)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #0b0b0b;")
        scroll.setWidget(content_widget)
        
        self.main_layout = QVBoxLayout(content_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.setup_header()
        self.setup_upload_section()
        self.setup_metrics_section()
        self.setup_charts_section()
        self.setup_history_section()
        
        self.main_layout.addStretch()

    def setup_header(self):
        header = QHBoxLayout()
        
        title = QLabel("Chemical Visualizer Dashboard")
        title.setStyleSheet("color: #e0e0e0;")
        font = title.font()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        
        self.btn_download = QPushButton("Download PDF Report")
        self.btn_download.setStyleSheet("background-color: #1a1a1a; color: #e0e0e0; border: 1px solid #333;")
        self.btn_download.setFixedSize(160, 30)
        self.btn_download.clicked.connect(self.download_pdf)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.btn_download)
        self.main_layout.addLayout(header)

    def setup_upload_section(self):
        group_box = Card()
        layout = QVBoxLayout(group_box)
        layout.setContentsMargins(10, 10, 10, 10)
        
        lbl_title = QLabel("Upload Dataset")
        lbl_title.setStyleSheet("color: #e0e0e0;")
        font = lbl_title.font()
        font.setBold(True)
        lbl_title.setFont(font)
        layout.addWidget(lbl_title)
        
        row = QHBoxLayout()
        
        self.lbl_file = QLabel("No file selected")
        self.lbl_file.setStyleSheet("background-color: #0b0b0b; color: #e0e0e0; border: 1px solid #333;")
        self.lbl_file.setFrameShape(QFrame.StyledPanel)
        self.lbl_file.setFixedSize(300, 30)
        
        self.btn_browse = QPushButton("Choose File")
        self.btn_browse.setStyleSheet("background-color: #1a1a1a; color: #e0e0e0; border: 1px solid #333;")
        self.btn_browse.clicked.connect(self.browse_file)
        
        self.btn_upload = QPushButton("Upload CSV")
        self.btn_upload.setStyleSheet("background-color: #1a1a1a; color: #e0e0e0; border: 1px solid #333;")
        self.btn_upload.clicked.connect(self.upload_csv)
        
        self.lbl_upload_status = QLabel("")
        self.lbl_upload_status.setStyleSheet("color: #e0e0e0;")
        
        row.addWidget(self.btn_browse)
        row.addWidget(self.lbl_file)
        row.addWidget(self.btn_upload)
        row.addWidget(self.lbl_upload_status)
        row.addStretch()
        
        layout.addLayout(row)
        self.main_layout.addWidget(group_box)

    def setup_metrics_section(self):
        self.metrics_card = Card()
        layout = QHBoxLayout(self.metrics_card)
        layout.setContentsMargins(10, 20, 10, 20)
        
        self.lbl_metric_total = QLabel("Total Equipment: -")
        self.lbl_metric_flow = QLabel("Avg Flow: -")
        self.lbl_metric_press = QLabel("Avg Pressure: -")
        self.lbl_metric_temp = QLabel("Avg Temp: -")
        
        for lbl in [self.lbl_metric_total, self.lbl_metric_flow, self.lbl_metric_press, self.lbl_metric_temp]:
            lbl.setStyleSheet("color: #e0e0e0;")
            font = lbl.font()
            font.setPointSize(10)
            font.setBold(True)
            lbl.setFont(font)
            lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(lbl)
            
        self.metrics_card.hide()
        self.main_layout.addWidget(self.metrics_card)

        self.lbl_placeholder = QLabel("Please upload a CSV file to view analytics.")
        self.lbl_placeholder.setStyleSheet("color: #888;")
        self.lbl_placeholder.setAlignment(Qt.AlignCenter)
        font = self.lbl_placeholder.font()
        font.setPointSize(12)
        font.setItalic(True)
        self.lbl_placeholder.setFont(font)
        self.main_layout.addWidget(self.lbl_placeholder)

    def setup_charts_section(self):
        self.charts_container = QWidget()
        self.charts_container.setStyleSheet("background-color: #0b0b0b;")
        layout = QHBoxLayout(self.charts_container)
        layout.setSpacing(10)
        
        bar_card = Card()
        bar_layout = QVBoxLayout(bar_card)
        self.canvas_bar = MplCanvas(self)
        bar_layout.addWidget(self.canvas_bar)
        
        pie_card = Card()
        pie_layout = QVBoxLayout(pie_card)
        self.canvas_pie = MplCanvas(self)
        pie_layout.addWidget(self.canvas_pie)
        
        layout.addWidget(bar_card)
        layout.addWidget(pie_card)
        
        self.charts_container.hide()
        self.main_layout.addWidget(self.charts_container)

    def setup_history_section(self):
        self.history_card = Card()
        layout = QVBoxLayout(self.history_card)
        layout.setContentsMargins(10, 10, 10, 10)
        
        lbl_title = QLabel("Upload History (Last 5)")
        lbl_title.setStyleSheet("color: #e0e0e0;")
        font = lbl_title.font()
        font.setBold(True)
        lbl_title.setFont(font)
        layout.addWidget(lbl_title)
        
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0b0b0b; 
                color: #e0e0e0; 
                gridline-color: #333;
            }
            QHeaderView::section {
                background-color: #ffffff;
                color: #000000;
                font-weight: bold;
                padding: 6px;
                border: none;
                border-bottom: 1px solid #cccccc;
                border-right: 1px solid #e0e0e0;
            }
        """)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Uploaded At", "Total Equipment"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(200)
        
        layout.addWidget(self.table)
        self.main_layout.addWidget(self.history_card)

    def browse_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '.', "CSV Files (*.csv)")
        if fname:
            self.selected_file = fname
            self.lbl_file.setText(fname.split('/')[-1])
        else:
            self.selected_file = None
            self.lbl_file.setText("No file selected")

    def upload_csv(self):
        if not hasattr(self, 'selected_file') or not self.selected_file:
            QMessageBox.warning(self, "Warning", "Please select a file first.")
            return
            
        try:
            files = {'file': open(self.selected_file, 'rb')}
            self.lbl_upload_status.setText("Uploading...")
            
            r = requests.post(API_URL + "upload/", files=files, auth=self.auth)
            
            if r.status_code == 201:
                self.lbl_upload_status.setText("Upload successful!")
                self.load_data()
            else:
                self.lbl_upload_status.setText("Upload Failed")
                QMessageBox.warning(self, "Error", f"Upload Failed: {r.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.lbl_upload_status.setText("Error")

    def load_data(self):
        try:
            r_sum = requests.get(API_URL + "summary/", auth=self.auth)
            if r_sum.status_code == 200:
                data = r_sum.json()
                if 'total_equipment' in data:
                    self.update_summary_ui(data)
            
            r_hist = requests.get(API_URL + "history/", auth=self.auth)
            if r_hist.status_code == 200:
                self.update_history_table(r_hist.json())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")

    def update_summary_ui(self, data):
        self.lbl_placeholder.hide()
        self.metrics_card.show()
        self.charts_container.show()
        
        self.lbl_metric_total.setText(f"Total Equipment: {data['total_equipment']}")
        self.lbl_metric_flow.setText(f"Avg Flow: {data['avg_flowrate']:.2f}")
        self.lbl_metric_press.setText(f"Avg Pressure: {data['avg_pressure']:.2f}")
        self.lbl_metric_temp.setText(f"Avg Temp: {data['avg_temperature']:.2f}")
        
        self.canvas_bar.axes.cla()
        self.canvas_bar.axes.set_facecolor("#0b0b0b")
        self.canvas_bar.axes.tick_params(colors="white", which="both")
        for spine in self.canvas_bar.axes.spines.values():
            spine.set_color("white")
        self.canvas_bar.axes.xaxis.label.set_color("white")
        self.canvas_bar.axes.yaxis.label.set_color("white")
        
        params = ['Flowrate', 'Pressure', 'Temp']
        values = [data['avg_flowrate'], data['avg_pressure'], data['avg_temperature']]
        self.canvas_bar.axes.bar(params, values, color='#4a9eff')
        self.canvas_bar.axes.grid(True, color='#333', linestyle='--', linewidth=0.5)
        self.canvas_bar.draw()
        
        self.canvas_pie.axes.cla()
        self.canvas_pie.axes.set_facecolor("#0b0b0b")
        labels = list(data['type_distribution'].keys())
        sizes = list(data['type_distribution'].values())
        colors = ['#4a9eff', '#ff6b6b', '#4ecdc4', '#ffe66d', '#a8dadc']
        wedges, texts, autotexts = self.canvas_pie.axes.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        for text in texts:
            text.set_color('white')
        for autotext in autotexts:
            autotext.set_color('white')
        self.canvas_pie.axes.axis('equal')
        self.canvas_pie.draw()

    def update_history_table(self, history):
        self.table.setRowCount(len(history))
        for i, row in enumerate(history):
            self.table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['uploaded_at'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(row['total_equipment'])))

    def download_pdf(self):
        try:
            fname, _ = QFileDialog.getSaveFileName(self, 'Save PDF Report', 'summary_report.pdf', "PDF Files (*.pdf)")
            if fname:
                r = requests.get(API_URL + "report_pdf/", auth=self.auth)
                if r.status_code == 200:
                    with open(fname, 'wb') as f:
                        f.write(r.content)
                    QMessageBox.information(self, "Success", "PDF Report saved successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to generate report.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
