# notepadwindow.py
import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QFileDialog, QMenu, QAction, QVBoxLayout, QWidget, 
    QGridLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QApplication, 
    QStatusBar, QDialog, QDialogButtonBox, QVBoxLayout, QFontDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


# class NotepadWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Notepad")
#         self.setGeometry(100, 100, 800, 600)
#         self.setStyleSheet("background-color: #F2F2F2;")

#         # Notepad setup
#         self.text_area = QTextEdit(self)
#         self.setCentralWidget(self.text_area)
#         self.text_area.setStyleSheet("""
#             background-color: #FFFFFF; 
#             font-family: 'Consolas', 'Courier New', monospace; 
#             font-size: 12px;
#             color: black;
#             padding: 10px;
#         """)

#         # Initialize status bar
#         self.status_bar = QStatusBar(self)
#         self.setStatusBar(self.status_bar)

#         # File menu
#         self.create_menu()

#         # Set the undo/redo actions
#         self.undo_action = self.text_area.undo
#         self.redo_action = self.text_area.redo
#         self.text_area.textChanged.connect(self.update_status_bar)

#     def create_menu(self):
#         menubar = self.menuBar()

#         # File Menu
#         file_menu = menubar.addMenu("File")
#         new_action = QAction("New", self)
#         new_action.triggered.connect(self.new_file)
#         open_action = QAction("Open...", self)
#         open_action.triggered.connect(self.open_file)
#         save_action = QAction("Save", self)
#         save_action.triggered.connect(self.save_file)
#         save_as_action = QAction("Save As...", self)
#         save_as_action.triggered.connect(self.save_as_file)
#         exit_action = QAction("Exit", self)
#         exit_action.triggered.connect(self.close)

#         file_menu.addAction(new_action)
#         file_menu.addAction(open_action)
#         file_menu.addAction(save_action)
#         file_menu.addAction(save_as_action)
#         file_menu.addAction(exit_action)

#         # Edit Menu
#         edit_menu = menubar.addMenu("Edit")
#         undo_action = QAction("Undo", self)
#         undo_action.triggered.connect(self.text_area.undo)
#         redo_action = QAction("Redo", self)
#         redo_action.triggered.connect(self.text_area.redo)
#         cut_action = QAction("Cut", self)
#         cut_action.triggered.connect(self.cut_text)
#         copy_action = QAction("Copy", self)
#         copy_action.triggered.connect(self.copy_text)
#         paste_action = QAction("Paste", self)
#         paste_action.triggered.connect(self.paste_text)

#         edit_menu.addAction(undo_action)
#         edit_menu.addAction(redo_action)
#         edit_menu.addAction(cut_action)
#         edit_menu.addAction(copy_action)
#         edit_menu.addAction(paste_action)

#         # Format Menu
#         format_menu = menubar.addMenu("Format")
#         font_action = QAction("Font...", self)
#         font_action.triggered.connect(self.change_font)
#         format_menu.addAction(font_action)

#         # Help Menu
#         help_menu = menubar.addMenu("Help")
#         about_action = QAction("About", self)
#         about_action.triggered.connect(self.about_notepad)
#         help_menu.addAction(about_action)

#     def new_file(self):
#         self.text_area.clear()

#     def open_file(self):
#         options = QFileDialog.Options()
#         file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
#         if file_path:
#             with open(file_path, 'r') as f:
#                 content = f.read()
#             self.text_area.setText(content)

#     def save_file(self):
#         file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
#         if file_path:
#             with open(file_path, 'w') as f:
#                 f.write(self.text_area.toPlainText())

#     def save_as_file(self):
#         file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Text Files (*.txt);;All Files (*)")
#         if file_path:
#             with open(file_path, 'w') as f:
#                 f.write(self.text_area.toPlainText())

#     def cut_text(self):
#         self.text_area.cut()

#     def copy_text(self):
#         self.text_area.copy()

#     def paste_text(self):
#         self.text_area.paste()

