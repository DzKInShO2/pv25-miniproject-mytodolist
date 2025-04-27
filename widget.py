from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QInputDialog,
    QDialog,
    QListWidgetItem,
    QMessageBox,
)


class ReminderDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/reminder_dialog.ui", self)

    def getData(self) -> dict:
        return {
            "title": self.titleLineEdit.text(),
            "month": self.monthComboBox.currentText(),
            "date":  self.dateSpinBox.value()
        }

    def setData(self, data: dict) -> None:
        self.titleLineEdit.setText(data["title"])
        self.monthComboBox.setCurrentText(data["month"])
        self.dateSpinBox.setValue(data["date"])


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

        self.newReminderButton.pressed.connect(self._onNewReminderPressed)
        self.deleteReminderButton.pressed.connect(
            self._onDeleteReminderButtonPressed)

        self.taskList.itemSelectionChanged.connect(self._onTaskSelectionChange)
        self.taskList.itemDoubleClicked.connect(self._onTaskDoubleClicked)

        self.reminderList.itemDoubleClicked.connect(
            self._onReminderDoubleClicked)
        self.reminderList.itemSelectionChanged.connect(
            self._onReminderSelectionChange)

    def _onNewTaskPressed(self):
        task, ok = QInputDialog().getText(self, "New Task", "Task: ")

        if ok:
            item = QListWidgetItem(task)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

            self.taskList.addItem(item)

    def _onNewReminderPressed(self):
        dialog = ReminderDialog()
        while True:
            status = dialog.exec()
            if status == QDialog.Accepted:
                data = dialog.getData()
                if data["title"] != "" and data["month"][0] != "-":
                    text = f"{data["title"]}\n{data["month"]} {data["date"]}"
                    item = QListWidgetItem(text)
                    self.reminderList.addItem(item)
                    break

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error! Invalid Data!")
                msg.setText("The data you've entered is invalid!")
                msg.exec()
            elif status == QDialog.Rejected:
                break

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

    def _onReminderSelectionChange(self):
        if not self.reminderList.selectedItems():
            return

        self.deleteReminderButton.show()

    def _onTaskDoubleClicked(self, item):
        newText, ok = QInputDialog().getText(self, "Edit Task", "Task: ",
                                             text=item.text())

        if ok:
            item.setText(newText)

    def _onReminderDoubleClicked(self, item):
        title = item.text().split("\n")

        time = title[1].split(" ")
        title = title[0]

        dialog = ReminderDialog()
        dialog.setData({
            "title": title,
            "month": time[0],
            "date": int(time[1])
        })

        while True:
            status = dialog.exec()
            if status == QDialog.Accepted:
                data = dialog.getData()
                if data["title"] != "" and data["month"][0] != "-":
                    text = f"{data["title"]}\n{data["month"]} {data["date"]}"
                    item.setText(text)
                    break

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error! Invalid Data!")
                msg.setText("The data you've entered is invalid!")
                msg.exec()
            elif status == QDialog.Rejected:
                break

    def _onDeleteTaskButtonPressed(self):
        items = self.taskList.selectedItems()
        for item in items:
            self.taskList.takeItem(self.taskList.row(item))

        self.deleteTaskButton.hide()
        self.taskList.clearSelection()

    def _onDeleteReminderButtonPressed(self):
        items = self.reminderList.selectedItems()
        for item in items:
            self.reminderList.takeItem(self.reminderList.row(item))

        self.deleteReminderButton.hide()
        self.reminderList.clearSelection()


if __name__ == "__main__":
    app = QApplication([])
    win = MynWindow()
    win.show()
    app.exec()
