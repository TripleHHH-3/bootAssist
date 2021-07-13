import psutil
import win32gui
import win32process
from PySide2.QtWidgets import QTreeWidgetItem, QApplication, QDialog

from src.ui.BgProgramDialog_UI import Ui_Dialog


class BgProgramDialog(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init()

    def init(self):
        # self.treeWidget.setColumnCount(1)
        # self.treeWidget.addTopLevelItem(QTreeWidgetItem(self.treeWidget, "后台程序"))

        # 设置列数
        self.treeWidget.setColumnCount(2)
        # 设置树形控件头部的标题
        self.treeWidget.setHeaderLabels(['Key', 'Value'])

        # 设置根节点
        root = QTreeWidgetItem(self.treeWidget)
        root.setText(0, 'Root')

        # 设置子节点1
        child1 = QTreeWidgetItem()
        child1.setText(0, 'child1')
        child1.setText(1, 'ios')

        root.addChild(child1)

        hwnd_title = dict()
        win32gui.EnumWindows(get_all_hwnd, hwnd_title)

        for h, t in hwnd_title.items():
            if t != "":
                thread_id, process_id = win32process.GetWindowThreadProcessId(h)
                process = psutil.Process(process_id)
                print(process.exe())
                print(process.name())
        pass


def get_all_hwnd(hwnd, dic):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        dic.update({hwnd: win32gui.GetWindowText(hwnd)})


if __name__ == "__main__":
    app = QApplication([])
    ui = BgProgramDialog()
    ui.show()
    app.exec_()
