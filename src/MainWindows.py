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
        self.ui.pushButton.clicked.connect(self.saveFilePath)

    # 保存文件路径
    def saveFilePath(self):
        # 获取文件路径
        filePath, _ = QFileDialog.getOpenFileName(
            self.ui,  # 父窗口对象
            "选择你要启动的程序",  # 标题
            r"d:\\data",  # 起始目录
            "程序类型 (*.exe)"  # 选择类型过滤项，过滤内容在括号中
        )

        # filePath != "" ,表明未选择文件
        if filePath != "":
            # 路径写入文件
            with open("../resource/config/path.txt", "a+", encoding="utf-8") as file:
                file.seek(0)
                for line in file:
                    # 已存在路径则提示
                    if line == filePath + "\n":
                        QMessageBox.information(self.ui, "提示", "已经存在相同的程序", QMessageBox.Ok)
                        break
                else:
                    file.write(filePath + "\n")
                    self.ui.listWidget.addItem(filePath)

    def init(self):
        # 初始化已保存的路径
        with open("../resource/config/path.txt", "r+", encoding="utf-8") as file:
            for index, line in enumerate(file):
                self.ui.appStoreTable.insertRow(index)
                # 填充名字与图标
                item = QTableWidgetItem(os.path.split(line)[1].strip(".exe\n"))
                item.setIcon(self.getIconFromPath(line))
                self.ui.appStoreTable.setItem(index, 0, item)
                # 填充程序路径
                self.ui.appStoreTable.setItem(index, 1, QTableWidgetItem(line.strip('\n')))

    def getIconFromPath(self, filePath):
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


if __name__ == "__main__":
    app = QApplication([])
    stats = MainWindows()
    stats.ui.show()
    app.exec_()
