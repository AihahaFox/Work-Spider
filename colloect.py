#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-27 11:57:13
# @Author  : Aihahafox (644015664@qq.com)
# @Link    : http://aihahafox.sinaapp.com
# @Version : $1.0$
from PyQt4.QtGui import *
from PyQt4.QtCore import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class CollectWidget(QDialog):
    """docstring for CollectWidget"""
    def __init__(self, parent=None):
        super(CollectWidget, self).__init__(parent)
        self.count = 0
        self.index = 0
        self.a = []
        self.setFixedSize(1000, 600)
        self.listWidget = QListWidget()
        self.findList()

        for i in range(0, self.index):
            self.a.append(0)
        self.stack = QStackedWidget()
        self.addStack(self.index)
        self.refreshButton = QPushButton(self.tr("更新"))
        self.deleteButton = QPushButton(self.tr("删除"))

        buttom = QHBoxLayout()
        buttom.addWidget(self.refreshButton)
        buttom.addWidget(self.deleteButton)

        right = QVBoxLayout()
        right.addWidget(self.stack)
        right.addLayout(buttom)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.listWidget)
        mainLayout.addLayout(right)
        mainLayout.setStretchFactor(self.listWidget, 1)
        mainLayout.setStretchFactor(right, 3)
        self.setLayout(mainLayout)

        self.connect(self.listWidget, SIGNAL("currentRowChanged(int)"), self.stack, SLOT("setCurrentIndex(int)"))
        self.connect(self.refreshButton, SIGNAL("clicked()"), self.refresh)
        self.connect(self.deleteButton, SIGNAL("clicked()"), self.delete)

    def findList(self):
        fp = open("content.txt")
        for eachLine in fp:
            if self.count == 0:
                self.listWidget.insertItem(self.index, self.tr(eachLine))
                self.count += 1
                self.index += 1
            if eachLine == "####################\n":
                self.count = 0
        fp.close()

    def addStack(self, index):
        fp = open("content.txt")
        for i in range(0, index):
            # exec("self.text" + str(i) + " = QTextEdit()")
            # eval("self.text" + str(i)).clear()
            # eval("self.text" + str(i)).setReadOnly(True)
            self.text = QTextEdit()
            self.text.clear()
            self.text.setReadOnly(True)
            for eachLine in fp:
                if eachLine != "####################\n":
                    #eval("self.text" + str(i)).append(self.tr(eachLine))
                    self.text.append(self.tr(eachLine))
                else:
                    if self.a[i] == 0:
                        self.stack.insertWidget(i, self.text)
                        #self.stack.addWidget(eval("self.text" + str(i)))
                        self.a[i] = 1
                    break
        fp.close()

    def refresh(self):
        self.listWidget.clear()
        #self.stack.clear()
        self.index = 0
        self.findList()
        for i in range(len(self.a), self.index):
            self.a.append(0)
        self.addStack(self.index)

    def delete(self):
        fp = open("content.txt")
        temp = fp.readlines()
        fp.close()
        fp = open("content.txt", 'w')
        i = 0
        index = []
        for line in temp:
            if line == "####################\n":
                index.append(i)
            i += 1
        if self.listWidget.currentRow() == 0:
            del temp[0: index[self.listWidget.currentRow()]+1]
        else:
            del temp[index[self.listWidget.currentRow()-1]: index[self.listWidget.currentRow()]]
        for line in temp:
            fp.write(line)
        fp.close()
        del self.a[self.index-1]
        for i in range(0, self.index-1):
            self.a[i] = 0
        self.refresh()
