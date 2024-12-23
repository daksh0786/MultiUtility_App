import sys
import pymysql
from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QFileDialog, QMenu, QAction, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QApplication,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SQLServer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Config
        self.setWindowTitle("SQL Query Application")
        self.setGeometry(100, 100, 800, 600)  # Fixed size for the application
        self.setStyleSheet("background-color: #F5F5F5;")  # Light pastel background color

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout(self.central_widget)

        # Input Field for SQL Query
        self.query_input = QTextEdit(self)
        self.query_input.setPlaceholderText("Enter your SQL query here...")
        self.query_input.setStyleSheet("""
            QTextEdit {
                background-color: #FFF9C4;
                font-size: 18px;
                border: 2px solid #D3D3D3;
                border-radius: 10px;
                padding: 10px;
            }
            QTextEdit:focus {
                border-color: #FFB74D;  /* Highlight color on focus */
            }
        """)
        self.layout.addWidget(self.query_input)

        # Execute Button
        self.execute_button = QPushButton("Execute Query", self)
        self.execute_button.setStyleSheet("""
            QPushButton {
                background-color: #FFB74D;
                font-size: 18px;
                color: white;
                padding: 15px;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF9800;
            }
        """)
        self.execute_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.execute_button)

        # Table Widget for Displaying Results
        self.result_table = QTableWidget(self)
        self.result_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #D3D3D3;
                border-radius: 10px;
                background-color: #FFFFFF;
                padding: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #FFB74D;
                color: white;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.result_table)

        # Connection Config
        self.connection = None
        self.connect_to_database()

    def connect_to_database(self):
        """Establish a connection to the Railway database."""
        try:
            self.connection = pymysql.connect(
                host="sql12.freesqldatabase.com",   # Host from Railway
                user="",                       # Username from Railway
                password="",  # Password from Railway
                database="sql12749421",                # Database name from Railway
                port=3306                         # Port from Railway
            )
            print("Connection successful!")
        except Exception as e:
            self.query_input.setPlainText(f"Error connecting to database: {str(e)}")
            print(f"Error: {str(e)}")

    def execute_query(self):
        """Execute the SQL query entered by the user."""
        query = self.query_input.toPlainText()
        if not self.connection:
            self.query_input.setPlainText("Not connected to the database.")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                if query.strip().upper().startswith("SELECT"):
                    results = cursor.fetchall()
                    headers = [desc[0] for desc in cursor.description]
                    self.populate_table(results, headers)
                else:
                    self.connection.commit()
                    self.query_input.setPlainText("Query executed successfully.")
        except Exception as e:
            self.query_input.setPlainText(f"Error executing query: {str(e)}")

    def populate_table(self, data, headers):
        """Display query results in the table widget."""
        self.result_table.clear()
        self.result_table.setRowCount(len(data))
        self.result_table.setColumnCount(len(headers))
        self.result_table.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
