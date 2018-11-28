"""
    爬取目标
    + 爬取豆瓣评分Top250的图书
    + 获取每本图书的详细信息
    + 把爬取结果存入Excel中
    https://book.douban.com/top250?start=0
    爬取豆瓣图书评分最高的前250本，
    第一页：start=0，第二页：start=25......
"""
# coding:utf-8

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import xlwt
from fake_useragent import UserAgent
from time import sleep


class DoubanBook:
    def __init__(self, pageIndex):
        self.pageIndex = 0

        # # 普通访问
        # self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
        #                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        # self.headers = {'User-Agent': self.user_agent}

        # 随意变换headers
        self.ua = UserAgent()
        self.headers = {'User-Agent': self.ua.random}

        print(self.headers)

        self.book_list = []

    # 获取每页网址的源码
    def getPage(self):
        try:
            url = 'https://book.douban.com/top250?start=' + str(self.pageIndex)
            request = Request(url, headers=self.headers)
            response = urlopen(request)
            page = response.read().decode('utf-8')
            return page
        except URLError as e:
            if hasattr(e, 'reason'):
                print("爬取失败，失败原因：", e.reason)

    def getBooks(self):
        pageCode = self.getPage()
        bsObj = BeautifulSoup(pageCode, 'lxml')
        for book in bsObj.findAll("td", {"valign": "top"}):
            # 判断是否是需要的信息，用于去除图片处代码信息
            if book.find('div',{'class':re.compile(r'pl[2]{1}')})==None:
                continue

            # 获取图书链接
            bookUrl = book.a['href'].strip()
            # 获取图书标题
            title = book.a['title'].strip()
            # 获取图书原作名
            title_src = re.compile(r'<span style="font-size:12px;">(.*?)</span>')
            title_src_item = re.findall(title_src, str(book))

            # 获取图书详情
            detail = book.find('p',{'class':'pl'}).get_text().split('/')
            # 获取作者author、译者translator、出版社press、出版时间date、价格price
            author = detail[0].strip()
            if len(detail)==5:
                translator = detail[1].strip()
                press = detail[2].strip()
                date = detail[3].strip()
                price = detail[4].strip()
            else:
                translator = ''
                press = detail[1].strip()
                date = detail[2].strip()
                price = detail[3].strip()

            # 获取豆瓣评分
            score = book.find('span',{'class':'rating_nums'}).get_text().strip()
            # 获取评分人数
            scoreNum = book.find('span',{'class':'pl'}).get_text().strip('(').strip(')').strip()
            # 获取图书引述
            if book.find('span',{'class':'inq'}) == None:
                quote = ''
            else:
                quote = book.find('span',{'class':'inq'}).get_text().strip()
            self.book_list.append([title,title_src_item,author,translator,press,date,price,score,scoreNum,quote,bookUrl])
            print(title, quote)
            # 反爬虫暂停
            sleep(1)

    def load(self,datalist):
        file = xlwt.Workbook()
        sheet = file.add_sheet('豆瓣图书Top250',cell_overwrite_ok=True)
        col = (u'图书名字',u'原作名',u'作者',u'译者',u'出版社',u'出版时间',u'价格',u'评分',u'评价人数',u'引述',u'图书豆瓣链接')
        for i in range(0,11):
            sheet.write(0,i,col[i]) #列名
        for i in range(0,250):
            data = datalist[i]
            for j in range(0,11):
                sheet.write(i+1,j,data[j])    #数据
        file.save('豆瓣图书Top250.xls')

    def start(self):
        print('现开始抓取豆瓣图书Top250的数据：')
        while self.pageIndex<=225:
            print('----现抓取第%d页----'% (self.pageIndex/25+1))
            self.getBooks()
            self.pageIndex+=25
        print("----抓取完成----")
        self.load(self.book_list)


book = DoubanBook(0)
book.start()