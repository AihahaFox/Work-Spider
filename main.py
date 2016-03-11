#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-27 10:55:16
# @Author  : Aihahafox (644015664@qq.com)
# @Link    : http://aihahafox.sinaapp.com
# @Version : $1.0$

from Mainwindow import *
from colloect import *


class Main(QDialog):
    """docstring for Main"""
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setFixedSize(1050, 700)
        self.mainWindow = MainWindow()
        self.collectWidget = CollectWidget()
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.mainWindow, self.tr("主页面"))
        self.tabWidget.addTab(self.collectWidget, self.tr("收藏"))
        self.cancelButton = QPushButton(self.tr("退出"))
        self.buttomLabel = QLabel(self.tr("version 1.0"))
        self.blank = QLabel()

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.buttomLabel)
        buttonLayout.addWidget(self.blank)
        buttonLayout.addWidget(self.cancelButton)

        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(self.cancelButton, SIGNAL("clicked()"), self, SLOT("close()"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("image/Welcom.png"))
    splash.show()
    app.processEvents()
    main = Main()
    main.show()
    splash.finish(main)
    app.exec_()
