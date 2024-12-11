import sys
import os
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QFont, QImageWriter
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QSlider, QFileDialog, QVBoxLayout, QWidget, QMessageBox


class ImageCompressorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Compressor")
        self.setGeometry(100, 100, 500, 450)

        # Set a light pastel background color for a professional feel
        self.setStyleSheet("background-color: #D7D3BF;")  # Pastel beige background color

        # Create a layout to hold UI components
        layout = QVBoxLayout()

        # Create a label to display the selected image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(490, 400)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px solid #B3D9FF;
                border-radius: 15px;
                background-color: #ECEFF1; /* Light grey */
            }
        """)
        layout.addWidget(self.image_label)

        # Create a button to open image file
        self.open_button = QPushButton("Open Image", self)
        self.open_button.clicked.connect(self.open_image)
        self.open_button.setStyleSheet("""
            QPushButton {
                background-color: #FFCC99;  /* Pastel yellow */
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #FFD54F;  /* Light yellow on hover */
            }
            QPushButton:pressed {
                background-color: #FFB74D;  /* Darker yellow on press */
            }
        """)
        layout.addWidget(self.open_button)

        # Create a label to display compression percentage
        self.percentage_label = QLabel("Compression Quality: 80%", self)
        self.percentage_label.setAlignment(Qt.AlignCenter)
        self.percentage_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.percentage_label)

        # Create a slider to control compression quality
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(1, 100)
        self.slider.setValue(80)  # Default quality
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #FFFFFF;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #FF5722;  /* Pastel orange */
                border: 1px solid #FF7043;
                width: 14px;
                height: 16px;
                margin: -4px 0;
                border-radius: 7px;
            }
        """)
        self.slider.valueChanged.connect(self.update_percentage)
        layout.addWidget(self.slider)

        # Create a button to compress the image
        self.compress_button = QPushButton("Compress Image", self)
        self.compress_button.clicked.connect(self.compress_image)
        self.compress_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;  /* Pastel orange */
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #FF7043;  /* Darker orange on hover */
            }
            QPushButton:pressed {
                background-color: #FF3D00;  /* Darker orange on press */
            }
        """)
        layout.addWidget(self.compress_button)

        # Set layout into a container widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_path = ""

    def open_image(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)", options=options)

        if self.image_path:
            # Display the selected image in the label
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

    def update_percentage(self):
        quality = self.slider.value()
        self.percentage_label.setText(f"Compression Quality: {quality}%")

    def compress_image(self):
        if not self.image_path:
            QMessageBox.warning(self, "No Image", "Please open an image first!")
            return

        # Get the quality from the slider
        quality = self.slider.value()

        try:
            # Get the directory where the script is located
            current_directory = os.path.dirname(os.path.abspath(__file__))

            # Save the compressed image in the same directory with a timestamp
            timestamp = int(time.time())
            compressed_image_path = os.path.join(current_directory, f'compressed_image_{timestamp}.jpg')

            # Compress the image
            image = QImage(self.image_path)
            if image.isNull():
                QMessageBox.warning(self, "Invalid Image", "The selected image could not be loaded!")
                return
            
            image_writer = QImageWriter(compressed_image_path)
            image_writer.setQuality(quality)
            if not image_writer.write(image):
                QMessageBox.warning(self, "Error", "Compression failed!")
                return
            
            # Show the compressed image in the label
            pixmap = QPixmap(compressed_image_path)
            self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
            QMessageBox.information(self, "Success", "Image compressed successfully!")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

