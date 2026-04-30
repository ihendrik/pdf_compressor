import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.ui_main import MainWindow

app = QApplication(sys.argv)

with open("assets/style.qss") as f:
    app.setStyleSheet(f.read())

w = MainWindow()
w.setWindowIcon(QIcon("assets/app.ico"))
w.show()

sys.exit(app.exec())