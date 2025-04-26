from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QInputDialog,
    QDialog,
    QListWidgetItem,
)


class ReminderDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/reminder_dialog.ui", self)


class MynWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/app.ui", self)

        self._createComponents()
        self._configureComponents()
        self._setupCallbacks()

    def _createComponents(self):
        pass

    def _configureComponents(self):
        self.deleteTaskButton.hide()
        self.deleteReminderButton.hide()

    def _setupCallbacks(self):
        self.actionExit.triggered.connect(lambda: self.close())

        self.taskSection.toggled.connect(self._onSectionChanged)
        self.reminderSection.toggled.connect(self._onSectionChanged)

        self.newTaskButton.pressed.connect(self._onNewTaskPressed)
        self.deleteTaskButton.pressed.connect(self._onDeleteTaskButtonPressed)

        self.taskList.itemSelectionChanged.connect(self._onTaskSelectionChange)
        self.taskList.itemDoubleClicked.connect(self._onItemDoubleClicked)

        self.newReminderButton.pressed.connect(self._onNewReminderPressed)

    def _onNewTaskPressed(self):
        task, ok = QInputDialog().getText(self, "New Task", "Task: ")

        if ok:
            item = QListWidgetItem(task)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

            self.taskList.addItem(item)

    def _onNewReminderPressed(self):
        dialog = ReminderDialog()

        if dialog.exec() == QDialog.Accepted:
            pass

    def _onSectionChanged(self, checked):
        sender = self.sender()

        if checked:
            if sender is self.taskSection:
                self.contentStack.setCurrentIndex(0)
            elif sender is self.reminderSection:
                self.contentStack.setCurrentIndex(1)

    def _onTaskSelectionChange(self):
        if not self.taskList.selectedItems():

            return

        self.deleteTaskButton.show()

    def _onItemDoubleClicked(self, item):
        newText, ok = QInputDialog().getText(self, "Edit Task", "Task: ",
                                             text=item.text())

        if ok:
            item.setText(newText)

    def _onDeleteTaskButtonPressed(self):
        items = self.taskList.selectedItems()
        for item in items:
            self.taskList.takeItem(self.taskList.row(item))

        self.deleteTaskButton.hide()
        self.taskList.clearSelection()


if __name__ == "__main__":
    app = QApplication([])
    win = MynWindow()
    win.show()
    app.exec()
