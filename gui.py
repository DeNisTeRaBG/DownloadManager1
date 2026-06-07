from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QHBoxLayout, QDialog, QFileDialog, 
                               QMainWindow, QWidget)
from PySide6.QtCore import Qt
from back import download_file

site_x = ''

class DownloaderPopup(QDialog):

    def __init__(self, parent=None):
        super(DownloaderPopup, self).__init__(parent)
        self.setWindowTitle("python")


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
        self.download_button.clicked.connect(self.download_link)

    def download_link(self):
            url = self.url_edit.text()
            folder_path = self.path_edit.text()

            print("Downloading...")
            
            success, message = download_file(url, folder_path)

            if success:
                print(message) 
            else:
                print("ERROR: " + message)

    def choose_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Download Folder")

        if folder_path:
            self.path_edit.setText(folder_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Hub")
        self.resize(500, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.open_downloader_btn = QPushButton("Install file with link")
        self.open_downloader_btn.setFixedSize(200, 50)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.open_downloader_btn, alignment=Qt.AlignCenter)

        self.open_downloader_btn.clicked.connect(self.open_downloader)

    def open_downloader(self):
        downloader_dialog = DownloaderPopup(self)
        
        downloader_dialog.setFixedSize(700, 150)
        
        downloader_dialog.exec()

    