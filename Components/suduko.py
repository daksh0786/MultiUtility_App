import random
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QGridLayout, QWidget, QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Sudoku(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setGeometry(100, 100, 600, 600)  # Fixed square geometry for the app
        self.create_ui()

    def create_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create the layout for the grid
        self.layout = QGridLayout()
        self.layout.setSpacing(3)

        # Create the grid of cells with square-shaped placeholders and styling
        self.cells = {}
        for row in range(9):
            for col in range(9):
                cell = QLineEdit()
                cell.setAlignment(Qt.AlignCenter)
                cell.setMaxLength(1)
                cell.setFont(QFont('Arial', 20))
                cell.setStyleSheet("""
                    QLineEdit {
                        width: 60px;
                        height: 60px;
                        font-size: 20px;
                        text-align: center;
                        border: 2px solid #D3D3D3;
                        border-radius: 8px;
                        background-color: #FFF9C4;
                    }
                    QLineEdit:focus {
                        border-color: #FFB74D; /* Highlight color on focus */
                    }
                """)
                cell.textChanged.connect(lambda _, r=row, c=col: self.validate_input(r, c))
                self.layout.addWidget(cell, row, col)
                self.cells[(row, col)] = cell

        # Create the "Solve" button with a stylized appearance
        self.solve_button = QPushButton("Solve")
        self.solve_button.setStyleSheet("""
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
        self.solve_button.clicked.connect(self.solve_sudoku)

        # Create a "Clear" button to reset the grid
        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #FF7043;
                font-size: 18px;
                color: white;
                padding: 15px;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF5722;
            }
        """)
        self.clear_button.clicked.connect(self.clear_grid)

        # Create a layout to add buttons and center them
        button_layout = QGridLayout()
        button_layout.addWidget(self.solve_button, 0, 0)
        button_layout.addWidget(self.clear_button, 0, 1)

        # Center the buttons horizontally in the layout
        button_layout.setColumnStretch(0, 1)
        button_layout.setColumnStretch(1, 1)

        # Add the button layout below the grid
        self.layout.addLayout(button_layout, 9, 0, 1, 9)

        # Add the layout to the central widget
        central_widget.setLayout(self.layout)

    def clear_grid(self):
        """Clear the grid for a new puzzle."""
        for (row, col) in self.cells:
            self.cells[(row, col)].clear()

    def validate_input(self, row, col):
        """Validate that input is a number from 1 to 9, otherwise clear the input."""
        text = self.cells[(row, col)].text()
        if text and (not text.isdigit() or int(text) < 1 or int(text) > 9):
            self.cells[(row, col)].clear()
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number between 1 and 9.")

        
        num = int(text) if text else None
        if num:
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)  # Identify the top-left corner of the 3x3 subgrid
            subgrid_values = []

            # Collect values from the 3x3 subgrid
            for i in range(3):
                for j in range(3):
                    if (start_row + i, start_col + j) != (row, col):  # Skip the current cell
                        value = self.cells[(start_row + i, start_col + j)].text()
                        if value.isdigit():
                            subgrid_values.append(int(value))

            # If the number already exists in the subgrid, show a warning
            if num in subgrid_values:
                self.cells[(row, col)].clear()
                QMessageBox.warning(self, "Duplicate in Subgrid", "This number already exists in the 3x3 subgrid. Please choose another number.")


    def solve_sudoku(self):
        """Solve the Sudoku puzzle."""
        # Convert text input into a 2D list of integers
        self.sudoku_grid = [[int(self.cells[(r, c)].text() or 0) for c in range(9)] for r in range(9)]
        
        # Validate if the grid contains any invalid input before solving
        for r in range(9):
            for c in range(9):
                if self.sudoku_grid[r][c] != 0 and not (1 <= self.sudoku_grid[r][c] <= 9):
                    QMessageBox.warning(self, "Invalid Input", "Please enter a valid Sudoku grid with numbers from 1 to 9.")
                    return False
        
        # Attempt to solve the puzzle
        if self.solve(0, 0):
            self.update_ui()
        else:
            QMessageBox.warning(self, "Invalid Sudoku", "No solution exists for this puzzle.")
            return False

    def update_ui(self):
        """Update the grid with the solved Sudoku values."""
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].setText(str(self.sudoku_grid[row][col]))

    def is_valid(self, row, col, num):
        """Check if placing a number in the given cell is valid."""
        # Check row and column for conflicts
        for x in range(9):
            if self.sudoku_grid[row][x] == num or self.sudoku_grid[x][col] == num:
                return False
        
        # Check 3x3 subgrid for conflicts
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.sudoku_grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(self, row, col):
        """Solve the Sudoku puzzle using backtracking."""
        if row == 9:
            return True
        if col == 9:
            return self.solve(row + 1, 0)
        if self.sudoku_grid[row][col] != 0:
            return self.solve(row, col + 1)
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.sudoku_grid[row][col] = num
                if self.solve(row, col + 1):
                    return True
                self.sudoku_grid[row][col] = 0
        
        return False