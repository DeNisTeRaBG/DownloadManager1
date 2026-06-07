from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QHBoxLayout, QDialog, QFileDialog, 
                               QMainWindow, QWidget)
from PySide6.QtCore import Qt, QThread, Signal
from back import *

site_x = ''


class DownloadWorker(QThread):
    finished_signal = Signal(bool, str) 

    def __init__(self, url, folder_path):
        super().__init__()
        self.url = url
        self.folder_path = folder_path

    def run(self):
        """This runs in the background perfectly isolated from the UI"""
        match = re.search(r'/([^/]+\.(jpg|jpeg|png|gif|txt))$', self.url, re.IGNORECASE)
        filename = match.group(1) if match else "downloaded_file.png"
        final_save_path = os.path.join(self.folder_path, filename)

        scraper = cloudscraper.create_scraper()
        
        try:
            r = scraper.get(self.url, headers=headers)
            if r.status_code == 200:
                with open(final_save_path, "wb") as file:
                    file.write(r.content)
                self.finished_signal.emit(True, f"Success! Saved to:\n{final_save_path}")
            else:
                self.finished_signal.emit(False, f"Failed. Status code: {r.status_code}")
        except Exception as e:
            self.finished_signal.emit(False, f"Network error: {e}")


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

        # 1. Lock the UI so they don't click it twice
        self.download_button.setEnabled(False)
        self.download_button.setText("Downloading...")
        print("Download started in background...")

        # 2. Create the worker and hand it the data
        self.worker = DownloadWorker(url, folder_path)
        
        # 3. Connect the worker's signal to our wrap-up function
        self.worker.finished_signal.connect(self.on_download_finished)
        
        # 4. Start the background thread!
        self.worker.start()

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