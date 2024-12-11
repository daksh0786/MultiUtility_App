# # -*- coding: utf-8 -*-

# Import necessary modules from PyQt5
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from Components.notepad import NotepadWindow
from Components.imageClassifier import ClassifierWindow
from Components.calculator import CalculatorWindow
from Components.imageCompress import ImageCompressorWindow
from Components.game2048 import Game2048
from Components.suduko import Sudoku
from Components.sqlServer import SQLServer
from Components.objectDetection import ObjectDetection


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        """
        Set up the UI components of the main window.
        """
        # Configure main window properties
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1112, 722)
        
        # Set global font for the window
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        MainWindow.setFont(font)
        
        # Set the background color of the main window
        MainWindow.setStyleSheet("background-color: #EAEAEA;")  # Soft neutral background color

        # Initialize the central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create a main vertical layout
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Title Label
        self.label = QtWidgets.QLabel("APP SUITE", self.centralwidget)
        title_font = QtGui.QFont()
        title_font.setFamily("Segoe UI Symbol")
        title_font.setPointSize(18)
        self.label.setFont(title_font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.label)

        # Create a grid layout for buttons and labels
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setHorizontalSpacing(40)  # Set horizontal spacing
        self.grid_layout.setVerticalSpacing(20)    # Set vertical spacing
        self.grid_layout.setContentsMargins(10, 10, 10, 10)  # Set layout margins

        # Add buttons with icons to the grid and different colors for each button
        def get_resource_path(relative_path):
            if getattr(sys, 'frozen', False):
                # If running as a bundled executable
                base_path = sys._MEIPASS
            else:
                # If running as a normal script
                base_path = os.path.dirname(__file__)

            return os.path.join(base_path, relative_path)

        # Updated button creation using resolved paths
        self.pushButton = self.create_icon_button(get_resource_path("resources/calculator_icon.png"), "Calculator", "#A7D8D7")
        self.pushButton_2 = self.create_icon_button(get_resource_path("resources/compressor_icon.png"), "Image Compressor", "#FFE3E3")
        self.pushButton_3 = self.create_icon_button(get_resource_path("resources/ear_recognition.png"), "Ear Recognition", "#C6E7FF")
        self.pushButton_4 = self.create_icon_button(get_resource_path("resources/notepad_icon.png"), "NotePad", "#EF9C66")
        self.pushButton_5 = self.create_icon_button(get_resource_path("resources/suduko_icon.png"), "Sudoku Solver", "#B3D9FF")
        self.pushButton_6 = self.create_icon_button(get_resource_path("resources/game2048_icon.png"), "Image", "#FFCC99")
        self.pushButton_7 = self.create_icon_button(get_resource_path("resources/SQL_server_icon.png"), "SQL", "#FFD700")
        self.pushButton_8 = self.create_icon_button(get_resource_path("resources/object_detect_icon.png"), "Object_detect", "#D3D3D3")

        # Add corresponding labels for the apps
        self.label_3 = self.create_label("Calculator", font_size=12)
        self.label_4 = self.create_label("Image Compressor", font_size=12)
        self.label_5 = self.create_label("Ear Recognition", font_size=12)
        self.label_6 = self.create_label("NotePad", font_size=12)
        self.label_7 = self.create_label("Sudoku Solver", font_size=12)
        self.label_8 = self.create_label("game2048", font_size=12)
        self.label_9 = self.create_label("SQL_Server", font_size=12)
        self.label_10 = self.create_label("object_detect", font_size=12)

        # Arrange buttons and labels in the grid layout
        self.add_to_grid(0, 0, self.pushButton, self.label_3)
        self.add_to_grid(0, 1, self.pushButton_2, self.label_4)
        self.add_to_grid(0, 2, self.pushButton_3, self.label_5)
        self.add_to_grid(0, 3, self.pushButton_4, self.label_6)
        self.add_to_grid(1, 0, self.pushButton_5, self.label_7)
        self.add_to_grid(1, 1, self.pushButton_6, self.label_8)
        self.add_to_grid(1, 2, self.pushButton_7, self.label_9)
        self.add_to_grid(1, 3, self.pushButton_8, self.label_10)

        # Add the grid layout to the main layout
        self.main_layout.addLayout(self.grid_layout)

        # Footer Label
        self.label_2 = QtWidgets.QLabel("© 2024", self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.label_2)

        # Set the central widget and its layout
        MainWindow.setCentralWidget(self.centralwidget)

        # Connect signals and slots
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connecting events to functions
        self.pushButton.clicked.connect(self.open_calculator)
        self.pushButton_2.clicked.connect(self.open_image_compressor)
        self.pushButton_3.clicked.connect(self.open_classifier)
        self.pushButton_4.clicked.connect(self.open_notepad)
        self.pushButton_5.clicked.connect(self.open_sudoku)
        self.pushButton_6.clicked.connect(self.open_game2048)
        self.pushButton_7.clicked.connect(self.open_SQL_Server)
        self.pushButton_8.clicked.connect(self.open_Obeject_detect)

    def create_label(self, text, font_size=10):
        """
        Helper function to create a label with customizable font size.
        """
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        # Set the font for the label with the specified size
        font = QtGui.QFont()
        font.setPointSize(font_size)
        label.setFont(font)

        return label
    
    def create_icon_button(self, icon_path, tooltip, bg_color):
        """
        Helper function to create a button with an icon.
        """
        button = ResizableIconButton(icon_path, tooltip, bg_color)  # Use the custom button class
        return button

    def add_to_grid(self, row, col, button, label):
        """
        Helper function to add a button and label to the grid layout.
        """
        self.grid_layout.addWidget(button, row * 2, col)
        self.grid_layout.addWidget(label, row * 2 + 1, col)

    # Event handlers to open windows
    def open_calculator(self):
        self.calc_window = CalculatorWindow()
        self.calc_window.show()

    def open_notepad(self):
        self.notepad_window = NotepadWindow()
        self.notepad_window.show()

    def open_image_compressor(self):
        self.image_compressor_window = ImageCompressorWindow()
        self.image_compressor_window.show()

    def open_classifier(self):
        self.classifier_window = ClassifierWindow()
        self.classifier_window.show()

    def open_sudoku(self):
        self.sudoku_window = Sudoku()
        self.sudoku_window.show()

    def open_game2048(self):
        self.sudoku_window = Game2048()
        self.sudoku_window.show()

    def open_SQL_Server(self):
        self.sudoku_window = SQLServer()
        self.sudoku_window.show()

    def open_Obeject_detect(self):
        self.sudoku_window = ObjectDetection()
        self.sudoku_window.show()


class ResizableIconButton(QtWidgets.QPushButton):
    def __init__(self, icon_path, tooltip, bg_color, parent=None):
        """
        Custom QPushButton with a resizable icon and minimal padding.
        """
        super().__init__(parent)
        self.icon_path = icon_path
        self.setToolTip(tooltip)

        # Set the icon for the button
        self.setIcon(QtGui.QIcon(self.icon_path))

        # Set the initial icon size
        self.setIconSize(QtCore.QSize(64, 64))  # Default size

        # Set the button style to minimize padding and apply background color
        self.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid #B3D9FF;  /* Light border */
                padding: 2px;  /* Thin padding around the icon */
                border-radius: 12px;  /* Rounded corners */
                background-color: {bg_color};  /* Set background color */
            }}
            QPushButton:hover {{
                cursor: pointer;  /* Change cursor to pointer when hovered */
                background-color: #FFB74D;  /* Highlight color on hover */
            }}
            QPushButton:focus {{
                outline: none; /* Remove focus outline */
            }}
        """)

        # Ensure the button has an expanding size policy
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
