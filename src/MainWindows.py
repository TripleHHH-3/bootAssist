import os

import win32gui
import win32ui
from PIL import Image
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PySide2.QtWidgets import QFileDialog


class MainWindows:

    def __init__(self):
        self.ui = QUiLoader().load('../resource/ui/mainWindows.ui')

        # 初始化
        self.init()

        # 槽连接
        self.ui.addBtn.clicked.connect(self.saveFilePath)
        self.ui.rightMoveBtn.clicked.connect(self.rightMove)

    # 保存文件路径
    def saveFilePath(self):
        # 获取文件路径
        filePath, _ = QFileDialog.getOpenFileName(
            self.ui,  # 父窗口对象
            "选择你要启动的程序",  # 标题
            r"d:\\data",  # 起始目录
            "程序类型 (*.exe)"  # 选择类型过滤项，过滤内容在括号中
        )

        # filePath != "" ,即未选择文件
        if filePath != "":
            # 路径写入文件
            if self.__pathWriteInFile("../resource/config/path.txt", filePath):
                self.__pathInsertTable(self.ui.storeTable.rowCount(), filePath)

    def __pathWriteInFile(self, filePath, content):
        with open(filePath, "a+", encoding="utf-8") as file:
            file.seek(0)
            for line in file:
                # 已存在路径则提示
                if line == content + "\n":
                    QMessageBox.information(self.ui, "提示", "已经存在相同的程序", QMessageBox.Ok)
                    return False
            else:
                file.write(content + "\n")
                return True

    def init(self):
        # 初始化已保存的路径
        with open("../resource/config/path.txt", "r+", encoding="utf-8") as file:
            readlines = file.readlines()
            for index, line in enumerate(readlines):
                self.__pathInsertTable(index, line)

    def __pathInsertTable(self, row, path):
        self.ui.storeTable.insertRow(row)
        # 填充名字与图标
        item = QTableWidgetItem(self.__getIconFromPath(path.strip("\n")), os.path.split(path)[1].strip(".exe\n"))
        self.ui.storeTable.setItem(row, 0, item)
        # 填充程序路径
        self.ui.storeTable.setItem(row, 1, QTableWidgetItem(path.strip('\n')))

    def __getIconFromPath(self, filePath):
        large, small = win32gui.ExtractIconEx(filePath, 0)
        win32gui.DestroyIcon(small[0])
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), large[0])
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (32, 32),
            bmpstr, 'raw', 'BGRA', 0, 1
        )

        img.save('../resource/temp/temp.png')
        icon = QIcon("../resource/temp/temp.png")
        os.remove("../resource/temp/temp.png")
        return icon

    def rightMove(self):
        self.__writeAndMove(self.ui.storeTable, self.ui.startTable)

    def __writeAndMove(self, formTable, toTable):
        items = formTable.selectedItems()
        colCount = formTable.columnCount()
        # 把单个的单元格list切片成以每行为单位的单元格list
        itemRowList = [items[i:i + colCount] for i in range(0, len(items), colCount)]

        # 打开fromTable的txt后续备用
        fromFile = open(formTable.property("filePath"), "w+", encoding="utf-8")

        # 遍历每一行单元格
        for itemList in itemRowList:
            text = itemList[-1].text()
            # 文件路径保存到toTable.txt后再插入toTable
            if self.__pathWriteInFile(toTable.property("filePath"), text):

                # 从formTable.txt删除选中的文件路径
                readlines = fromFile.readlines()
                if text + '\n' in readlines:
                    readlines.remove(text + "\n")
                fromFile.writelines(readlines)

                # 遍历复制每个单元格到toTable
                rowCount = toTable.rowCount()
                toTable.insertRow(rowCount)
                for index, item in enumerate(itemList):
                    toTable.setItem(rowCount, index, item.clone())

                # 从formTable删除选中行
                formTable.removeRow(itemList[-1].row())

        fromFile.close()


if __name__ == "__main__":
    app = QApplication([])
    stats = MainWindows()
    stats.ui.show()
    app.exec_()
