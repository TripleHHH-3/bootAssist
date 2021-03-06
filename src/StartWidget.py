import os

import win32api
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QWidget
from PySide2.QtWidgets import QFileDialog

from src import BgProgram
from src.BgProgram import BgProgramDialog
from src.ui.StartWidget_UI import Ui_Form


class StartWidget(QWidget, Ui_Form):

    def __init__(self):
        # 初始化
        super().__init__()
        self.setupUi(self)

        filePath, fileName = os.path.split(BgProgramDialog.tempPath)
        if not os.path.exists(filePath):
            os.makedirs(filePath)

        self.init()

        self.lastFocusTable = self.storeTable

    def init(self):
        # 初始化已保存的路径
        self.__initTableWidget(self.storeTable)
        self.__initTableWidget(self.startTable)

        # 安装监听
        self.startTable.installEventFilter(self)
        self.storeTable.installEventFilter(self)

        self.storeTable.setFocus()

    def eventFilter(self, obj, event):
        """给两个table添加焦点监听"""
        if obj == self.storeTable:
            if event.type() == QtCore.QEvent.Type.FocusIn:
                self.lastFocusTable = obj
                self.rightMoveBtn.setEnabled(True)
                self.leftMoveBtn.setEnabled(False)

        if obj == self.startTable:
            if event.type() == QtCore.QEvent.Type.FocusIn:
                self.lastFocusTable = obj
                self.leftMoveBtn.setEnabled(True)
                self.rightMoveBtn.setEnabled(False)

        return super(StartWidget, self).eventFilter(obj, event)

    def start(self):
        with open(self.startTable.property("filePath"), "r+", encoding="utf-8") as file:
            for line in file:
                win32api.ShellExecute(0, 'open', line.rstrip("\n"), '', '', 0)

    def readBg(self):
        dialog = BgProgramDialog()
        dialog.appListSignal.connect(self.bgAppHandle)
        dialog.exec_()
        dialog.appListSignal.disconnect(self.bgAppHandle)
        dialog.deleteLater()

    def bgAppHandle(self, appList):
        for filePath in appList:
            self.__pathInsertFileAndTable(self.lastFocusTable, filePath)

    def delFilePath(self):
        self.__delPathInFile(self.lastFocusTable)
        self.lastFocusTable.setFocus()

    def __delPathInFile(self, table):
        if len(table.selectedItems()) == 0:
            return

        text = table.selectedItems()[1].text() + "\n"
        with open(table.property("filePath"), "r+", encoding="utf-8") as file:
            readlines = file.readlines()
            if text in readlines:
                readlines.remove(text)
            file.seek(0)
            file.truncate()
            file.writelines(readlines)

        table.removeRow(table.selectedItems()[1].row())

    # 保存文件路径
    def saveFilePath(self):
        # 获取文件路径
        filePath, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择你要启动的程序",  # 标题
            r"d:\\data",  # 起始目录
            "程序类型 (*.exe)"  # 选择类型过滤项，过滤内容在括号中
        )

        if filePath != "":
            self.__pathInsertFileAndTable(self.lastFocusTable, filePath)

    def __pathInsertFileAndTable(self, table, filePath):
        """把路径写入文件和插入table"""

        # 判断两个table是否已存在路径
        for row in range(self.storeTable.rowCount()):
            item = self.storeTable.item(row, 1)
            if item.text() == filePath:
                self.storeTable.selectRow(row)
                self.storeTable.setFocus()
                return

        for row in range(self.startTable.rowCount()):
            item = self.startTable.item(row, 1)
            if item.text() == filePath:
                self.startTable.selectRow(row)
                self.startTable.setFocus()
                return

        # 写入文件
        with open(table.property("filePath"), "a", encoding="utf-8") as file:
            file.write(filePath + "\n")

        # 插入table
        self.__pathInsertTable(table, filePath)

    def __initTableWidget(self, tableWidget):
        """初始化table控件，即从文件中读出路径渲染到table"""

        if os.path.isfile(tableWidget.property("filePath")):
            with open(tableWidget.property("filePath"), "r+", encoding="utf-8") as file:
                for index, line in enumerate(file.readlines()):
                    self.__pathInsertTable(tableWidget, line, index)
        else:
            filePath, fileName = os.path.split(tableWidget.property("filePath"))
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            open(tableWidget.property("filePath"), 'w').close()

    def __pathInsertTable(self, tableWidget, path, row=-1):
        if row < 0:
            row = tableWidget.rowCount()

        tableWidget.insertRow(row)
        # 填充名字与图标
        item = QTableWidgetItem(BgProgram.getIconFromPath(path.strip("\n")), os.path.split(path)[1][:-5])
        tableWidget.setItem(row, 0, item)
        # 填充程序路径
        tableWidget.setItem(row, 1, QTableWidgetItem(path.strip('\n')))

    def rightMove(self):
        self.__writeAndMove(self.storeTable, self.startTable)

    def leftMove(self):
        self.__writeAndMove(self.startTable, self.storeTable)

    def __writeAndMove(self, formTable, toTable):
        """把程序路径从table移动到另一个table，包括table单元格和txt的数据"""

        items = formTable.selectedItems()

        if len(items) == 0:
            QMessageBox.information(self, "提示", "请选择程序", QMessageBox.Ok)
            return

        path = items[1].text()
        self.__delPathInFile(formTable)
        self.__pathInsertFileAndTable(toTable, path)


if __name__ == "__main__":
    app = QApplication([])
    startWidget = StartWidget()
    startWidget.show()
    app.exec_()
