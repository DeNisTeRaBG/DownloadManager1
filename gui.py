import os, cloudscraper, re
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QHBoxLayout, QDialog, QFileDialog, 
                               QMainWindow, QWidget)
from PySide6.QtCore import Qt
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}

site_x = ''

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
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
        main_layout.addLayout(path_layout) # Add the horizontal row we made above
        main_layout.addStretch()

        self.setLayout(main_layout)

        self.browse_button.clicked.connect(self.choose_path)
        self.download_button.clicked.connect(self.download_link)

    def choose_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Download Folder")

        if folder_path:
            self.path_edit.setText(folder_path)

    def download_link(self):
        site_x = self.url_edit.text()
        folder_path = self.path_edit.text()

        if not site_x:
            print("Error: Please provide both a link")
            return

        match = re.search(r'/([^/]+\.(jpg|png|txt))$', site_x, re.IGNORECASE)
        filename = match.group(1) if match else "downloaded_file.png"

        final_save_path = os.path.join(folder_path, filename)

        scraper = cloudscraper.create_scraper()
        print("Downloading...")

        try:
            r = scraper.get(site_x, headers=headers)

            if r.status_code == 200:
                # Save using the combined path
                with open(final_save_path, "wb") as file:
                    file.write(r.content)
                print(f"File downloaded successfully to:\n{final_save_path}")
            else:
                print(f"Failed to download. Status code: {r.status_code}")
        except Exception as e:
            print(f"A network error occurred: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Hub")
        self.resize(500, 300) # Give the main window a decent size

        # In QMainWindow, you need a "Central Widget" to hold your layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a button for the main window
        self.open_downloader_btn = QPushButton("Open Image Downloader")
        self.open_downloader_btn.setFixedSize(200, 50)

        # Create a layout for the main window and center the button
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.open_downloader_btn, alignment=Qt.AlignCenter)

        # Connect the button to the function that opens the dialog
        self.open_downloader_btn.clicked.connect(self.open_downloader)

    def open_downloader(self):
        # Create an instance of your downloader Form
        downloader_dialog = Form(self)
        
        # Apply your fixed size to the popup here
        downloader_dialog.setFixedSize(700, 150)
        
        # Open it as a popup!
        downloader_dialog.exec()