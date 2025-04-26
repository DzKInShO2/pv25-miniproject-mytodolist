from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox
)


class MynWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("app.ui", self)

        self.__createComponents()
        self.__setupCallbacks()

    def __createComponents(self):
        self.aboutBox = QMessageBox()
        self.aboutBox.setWindowTitle("About Application")
        self.aboutBox.setIcon(QMessageBox.Icon.Information)
        self.aboutBox.setStandardButtons(QMessageBox.StandardButton.Close)

    def __setupCallbacks(self):
        self.actionAbout.triggered.connect(lambda: self.__aboutMessage())
        self.actionExit.triggered.connect(lambda: self.close())

    def __aboutMessage(self):
        self.aboutBox.exec()


if __name__ == "__main__":
    app = QApplication([])

    win = MynWindow()
    win.show()
    app.exec()
