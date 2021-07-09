import os
import subprocess

from PySide2.QtGui import QIcon, QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QApplication, QMessageBox, QAbstractItemView
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog
from PIL import Image
import win32ui
import win32gui


class MainWindows:

    def __init__(self):
        self.ui = QUiLoader().load('../resource/ui/mainWindows.ui')

        self.clear_space()

        # 初始化
        self.init()

        # 槽连接
        self.ui.addBtn.clicked.connect(self.saveFilePath)
        self.ui.deleteBtn.clicked.connect(self.deleteFilePath)
        self.ui.LToRBtn.clicked.connect(self.leftToRight)
        self.ui.RToLBtn.clicked.connect(self.rightToLeft)
        self.ui.startBtn.clicked.connect(self.recover)

    def getImg(self, exePath):
        ico_x = 32
        ico_y = 32

        large, small = win32gui.ExtractIconEx(exePath, 0)
        useIcon = large[0]
        destroyIcon = small[0]
        win32gui.DestroyIcon(destroyIcon)

        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
        hdc = hdc.CreateCompatibleDC()

        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), useIcon)

        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (32, 32),
            bmpstr, 'raw', 'BGRA', 0, 1
        )

        path = '../resource/img/' + os.path.basename(exePath).replace('.exe', '.png')
        img.save(path)

        item = QStandardItem()
        icon = QIcon(path)
        item.setIcon(QIcon(icon))
        return item

    # 保存文件路径
    def saveFilePath(self):
        # 获取文件路径
        filePath, _ = QFileDialog.getOpenFileName(
            self.ui,  # 父窗口对象
            "选择你要启动的程序",  # 标题
            r"d:\\1111",  # 起始目录
            "程序类型 (*.exe)"  # 选择类型过滤项，过滤内容在括号中
        )

        # 路径写入文件
        with open("../resource/config/path.txt", "a+", encoding="utf-8") as file:
            file.seek(0)
            rowPosition = l_model.rowCount()
            num = 0
            if file.read().strip() == "":
                file.write(filePath + "\n")
                l_model.setItem(rowPosition, 2, QStandardItem(str(filePath)))
                l_model.setItem(rowPosition, 0, self.getImg(filePath.replace("\n", "")))
                l_model.setItem(rowPosition, 1, QStandardItem(os.path.basename(filePath)))
                num = 1
            file.seek(0)
            for line in file:
                # 已存在路径则提示
                if line.strip() != '':
                    if line.replace("\n", "") == filePath and num == 0:
                        num = 2
                        QMessageBox.information(self.ui, "提示", "已经存在相同的程序", QMessageBox.Ok)
                        break
                    else:
                        pass
            if num == 0:
                file.write(filePath + "\n")
                l_model.setItem(rowPosition, 2, QStandardItem(str(filePath)))
                l_model.setItem(rowPosition, 0, self.getImg(filePath.replace("\n", "")))
                l_model.setItem(rowPosition, 1, QStandardItem(os.path.basename(filePath)))

    # 删除文件路径
    def deleteFilePath(self):
        row = self.ui.preTableView.selectionModel().currentIndex().row()
        item = self.ui.preTableView.model().index(row, 2).data()
        with open("../resource/config/path.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open("../resource/config/path.txt", "w", encoding="utf-8") as newFile:
            for line in lines:
                if item != line.replace("\n", ""):
                    newFile.write(line)
            l_model.takeRow(row)

    # 消除文件空行
    def clear_space(self):
        with open("../resource/config/path.txt", 'r', encoding='utf-8') as old_path:
            pre_lines = old_path.readlines()
        with open("../resource/config/path.txt", 'w+', encoding='utf-8') as new_path:
            for line in pre_lines:
                if line.split():
                    new_path.write(line)
        with open("../resource/config/realPath.txt", 'r', encoding='utf-8') as old_realPath:
            start_lines = old_realPath.readlines()
        with open("../resource/config/realPath.txt", 'w+', encoding='utf-8') as new_realPath:
            for line in start_lines:
                if line.split():
                    new_realPath.write(line)

    # 向右传导
    def leftToRight(self):
        row = self.ui.preTableView.selectionModel().currentIndex().row()
        item = self.ui.preTableView.model().index(row, 2).data()

        rowPosition = r_model.rowCount()
        # 右边文件添加
        with open("../resource/config/realPath.txt", "a+", encoding="utf-8") as newFile:
            r_model.setItem(rowPosition, 2, QStandardItem(str(item)))
            r_model.setItem(rowPosition, 0, self.getImg(item))
            r_model.setItem(rowPosition, 1,
                            QStandardItem(os.path.basename(item)))
            newFile.write("\n"+item)

        # 左边文件路径删除
        with open("../resource/config/path.txt", "r", encoding="utf-8") as left_old:
            l_old = left_old.readlines()
        with open("../resource/config/path.txt", "w+", encoding="utf-8") as left_new:
            for l in l_old:
                if item != l.replace("\n", "") and l != "":
                    left_new.write(l + "\n")
            l_model.takeRow(row)

    # 向左传导
    def rightToLeft(self):
        row = self.ui.startTableView.selectionModel().currentIndex().row()
        item = self.ui.startTableView.model().index(row, 2).data()

        rowPosition = l_model.rowCount()
        # 左边文件添加
        with open("../resource/config/path.txt", "a+", encoding="utf-8") as newFile:
            l_model.setItem(rowPosition, 2, QStandardItem(str(item)))
            l_model.setItem(rowPosition, 0, self.getImg(item))
            l_model.setItem(rowPosition, 1,
                            QStandardItem(os.path.basename(item)))
            l_model.appendRow(r_model.item(row))
            # for i in 3:
                # l_model.setItem(rowPosition, i, self.ui.startTableView.model().index(row, i).data())
            newFile.write("\n"+item)

        # 右边文件路径删除
        with open("../resource/config/realPath.txt", "r", encoding="utf-8") as right_old:
            r_old = right_old.readlines()
        with open("../resource/config/realPath.txt", "w+", encoding="utf-8") as right_new:
            for r in r_old:
                if item != r.replace("\n", ""):
                    right_new.write(r + "\n")
            r_model.takeRow(row)

    def iniTableView(self):
        global l_model
        l_model = QStandardItemModel()
        ls = ['图标', '名称', '路径']
        l_model.setHorizontalHeaderLabels(ls)
        l_model.setColumnCount(3)
        self.ui.preTableView.setModel(l_model)
        self.ui.preTableView.horizontalHeader().setVisible(True)
        self.ui.preTableView.setColumnWidth(0, 40)
        self.ui.preTableView.setColumnWidth(1, 100)
        self.ui.preTableView.setColumnWidth(2, 300)
        self.ui.preTableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.preTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.preTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        global r_model
        r_model = QStandardItemModel()
        r_model.setHorizontalHeaderLabels(ls)
        r_model.setColumnCount(3)
        self.ui.startTableView.setModel(l_model)
        self.ui.startTableView.horizontalHeader().setVisible(True)
        self.ui.startTableView.setColumnWidth(0, 40)
        self.ui.startTableView.setColumnWidth(1, 100)
        self.ui.startTableView.setColumnWidth(2, 300)
        self.ui.startTableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.startTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.startTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        return l_model, r_model

    def init(self):
        # 初始化已保存的路径
        l_model, r_model = self.iniTableView()

        with open("../resource/config/path.txt", "r+", encoding="utf-8") as file:
            prePosition = 0
            for line in file:
                print("1    "+line)
                if not line.isspace():
                    l_model.setItem(prePosition, 0, self.getImg(line.replace("\n", "")))
                    l_model.setItem(prePosition, 1,
                                    QStandardItem(os.path.basename(line.replace("\n", ""))))
                    l_model.setItem(prePosition, 2, QStandardItem(str(line.replace("\n", ""))))
                    self.ui.preTableView.setModel(l_model)
                    prePosition = prePosition + 1

        with open("../resource/config/realPath.txt", "r+", encoding="utf-8") as file:
            startPosition = 0
            for line in file:
                print("2    " + line)
                if not line.isspace():
                    r_model.setItem(startPosition, 2, QStandardItem(str(line.replace("\n", ""))))
                    r_model.setItem(startPosition, 0, self.getImg(line.replace("\n", "")))
                    r_model.setItem(startPosition, 1,
                                    QStandardItem(os.path.basename(line.replace("\n", ""))))
                    self.ui.startTableView.setModel(r_model)
                    startPosition = startPosition + 1

    def recover(self):
        temp_str = ""
        with open("../resource/config/realPath.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        p = ''
        for i in lines:
            if i.isspace() != True:
                temp_str = temp_str + "start \"\" \"" + i.replace("\n", "") + "\"" + "\n"

                p = subprocess.Popen(i.replace("\n", ""));
        p.wait()


if __name__ == "__main__":
    app = QApplication([])
    stats = MainWindows()
    stats.ui.show()
    app.exec_()
