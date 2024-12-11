import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainWindow import Ui_MainWindow  # Import the correct Ui_MainWindow class
from PyQt5 import QtCore, QtGui, QtWidgets  # Correct import



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create an instance of QMainWindow
    main_window = QMainWindow()  # Create the main window
    
    # Create an instance of Ui_MainWindow and set up the UI
    ui = Ui_MainWindow()
    ui.setupUi(main_window)  # Set up the UI on the main window
    
    main_window.show()  # Show the main window
    
    sys.exit(app.exec_())  # Start the Qt application event loop