#     def change_font(self):
#     # Open the font dialog and get the selected font
#         font, ok = QFontDialog.getFont(self)
        
#         if ok:
#             # Apply the selected font to the text area
#             self.text_area.setFont(font)

#     def update_status_bar(self):
#         cursor = self.text_area.textCursor()
#         line = cursor.blockNumber() + 1
#         column = cursor.columnNumber() + 1
#         self.status_bar.showMessage(f"Line: {line}  Column: {column}")

#     def about_notepad(self):
#         QMessageBox.information(self, "About", "Windows Notepad-like application built with PyQt5.")

# import sys
# import os
# from PyQt5.QtWidgets import (
#     QMainWindow, QTextEdit, QFileDialog, QMenu, QAction, QVBoxLayout, QWidget, 
#     QGridLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QApplication, 
#     QStatusBar, QDialog, QDialogButtonBox, QVBoxLayout, QFontDialog, QFindDialog, QReplaceDialog
# )
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QFont, QTextCursor


class NotepadWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #F2F2F2;")

        # Notepad setup
        self.text_area = QTextEdit(self)
        self.setCentralWidget(self.text_area)
        self.text_area.setStyleSheet("""
            background-color: #FFFFFF; 
            font-family: 'Consolas', 'Courier New', monospace; 
            font-size: 12px;
            color: black;
            padding: 10px;
        """)

        # Initialize status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # File menu
        self.create_menu()

        # Set the undo/redo actions
        self.undo_action = self.text_area.undo
        self.redo_action = self.text_area.redo
        self.text_area.textChanged.connect(self.update_status_bar)

    def create_menu(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_file)
        open_action = QAction("Open...", self)
        open_action.triggered.connect(self.open_file)
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        save_as_action = QAction("Save As...", self)
        save_as_action.triggered.connect(self.save_as_file)
        print_action = QAction("Print", self)
        print_action.triggered.connect(self.print_file)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(print_action)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("Edit")
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.text_area.undo)
        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.text_area.redo)
        cut_action = QAction("Cut", self)
        cut_action.triggered.connect(self.cut_text)
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copy_text)
        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.paste_text)
        select_all_action = QAction("Select All", self)
        select_all_action.triggered.connect(self.select_all_text)
        find_action = QAction("Find...", self)
        find_action.triggered.connect(self.find_text)
        replace_action = QAction("Replace...", self)
        replace_action.triggered.connect(self.replace_text)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(select_all_action)
        edit_menu.addAction(find_action)
        edit_menu.addAction(replace_action)

    def new_file(self):
        self.text_area.clear()

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'r') as f:
                content = f.read()
            self.text_area.setText(content)

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.text_area.toPlainText())

    def save_as_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.text_area.toPlainText())

    def print_file(self):
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            self.text_area.print_(printer)

    def cut_text(self):
        self.text_area.cut()

    def copy_text(self):
        self.text_area.copy()

    def paste_text(self):
        self.text_area.paste()

    def select_all_text(self):
        self.text_area.selectAll()

    def find_text(self):
        text, ok = QInputDialog.getText(self, 'Find', 'Find:')
        if ok:
            cursor = self.text_area.textCursor()
            document = self.text_area.document()
            search_result = document.find(text, cursor)
            if not search_result:
                QMessageBox.information(self, "Not Found", "The text was not found.")

    def replace_text(self):
        find_text, ok = QInputDialog.getText(self, 'Replace', 'Find:')
        if ok:
            replace_text, ok2 = QInputDialog.getText(self, 'Replace', 'Replace with:')
            if ok2:
                cursor = self.text_area.textCursor()
                document = self.text_area.document()
                while document.find(find_text, cursor):
                    cursor.insertText(replace_text)
                QMessageBox.information(self, "Replaced", "Text replaced successfully.")

    def update_status_bar(self):
        cursor = self.text_area.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.status_bar.showMessage(f"Line: {line}  Column: {column}")


