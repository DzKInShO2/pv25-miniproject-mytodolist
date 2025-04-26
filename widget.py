from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)


class MynWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/app.ui", self)

        self._createComponents()
        self._setupCallbacks()

    def _createComponents(self):
        pass

    def _setupCallbacks(self):
        self.actionExit.triggered.connect(lambda: self.close())

        self.taskSection.toggled.connect(self._onSectionChanged)
        self.reminderSection.toggled.connect(self._onSectionChanged)

    def _onSectionChanged(self, checked):
        sender = self.sender()

        if checked:
            if sender is self.taskSection:
                self.contentStack.setCurrentIndex(0)
            elif sender is self.reminderSection:
                self.contentStack.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication([])
    win = MynWindow()
    win.show()
    app.exec()
