import json

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QInputDialog,
    QDialog,
    QListWidgetItem,
    QMessageBox,
    QFileDialog,
    QWidget,
    QVBoxLayout,
    QLabel
)


def extractDataFromReminderItem(reminderItem) -> tuple:
    title = reminderItem.text().split("\n")
    time = title[1].split(" ")
    title = title[0]

    return (title, time[0], int(time[1]))


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
        self.invalidMsg = QMessageBox()
        self.aboutAppMsg = QMessageBox()

        self.aboutCreator = QWidget()

    def _configureComponents(self):
        self.deleteTaskButton.hide()
        self.deleteReminderButton.hide()

        self.invalidMsg.setIcon(QMessageBox.Icon.Warning)
        self.invalidMsg.setWindowTitle("Error! Invalid Data!")
        self.invalidMsg.setText("The data you've entered is invalid!")

        self.aboutAppMsg.setIcon(QMessageBox.Icon.Information)
        self.aboutAppMsg.setWindowTitle("About App")
        self.aboutAppMsg.setText("Just Do It v0.0.1")

        creatorLayout = QVBoxLayout()
        creatorLayout.addWidget(QLabel("Dzakanov Inshoofi"))
        creatorLayout.addWidget(QLabel("F1D02310110"))
        self.aboutCreator.setLayout(creatorLayout)
        self.aboutCreator.setWindowTitle("About Creator")
        self.aboutCreator.setFixedSize(128, 72)

    def _setupCallbacks(self):
        self.actionOpen.triggered.connect(self._onOpenTriggered)
        self.actionSave.triggered.connect(self._onSaveTriggered)
        self.actionExit.triggered.connect(lambda: self.close())

        self.actionAboutApp.triggered.connect(lambda: self.aboutAppMsg.show())
        self.actionAboutCreator.triggered.connect(
            lambda: self.aboutCreator.show())

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

    def _onOpenTriggered(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Open JDT File", "", "JDT Files (*.jdt);; All Files (*)")

        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)

                for task in data["taskList"]:
                    item = QListWidgetItem(task["title"])
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(
                        Qt.Checked if task["checked"] else Qt.Unchecked)

                    self.taskList.addItem(item)

                for reminder in data["reminderList"]:
                    item = QListWidgetItem(f"{reminder["title"]}\n{
                                           reminder["month"]} {reminder["date"]}")
                    self.reminderList.addItem(item)

    def _onSaveTriggered(self):
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Open JDT File", "", "JDT Files (*.jdt);; All Files (*)")
        if file_path:
            if not file_path.endswith(".jdt"):
                file_path += ".jdt"

            taskItems: list = []

            for i in range(self.taskList.count()):
                item = self.taskList.item(i)

                taskItems.append({
                    "checked": item.checkState() == Qt.CheckState.Checked,
                    "title": item.text()
                })

            reminderItems: list = []
            for i in range(self.reminderList.count()):
                item = self.reminderList.item(i)
                title, month, date = extractDataFromReminderItem(item)

                reminderItems.append({
                    "title": title,
                    "month": month,
                    "date": date
                })

            data = {
                "taskList": taskItems,
                "reminderList": reminderItems
            }

            with open(file_path, "w") as f:
                json.dump(data, f)

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

                self.invalidMsg.exec()
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
        title, month, date = extractDataFromReminderItem(item)

        dialog = ReminderDialog()
        dialog.setData({
            "title": title,
            "month": month,
            "date": date
        })

        while True:
            status = dialog.exec()
            if status == QDialog.Accepted:
                data = dialog.getData()
                if data["title"] != "" and data["month"][0] != "-":
                    text = f"{data["title"]}\n{data["month"]} {data["date"]}"
                    item.setText(text)
                    break

                self.invalidMsg.exec()
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
