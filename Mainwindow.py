#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-12 09:53:09
# @Author  : Aihahafox (644015664@qq.com)
# @Link    : http://aihahafox.sinaapp.com
# @Version : $1.0$
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from process import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class MainWindow(QDialog):
    """关于爬虫软件界面"""
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle(self.tr("工作爬虫"))
        self.URL = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&keyword="
        self.Page = "&curr_page="
        self.count = 1
        self.row = 0
        self.setFixedSize(1000, 600)
        #mainSplitter = QSplitter(Qt.Horizontal)
        #mainSplitter.setOpaqueResize(True)
        #frame = QFrame(mainSplitter)
        self.workTable = WorkTable()

        #welcomeLabel = QLabel(self.tr("欢迎使用职业爬虫！"))
        #self.quitButtton = QPushButton(self.tr("退出"))
        searchLabel = QLabel(self.tr("请输入您所想要搜索的职业"))
        searchButton = QPushButton(self.tr("搜索"))
        self.searchLineEdit = QLineEdit()
        #self.contentWeb = QWebView()
        #self.contentWeb.load(QUrl("http://www.baidu.com/"))
        self.preButton = QPushButton(self.tr("上一页"))
        self.nextButton = QPushButton(self.tr("下一页"))
        self.detailButton = QPushButton(self.tr("详情>>"))
        self.collectButton = QPushButton(self.tr("添加到收藏"))
        self.webButton = QPushButton(self.tr("查看原网页"))

        self.contentText = QTextEdit()
        self.contentText.setReadOnly(True)

        self.detailLabel = QLabel(self.tr("双击获取详细信息"))
        self.detailText = QTextEdit()
        self.detailWidget = QWidget()

        #self.connect(self.quitButtton, SIGNAL("clicked()"), self, SLOT("close()"))
        self.connect(searchButton, SIGNAL("clicked()"), self.prepare)
        self.connect(self.preButton, SIGNAL("clicked()"), self.prePage)
        self.connect(self.nextButton, SIGNAL("clicked()"), self.nextPage)
        self.connect(self.detailButton, SIGNAL("clicked()"), self.slotExtension)
        self.connect(self.workTable, SIGNAL("cellDoubleClicked (int, int)"), self.more)
        self.connect(self.collectButton, SIGNAL("clicked()"), self.collect)
        self.connect(self.webButton, SIGNAL("clicked()"), self.webPage)

#设置界面布局
        hLayout = QHBoxLayout()
        hLayout.setSpacing(10)
        hLayout.addWidget(searchLabel)
        hLayout.addWidget(self.searchLineEdit)
        hLayout.addWidget(searchButton)

        bLayout = QGridLayout()
        bLayout.addWidget(self.preButton, 0, 0)
        bLayout.addWidget(self.nextButton, 0, 1)
        #bLayout.addWidget(self.quitButtton, 1, 0)
        #bLayout.addWidget(self.detailButton, 1, 1)

        baseLayout = QVBoxLayout()
        baseLayout.setMargin(10)
        baseLayout.addLayout(hLayout)
        baseLayout.addWidget(self.workTable)
        baseLayout.addLayout(bLayout)
        baseLayout.addWidget(self.detailButton)

        detailLayout = QVBoxLayout(self.detailWidget)
        detailLayout.addWidget(self.detailLabel)
        detailLayout.addWidget(self.detailText)
        detailLayout.addWidget(self.collectButton)
        detailLayout.addWidget(self.webButton)
        self.detailWidget.hide()

        #mainLayout = QHBoxLayout(frame)
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(baseLayout)
        mainLayout.addWidget(self.detailWidget)
        mainLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        mainLayout.setSpacing(5)

        #layout = QHBoxLayout(self)
        #layout.addWidget(mainSplitter)
        self.setLayout(mainLayout)

        QThread.sleep(3)

    def prepare(self):
        self.count = 1
        self.search()

    def search(self):
        self.workTable.clear()
        value = self.searchLineEdit.text()
        self.mySoup = getHtml(str(self.URL + value + self.Page + str(self.count)))
        workList = getContent(findWorkInfo(self.mySoup))
        companyList = getContent(findWorkCom(self.mySoup))
        placeList = getContent(findWorkPlace(self.mySoup))
        timeList = getContent(findWorkTime(self.mySoup))
        for work in workList:
            self.workTable.insertRow(self.row)
            self.workTable.insertItem(work, self.row, 0)
            self.row = self.row + 1
        self.row = 0
        for company in companyList:
            self.workTable.insertItem(company, self.row, 1)
            self.row = self.row + 1
        self.row = 0
        for place in placeList:
            self.workTable.insertItem(place, self.row, 2)
            self.row = self.row + 1
        self.row = 0
        for time in timeList:
            self.workTable.insertItem(time, self.row, 3)
            self.row = self.row + 1
        self.workTable.resizeColumnsToContents()
        self.row = 0
        #self.contentText.setText(QString(content))

    def slotExtension(self):
        if self.detailWidget.isHidden():
            self.detailWidget.show()
        else:
            self.detailWidget.hide()

    def more(self):
        self.detailText.clear()
        self.currentRow = self.workTable.currentRow()
        if self.currentRow == 0:
            return -1
        self.htmlList = getWorkDetailHtml(self.mySoup)
        res1 = getDetailBaseInfo(self.htmlList[self.currentRow-1])
        res2 = getDetailInfo(self.htmlList[self.currentRow-1])
        for i in res1:
            self.detailText.append(i)
        for i in res2:
            self.detailText.append(i)

    def prePage(self):
        if self.count == 1:
            return 0
        self.count = self.count - 1
        self.search()

    def nextPage(self):
        self.count = self.count + 1
        self.search()

    def collect(self):
        fp = open("content.txt", 'a')
        fp.write(self.detailText.toPlainText())
        fp.write("\n####################\n")
        #print self.detailText.toPlainText()
        fp.close()
        QMessageBox.information(self, "Information", self.tr("添加到收藏成功！"))

    def webPage(self):
        web = WebPage()
        web.contentWeb.load(QUrl(self.htmlList[self.currentRow-1]))
        web.show()
        web.exec_()


class WorkTable(QTableWidget):
    """显示搜索结果的简略内容"""
    def __init__(self, parent=None):
        super(WorkTable, self).__init__()
        self.setColumnCount(4)
        #self.setRowCount(50)
#设置表格不可编辑
        noEditTriggers = QAbstractItemView.NoEditTriggers
        self.setEditTriggers(noEditTriggers)
#设置表格整行选择
        self.setSelectionBehavior(QTableWidget.SelectRows)
#设置表头隐藏
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
#根据内容自动调整列宽
        #self.resizeColumnsToContents()
#设置隔行改变颜色
        self.setAlternatingRowColors(True)
#选择单行
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def insertItem(self, content, row, col):
        self.setItem(row, col, QTableWidgetItem(content))


class WebPage(QDialog):
    """docstring for WebPage"""
    def __init__(self, parent=None):
        super(WebPage, self).__init__(parent)
        self.contentWeb = QWebView()
        self.cancelButton = QPushButton(self.tr("返回"))

        self.connect(self.cancelButton, SIGNAL("clicked()"), self, SLOT("close()"))

        layout = QVBoxLayout()
        layout.addWidget(self.contentWeb)
        layout.addWidget(self.cancelButton)

        self.setLayout(layout)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     splash = QSplashScreen(QPixmap("image/Welcom.png"))
#     splash.show()
#     app.processEvents()
#     main = MainWindow()
#     main.show()
#     splash.finish(main)
#     app.exec_()
