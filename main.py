import os, sys, requests, cloudscraper, re
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QHBoxLayout, QDialog, QFileDialog)

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

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_button)

        self.download_button = QPushButton("Download")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.url_edit)
        main_layout.addLayout(path_layout) # Add the horizontal row we made above
        main_layout.addWidget(self.download_button)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())