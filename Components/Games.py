import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class SudokuGame(QMainWindow):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Sudoku Game")
        self.setGeometry(100, 100, 600, 600)
        self.sudoku_grid = [[0] * 9 for _ in range(9)]
        self.create_ui()

    def create_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.layout = QGridLayout()
        self.layout.setSpacing(5)

        self.cells = {}
        for row in range(9):
            for col in range(9):
                cell = QLineEdit()
                cell.setAlignment(Qt.AlignCenter)
                cell.setMaxLength(1)
                cell.setStyleSheet("font-size: 18px;")
                cell.textChanged.connect(lambda _, r=row, c=col: self.validate_input(r, c))
                self.layout.addWidget(cell, row, col)
                self.cells[(row, col)] = cell

        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_sudoku)
        self.layout.addWidget(self.solve_button, 9, 4)

        central_widget.setLayout(self.layout)

    def validate_input(self, row, col):
        text = self.cells[(row, col)].text()
        if text and not text.isdigit():
            self.cells[(row, col)].setText("")

    def solve_sudoku(self):
        self.sudoku_grid = [[int(self.cells[(r, c)].text() or 0) for c in range(9)] for r in range(9)]
        if self.solve(0, 0):
            self.update_ui()
        else:
            QMessageBox.warning(self, "Invalid Sudoku", "No solution exists for this puzzle.")

    def update_ui(self):
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].setText(str(self.sudoku_grid[row][col]))

    def is_valid(self, row, col, num):
        for x in range(9):
            if self.sudoku_grid[row][x] == num or self.sudoku_grid[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.sudoku_grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(self, row, col):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuGame()
    window.show()
    sys.exit(app.exec_())