# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StartWidget_UI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1000, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(1000, 600))
        Form.setMaximumSize(QSize(1000, 600))
        self.addBtn = QPushButton(Form)
        self.addBtn.setObjectName(u"addBtn")
        self.addBtn.setGeometry(QRect(370, 240, 75, 23))
        self.storeTable = QTableWidget(Form)
        if (self.storeTable.columnCount() < 2):
            self.storeTable.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.storeTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.storeTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.storeTable.setObjectName(u"storeTable")
        self.storeTable.setGeometry(QRect(50, 120, 261, 231))
        self.storeTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.storeTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.storeTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.storeTable.horizontalHeader().setVisible(True)
        self.storeTable.horizontalHeader().setStretchLastSection(True)
        self.delBtn = QPushButton(Form)
        self.delBtn.setObjectName(u"delBtn")
        self.delBtn.setGeometry(QRect(370, 280, 75, 23))
        self.startTable = QTableWidget(Form)
        if (self.startTable.columnCount() < 2):
            self.startTable.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.startTable.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.startTable.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        self.startTable.setObjectName(u"startTable")
        self.startTable.setGeometry(QRect(520, 120, 261, 231))
        self.startTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.startTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.startTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.startTable.horizontalHeader().setStretchLastSection(True)
        self.rightMoveBtn = QPushButton(Form)
        self.rightMoveBtn.setObjectName(u"rightMoveBtn")
        self.rightMoveBtn.setEnabled(False)
        self.rightMoveBtn.setGeometry(QRect(370, 140, 75, 23))
        self.leftMoveBtn = QPushButton(Form)
        self.leftMoveBtn.setObjectName(u"leftMoveBtn")
        self.leftMoveBtn.setEnabled(False)
        self.leftMoveBtn.setGeometry(QRect(370, 180, 75, 23))
        self.readBgBtn = QPushButton(Form)
        self.readBgBtn.setObjectName(u"readBgBtn")
        self.readBgBtn.setGeometry(QRect(370, 320, 75, 23))

        self.retranslateUi(Form)
        self.delBtn.clicked.connect(Form.delFilePath)
        self.addBtn.clicked.connect(Form.saveFilePath)
        self.rightMoveBtn.clicked.connect(Form.rightMove)
        self.leftMoveBtn.clicked.connect(Form.leftMove)
        self.readBgBtn.clicked.connect(Form.readBg)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        Form.setProperty("filePath", QCoreApplication.translate("Form", u"../resource/config/startPath.txt", None))
        self.addBtn.setText(QCoreApplication.translate("Form", u"\uff0b", None))
        ___qtablewidgetitem = self.storeTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u7a0b\u5e8f", None));
        ___qtablewidgetitem1 = self.storeTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u8def\u5f84", None));
        self.storeTable.setProperty("filePath", QCoreApplication.translate("Form", u"../resource/config/storePath.txt", None))
        self.delBtn.setText(QCoreApplication.translate("Form", u"\uff0d", None))
        ___qtablewidgetitem2 = self.startTable.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u7a0b\u5e8f", None));
        ___qtablewidgetitem3 = self.startTable.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"\u8def\u5f84", None));
        self.startTable.setProperty("filePath", QCoreApplication.translate("Form", u"../resource/config/startPath.txt", None))
        self.rightMoveBtn.setText(QCoreApplication.translate("Form", u">>>", None))
        self.leftMoveBtn.setText(QCoreApplication.translate("Form", u"<<<", None))
        self.readBgBtn.setText(QCoreApplication.translate("Form", u"\u8bfb\u53d6\u540e\u53f0", None))
    # retranslateUi

