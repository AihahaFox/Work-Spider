#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-12 13:35:07
# @Author  : Aihahafox (644015664@qq.com)
# @Link    : http://aihahafox.sinaapp.com
# @Version : $1.0$

import sys
import urllib2
from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")


def getHtml(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, fromEncoding="gb18030")
    return soup


def findWorkInfo(soup):
    tdResult = soup.findAll('td', attrs={"class": "td1"})
    content = ''
    for td in tdResult:
        content = content + td.text + '&'
    return content


def findWorkCom(soup):
    tdResult = soup.findAll('td', attrs={"class": "td2"})
    content = ''
    for td in tdResult:
        content = content + td.text + '&'
    return content


def findWorkPlace(soup):
    tdResult = soup.findAll('td', attrs={"class": "td3"})
    content = ''
    for td in tdResult:
        content = content + td.text + '&'
    return content


def findWorkTime(soup):
    tdResult4 = soup.findAll('td', attrs={"class": "td4"})
    content = ''
    for td in tdResult4:
        content = content + td.text + '&'
    return content


def getContent(content):
    node = '&'
    userList = []
    while content.strip():
        now = content[0: content.find(node)]
        userList.append(now)
        content = content[content.find(node)+1:]
    return userList


def getWorkDetailHtml(soup):
    detailHtml = []
    tdResult = soup.findAll('td', attrs={"class": "td1"})
    for td in tdResult:
        aArray = td.findAll('a')
        for a in aArray:
            detailHtml.append(a.get('href'))
    return detailHtml


def getDetailBaseInfo(detailHtml):
    detailBaseInfo = []
    soup = getHtml(detailHtml)
    tableArray = soup.findAll('table', attrs={"class": "jobs_1"})
    tdArray = tableArray[0].findAll('td')
    jobName = tdArray[0].text
    companyName = tdArray[2].findAll('a')[0].text
    description = getDescription(tdArray[4].text)
    detailBaseInfo.append(jobName)
    detailBaseInfo.append(companyName)
    detailBaseInfo.append(description)
    return detailBaseInfo


def getDescription(description):
    x = '公司性质'
    y = '公司规模'
    node = '&nbsp;'
    result = description.replace(node, ' ')
    result = result[0: result.find(x)] + '\n' + result[result.find(x):]
    result = result[0: result.find(y)] + '\n' + result[result.find(y):]
    return result


def getDetailInfo(detailHtml):
    content1 = ''
    content2 = ''
    result = []
    soup = getHtml(detailHtml)
    tableArray = soup.findAll('table', attrs={"class": "jobs_1"})
    tdArray = tableArray[2].findAll('td')
    td1 = tableArray[2].findAll('td', attrs={"class": "job_detail"})
    td2 = tableArray[2].findAll('td', attrs={"class": "txt_4 wordBreakNormal job_detail "})
    for i in range(0, 12):
        if (i + 1) % 6 == 0:
            content1 = content1 + tdArray[i].text.replace('&nbsp;', '') + '\n'
        elif (i + 1) % 2 == 0:
            content1 = content1 + tdArray[i].text.replace('&nbsp;', '') + '     '
        else:
            content1 = content1 + tdArray[i].text.replace('&nbsp;', '')
    for i in td1:
        content2 = content2 + i.text.replace('&nbsp;', '') + '\n'
    content3 = getContent3(td2[0].text.replace('&nbsp;', ''))
    result.append(content1)
    result.append(content2)
    result.append(content3)
    return result


def getContent3(content):
    #for x in ['：', '；', '。', ':', ';']:
    content1 = content.replace(':', ':\n')
    content2 = content1.replace(';', ';\n')
    content3 = content2.replace('：', '：\n')
    content4 = content3.replace('；', '；\n')
    result = content4.replace('。', '。\n')
    return result
