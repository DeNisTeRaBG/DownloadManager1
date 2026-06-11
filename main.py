import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui import MainWindow
from back import get_resource_path

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
        

    app = QApplication(sys.argv)

    app.setApplicationName("SnowPrism")
    app.setOrganizationName("DenisteraBG")

    icon_path = get_resource_path("app_icon.ico")
    app.setWindowIcon(QIcon(icon_path))

    main_window = MainWindow()
    if len(sys.argv) > 1:
        passed_link = sys.argv[1].strip('"').strip("'")
        
        if passed_link.startswith("magnet:"):
            main_window.open_downloader_with_link(passed_link)

    main_window.show()
    sys.exit(app.exec())