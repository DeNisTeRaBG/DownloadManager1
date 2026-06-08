from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QHBoxLayout, QDialog, QFileDialog, 
                               QMainWindow, QWidget)
from PySide6.QtCore import Qt, QThread, Signal
from back import *

site_x = ''


class DownloadWorker(QThread):
    progress_signal = Signal(str)
    finished_signal = Signal(bool, str) 

    def __init__(self, url, folder_path):
        super().__init__()
        self.url = url
        self.folder_path = folder_path

    def run(self):
        success, message = process_download(
            self.link, 
            self.folder_path, 
            progress_callback=self.progress_signal.emit
        )
        
        self.finished_signal.emit(success, message)


class DownloadDialog(QDialog):
    def __init__(self, parent=None):
        super(DownloadDialog, self).__init__(parent)
        self.setWindowTitle("Downloader")

        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("Paste Download Link")

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Choose where to save...")
        self.path_edit.setReadOnly(True)
        
        self.browse_button = QPushButton("Browse...")
        self.download_button = QPushButton("Download")

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_button)
        path_layout.addWidget(self.download_button, alignment=Qt.AlignRight)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)

        main_layout.addWidget(self.url_edit)
        main_layout.addLayout(path_layout) 
        main_layout.addStretch()

        self.setLayout(main_layout)

        self.browse_button.clicked.connect(self.choose_path)
        self.download_button.clicked.connect(self.start_download)

    def choose_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder_path:
            self.path_edit.setText(folder_path)

    def start_download(self):
        url = self.url_edit.text()
        folder_path = self.path_edit.text()

        if not url or not folder_path:
            print("Error: Please provide a link and a save path.")
            return

        self.download_button.setEnabled(False)
        self.download_button.setText("Working...")

        # Create the worker
        self.worker = DownloadWorker(link, folder_path)
        
        # Connect both signals
        self.worker.progress_signal.connect(self.on_progress_update)
        self.worker.finished_signal.connect(self.on_download_finished)
        
        # Start the background thread
        self.worker.start()

    def on_progress_update(self, current_status):
        print(current_status)

    def on_download_finished(self, success, message):
        """This function triggers automatically when the worker emits its signal"""
        
        # 1. Unlock the UI again
        self.download_button.setEnabled(True)
        self.download_button.setText("Download")

        # 2. Print the result
        if success:
            print(message)
        else:
            print(f"ERROR: {message}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Hub")
        self.resize(500, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.open_downloader_btn = QPushButton("Open Image Downloader")
        self.open_downloader_btn.setFixedSize(200, 50)


        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.open_downloader_btn, alignment=Qt.AlignCenter)


        self.open_downloader_btn.clicked.connect(self.open_downloader)

    def open_downloader(self):
        downloader_dialog = DownloadDialog(self)
        
        downloader_dialog.setFixedSize(700, 150)
        
        downloader_dialog.exec()