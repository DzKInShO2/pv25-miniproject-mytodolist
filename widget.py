from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow
)


class MynWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("app.ui", self)


if __name__ == "__main__":
    app = QApplication([])

    win = MynWindow()
    win.show()

    app.exec()
