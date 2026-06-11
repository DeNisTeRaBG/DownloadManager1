import sys
import os
from PySide6.QtWidgets import QApplication
from gui import MainWindow

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    app = QApplication(sys.argv)
    main_window = MainWindow()
    if len(sys.argv) > 1:
        passed_link = sys.argv[1].strip('"').strip("'")
        
        if passed_link.startswith("magnet:"):
            main_window.open_downloader_with_link(passed_link)

    main_window.show()
    sys.exit(app.exec())