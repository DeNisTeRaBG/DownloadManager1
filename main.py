import sys, requests, cloudscraper
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}

site_x = ''

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.edit = QLineEdit("Paste Download Link")
        self.button = QPushButton("Download")

        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.button.clicked.connect(self.download_link)

    def download_link(self):
        scraper = cloudscraper.create_scraper()

        site_x = self.edit.text()

        r = scraper.get(site_x, headers)

        if r.status_code == 200:
            with open("downloaded_image.png", "wb") as file:
                file.write(r.content)
                print("Image downloaded successfully!")
        else:
            print(f"Failed to download. Status code: {r.status_code}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())