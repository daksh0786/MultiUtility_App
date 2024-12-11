import random
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QFileDialog, QMenu, QAction, QVBoxLayout, QWidget, QGridLayout, QWidget, QLineEdit, QPushButton, QMessageBox, QLabel, QApplication
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt    



class Game2048(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2048 Game")
        self.setGeometry(100, 100, 400, 400)
        
        # Initialize the grid and tiles
        self.grid = [[0] * 4 for _ in range(4)]
        self.tiles = [[Tile() for _ in range(4)] for _ in range(4)]
        
        # Set up UI
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.layout = QGridLayout(central_widget)
        self.layout.setSpacing(5)

        for row in range(4):
            for col in range(4):
                self.layout.addWidget(self.tiles[row][col], row, col)

        self.setCentralWidget(central_widget)
        self.spawn_tile()  # Spawn two tiles at the start
        self.spawn_tile()

    def spawn_tile(self):
        # Ensure grid is intact before proceeding
        if not self.grid or len(self.grid) != 4 or any(len(row) != 4 for row in self.grid):
            print("Error: Grid is not valid!")
            return

        # Find empty cells
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]

        # If there are no empty cells, do nothing
        if not empty_cells:
            return

        # Randomly choose an empty cell and place a new tile (2 or 4)
        r, c = random.choice(empty_cells)
        self.grid[r][c] = random.choice([2])

        # Update the tiles display
        self.update_tiles()

    def update_tiles(self):
        # Loop over the grid and update the tile widgets
        for row in range(4):
            for col in range(4):
                self.tiles[row][col].value = self.grid[row][col]
                self.tiles[row][col].update_tile()

    def keyPressEvent(self, event):
        moved = False
        if event.key() == Qt.Key_Left:
            moved = self.move_left()
        elif event.key() == Qt.Key_Right:
            moved = self.move_right()
        elif event.key() == Qt.Key_Up:
            moved = self.move_up()
        elif event.key() == Qt.Key_Down:
            moved = self.move_down()

        # If any move was made, spawn a new tile
        if moved:
            self.spawn_tile()

    def move_left(self):
        new_grid = []
        for row in self.grid:
            filtered = [value for value in row if value != 0]
            merged = []
            skip = False
            for i in range(len(filtered)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(filtered) and filtered[i] == filtered[i + 1]:
                    merged.append(filtered[i] * 2)
                    skip = True
                else:
                    merged.append(filtered[i])
            new_grid.append(merged + [0] * (4 - len(merged)))

        self.grid = new_grid
        self.update_tiles()  # Update the tiles display
        return True

    def move_right(self):
        moved = False
        # Process each row for rightward movement
        for row in range(4):
            # Filter out zeros in the row
            filtered = [value for value in self.grid[row] if value != 0]
            merged = []
            skip = False
            for i in range(len(filtered)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(filtered) and filtered[i] == filtered[i + 1]:
                    merged.append(filtered[i] * 2)
                    skip = True
                else:
                    merged.append(filtered[i])
            
            # Add leading zeros to maintain the grid size
            new_row = [0] * (4 - len(merged)) + merged
            
            # Assign the updated row back to the grid
            if self.grid[row] != new_row:
                moved = True  # Mark that the grid has changed
            self.grid[row] = new_row
        
        # Update the tiles to reflect the new grid state
        self.update_tiles()
        return moved


    def move_up(self):
        self.grid = list(map(list, zip(*self.grid)))
        moved = self.move_left()
        self.grid = list(map(list, zip(*self.grid)))
        self.update_tiles()
        return moved

    def move_down(self):
        moved = False
        # Process each column for downward movement
        for col in range(4):
            # Extract the column
            column = [self.grid[row][col] for row in range(4)]
            
            # Move the values in the column as if it was a move left
            filtered = [value for value in column if value != 0]  # Filter out zeros
            merged = []
            skip = False
            for i in range(len(filtered)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(filtered) and filtered[i] == filtered[i + 1]:
                    merged.append(filtered[i] * 2)
                    skip = True
                else:
                    merged.append(filtered[i])
            
            # Add trailing zeros to maintain the grid size
            new_column = [0] * (4 - len(merged)) + merged
            
            # Assign the updated column back to the grid
            for row in range(4):
                if self.grid[row][col] != new_column[row]:
                    moved = True  # Mark that the grid has changed
                self.grid[row][col] = new_column[row]
        
        # Update the tiles to reflect the new grid state
        self.update_tiles()
        return moved


    @staticmethod
    def merge(row):
        non_zero = [x for x in row if x != 0]
        for i in range(len(non_zero) - 1):
            if non_zero[i] == non_zero[i + 1]:
                non_zero[i] *= 2
                non_zero[i + 1] = 0
        return [x for x in non_zero if x != 0] + [0] * (len(row) - len(non_zero))

    def can_move(self):
        for r in range(4):
            for c in range(4):
                if self.grid[r][c] == 0:
                    return True
                if c < 3 and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r < 3 and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False


class Tile(QLabel):
    def __init__(self, value=0):
        super().__init__()
        self.value = value
        self.update_tile()

    def update_tile(self):
        self.setText(str(self.value) if self.value != 0 else "")
        self.setStyleSheet(f"font-size: 24px; color: {'black' if self.value < 8 else 'white'}; "
                           f"background-color: {self.get_color(self.value)}; "
                           "border-radius: 8px; border: 2px solid gray;")
        self.setAlignment(Qt.AlignCenter)

    @staticmethod
    def get_color(value):
        colors = {
            0: "#CDC1B4", 2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179",
            16: "#F59563", 32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72",
            256: "#EDCC61", 512: "#EDC850", 1024: "#EDC53F", 2048: "#EDC22E"
        }
        return colors.get(value, "#3C3A32")