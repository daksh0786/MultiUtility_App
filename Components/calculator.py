
import sys
import math
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton


class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scientific Calculator")
        self.setGeometry(100, 100, 400, 480)  # Starting size

        # Set pastel color for the calculator window
        self.setStyleSheet("background-color: #C8E6C9;")  # Light pastel green

        # Main widget container
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout (vertical layout for input display and buttons)
        main_layout = QVBoxLayout(central_widget)

        # Create a QLineEdit widget for the display
        self.display = QLineEdit(self)
        self.display.setReadOnly(False)  # Make the input editable
        self.display.setStyleSheet("background-color: #FFFFFF; font-size: 18px; color: #000000;")  # White display
        self.display.setFont(QFont('Arial', 20))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMinimumHeight(60)  # Adjusted input box height

        # Add display to the main layout
        main_layout.addWidget(self.display)

        # Create a grid layout for buttons
        self.create_buttons(main_layout)

        # This will store the current operation
        self.current_operation = None

    # Function to create buttons in a grid layout
    def create_buttons(self, layout):
        button_labels = [
            '7', '8', '9', '/', 'sin', 'cos', 'tan', 'log',
            '4', '5', '6', '*', 'sqrt', '^', '(', ')',
            '1', '2', '3', '-', 'pi', 'exp', 'ln', '%',
            '0', 'C', '=', '+', 'e', 'mod', '.', '!'
        ]

        # Grid layout for buttons
        button_layout = QGridLayout()

        positions = [(i, j) for i in range(5) for j in range(8)]  # 5 rows, 8 columns
        for position, label in zip(positions, button_labels):
            button = QPushButton(label, self)  # Create a button
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FFCCBC;  /* Pastel orange background */
                    font-size: 18px; 
                    border: 2px solid #FF6F61;  /* Strong border */
                    border-radius: 8px;  /* Curved edges */
                    padding: 10px;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #FF8A65;  /* Darker orange when pressed */
                }
            """)
            button.setFont(QFont('Arial', 14))
            button.clicked.connect(self.on_button_click)  # Connect button click event
            button_layout.addWidget(button, *position)  # Add button to grid layout

        # Add the button grid layout to the main layout
        layout.addLayout(button_layout)

    # Button click event handler
    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        # Clear the display
        if text == 'C':
            self.display.clear()
            self.current_operation = None

        # Handle operations
        elif text == '=':
            try:
                result = self.evaluate_expression()
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText("Error")
        
        # Set the current operation (sin, cos, tan, etc.)
        elif text in ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'ln', 'pi', 'e', '%', '!', '^', 'mod']:
            self.current_operation = text
            current_text = self.display.text()
            if current_text == "":
                self.display.setText(text + "(")  # Append function with opening parenthesis
            else:
                self.display.setText(current_text + text + "(")  # Append function with opening parenthesis

        # Handle mathematical functions like sin, cos, etc.
        elif text in ['pi', 'e', '.', '%', '!', '^']:
            if text == 'pi':
                self.display.setText(self.display.text() + str(math.pi))
            elif text == 'e':
                self.display.setText(self.display.text() + str(math.e))
            elif text == '.':
                current_text = self.display.text()
                if '.' not in current_text:
                    self.display.setText(current_text + '.')
            elif text == '%':
                try:
                    current_text = float(self.display.text())
                    self.display.setText(str(current_text / 100))
                except ValueError:
                    self.display.setText("Error")
            elif text == '^':
                current_text = self.display.text()
                self.display.setText(current_text + '')
            elif text == '!':
                try:
                    current_text = int(self.display.text())
                    result = math.factorial(current_text)
                    self.display.setText(str(result))
                except ValueError:
                    self.display.setText("Error")

        # Standard numbers and operators
        else:
            current_text = self.display.text()
            self.display.setText(current_text + text)

    def evaluate_expression(self):
        """ Evaluate the mathematical expression from the display. """
        expression = self.display.text()

        # Replace parentheses for easier evaluation
        expression = expression.replace("sin", "math.sin")
        expression = expression.replace("cos", "math.cos")
        expression = expression.replace("tan", "math.tan")
        expression = expression.replace("log", "math.log10")
        expression = expression.replace("sqrt", "math.sqrt")
        expression = expression.replace("exp", "math.exp")
        expression = expression.replace("ln", "math.log")
        expression = expression.replace("pi", str(math.pi))
        expression = expression.replace("e", str(math.e))
        expression = expression.replace("^", "**")  # Power operator
        expression = expression.replace("mod", "%")

        try:
            # Evaluate the expression and return the result
            result = eval(expression)
            return result
        except Exception as e:
            return "Error"