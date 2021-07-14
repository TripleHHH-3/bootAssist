import psutil
import win32gui
import win32process
from PySide2 import QtCore
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QApplication, QDialog, QTreeWidgetItem, QTreeWidgetItemIterator

from src import StartWidget
from src.ui.BgProgramDialog_UI import Ui_Dialog


class BgProgramDialog(QDialog, Ui_Dialog):
    ignoreList = ["SystemSettings.exe", "explorer.exe", "ApplicationFrameHost.exe", "TextInputHost.exe"]
    appListSignal = Signal(list)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init()

    def init(self):
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setColumnWidth(0, 150)
        self.treeWidget.setHeaderLabels(['程序', '路径'])

        hwnd_title = dict()
        win32gui.EnumWindows(get_all_hwnd, hwnd_title)

        duplicationSet = set()
        for h, t in hwnd_title.items():
            if t != "":
                thread_id, process_id = win32process.GetWindowThreadProcessId(h)
                process = psutil.Process(process_id)
                if (process.name() not in BgProgramDialog.ignoreList) and (process.name() not in duplicationSet):
                    item = QTreeWidgetItem()
                    try:
                        item.setIcon(0, StartWidget.getIconFromPath(process.exe()))
                        item.setText(0, process.name()[:-4])
                        item.setText(1, process.exe())
                        item.setCheckState(0, QtCore.Qt.Checked)
                        self.treeWidget.insertTopLevelItem(0, item)
                        duplicationSet.add(process.name())
                    except:
                        print(process.name())
                        pass

    def accept(self):
        appList = []
        it = QTreeWidgetItemIterator(self.treeWidget, QTreeWidgetItemIterator.Checked)
        while it.value():
            appList.append(it.value().text(1).replace("\\", "/"))
            it.__next__()

        self.appListSignal.emit(appList)
        super().accept()


def get_all_hwnd(hwnd, dic):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        dic.update({hwnd: win32gui.GetWindowText(hwnd)})


if __name__ == "__main__":
    app = QApplication([])
    ui = BgProgramDialog()
    ui.show()
    app.exec_()
