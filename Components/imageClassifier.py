import os
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QFileDialog, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import pickle
import cv2
import numpy as np
from skimage.feature import local_binary_pattern

class ClassifierWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Classifier")
        self.setGeometry(100, 100, 500, 700)  # Changed geometry to be horizontal (landscape)
        self.setStyleSheet("background-color: #D7D3BF;")  # Pastel background color

        # Load model
        with open("Model/model_saved_ear_LBP.unknown", 'rb') as f:
            self.model = pickle.load(f)

        self.classnames = ['ali', 'daksh', 'khan', 'prath', 'raj']

        # Create layout and widgets
        main_layout = QVBoxLayout()

        # Create a horizontal layout to hold two images side by side
        images_layout = QHBoxLayout()

        # Create the first image label to display an image
        self.image_label1 = QLabel(self)
        self.image_label1.setAlignment(Qt.AlignCenter)
        self.image_label1.setStyleSheet("""
            border: 3px solid #FFF6E3;
            border-radius: 10px;
            background-color: #ECEBDE;
        """)
        images_layout.addWidget(self.image_label1)

        # Create the second image label to display another image
        self.image_label2 = QLabel(self)
        self.image_label2.setAlignment(Qt.AlignCenter)
        self.image_label2.setStyleSheet("""
            border: 3px solid #FFF6E3;
            border-radius: 10px;
            background-color: #ECEBDE;
        """)
        images_layout.addWidget(self.image_label2)

        # Add the images layout (side by side) to the main layout
        main_layout.addLayout(images_layout)

        # Create a button to open images
        self.open_button = QPushButton("Open Image", self)
        self.open_button.setStyleSheet("""
            background-color: #FFCC99;
            border-radius: 12px;
            padding: 10px;
        """)
        self.open_button.clicked.connect(self.open_image)
        main_layout.addWidget(self.open_button)

        # Create the result label to display predicted class
        self.result_label = QLabel("Predicted Class: ", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 18px;            /* Adjust font size */
            font-weight: bold;         /* Make the text bold */
            color: #333333;
            margin-top: 5px;          /* Reduce space above */
            margin-bottom: 5px;        /* Reduce space below */
            padding: 5px;              /* Reduce padding */
        """)
        main_layout.addWidget(self.result_label)

        # Set the layout into a container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # To store the paths of the two selected images
        self.image_path1 = ""
        self.image_path2 = ""

    def open_image(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)", options=options)
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.image_label1.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
            self.classify_image()

    def preprocess_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.resize(image, (150, 150))
        lbp = local_binary_pattern(image, P=8, R=1)

        # Normalize LBP values to the range [0, 255] for better visibility
        lbp_normalized = np.uint8(lbp / lbp.max() * 255)  # Normalize to 8-bit image range

        # Convert the normalized LBP image to a QImage
        lbp_image = QImage(lbp_normalized.data, lbp_normalized.shape[1], lbp_normalized.shape[0], lbp_normalized.strides[0], QImage.Format_Grayscale8)

        # Convert the QImage to a QPixmap and set it to image_label2
        pixmap = QPixmap.fromImage(lbp_image)
        self.image_label2.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

        histogram = self.create_histogram(lbp, sub_images_num=3, bins_per_sub_images=64)
        
        return histogram.reshape(1, -1)

    def create_histogram(self, image, sub_images_num, bins_per_sub_images):
        grid = np.arange(0, image.shape[1] + 1, image.shape[1] // sub_images_num)
        sub_image_histograms = []
        for i in range(1, len(grid)):
            for j in range(1, len(grid)):
                sub_image = image[grid[i - 1]:grid[i], grid[j - 1]:grid[j]]
                sub_image_histogram = np.histogram(sub_image, bins=bins_per_sub_images)[0]
                sub_image_histograms.append(sub_image_histogram)
        
        return np.array(sub_image_histograms).flatten()
    

    def classify_image(self):
        histogram = self.preprocess_image(self.image_path)
        prediction = self.model.predict(histogram)
        predicted_class = self.classnames[prediction[0]]
        self.result_label.setText(f"Predicted Class: {predicted_class}")
