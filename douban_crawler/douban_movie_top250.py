"""
    爬取目标
    + 爬取豆瓣评分Top250的电影
    + 获取每部电影的详细信息
    + 把爬取结果存入Excel中
    https://movie.douban.com/top250
    爬取豆瓣电影评分最高的前250部，
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


class DoubanMovie:
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

        self.movie_list = []

    # 获取每页网址的源码
    def getPage(self):
        try:
            url = 'https://movie.douban.com/top250?start=' + str(self.pageIndex)
            request = Request(url, headers=self.headers)
            response = urlopen(request)
            page = response.read().decode('utf-8')
            return page
        except URLError as e:
            if hasattr(e, 'reason'):
                print("爬取失败，失败原因：", e.reason)

    def getMovies(self):
        pageCode = self.getPage()
        bsObj = BeautifulSoup(pageCode, 'lxml')
        for movie in bsObj.findAll("div", {"class": "info"}):

            # 获取链接
            movieUrl = movie.a['href'].strip()
            # 获取标题
            title = movie.a.find('span', attrs={'class': 'title'}).getText().strip()

            # 获取详情
            detail = movie.find('div', {'class': 'bd'}).p.getText()
            # 获取电影上映时间
            movieYear = re.findall(r'\d+', str(detail))[-1]
            # 获取电影所属国家
            country = detail.split('/')[-2]
            # 获取电影类型
            movieType = detail.split('/')[-1]

            # 获取豆瓣评分
            score = movie.find('span', attrs={'class': 'rating_num'}).getText()
            # 获取评分人数
            movieEval = movie.find('div', attrs={'class': 'star'})
            scoreNum = re.findall(r'\d+人评价', str(movieEval))[-1]

            # 得到电影的短评
            if movie.find('span',{'class':'inq'}) == None:
                quote = ''
            else:
                quote = movie.find('span',{'class':'inq'}).getText().strip()

            self.movie_list.append([title,movieYear,country,movieType,score,scoreNum,quote,movieUrl])
            print(title, quote)
            # 反爬虫暂停
            sleep(1)

    def load(self,datalist):
        file = xlwt.Workbook()
        sheet = file.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
        col = (u'电影名称',u'上映时间',u'制片国家/地区',u'类型',u'评分',u'评价人数',u'短评',u'豆瓣链接')
        for i in range(0,8):
            sheet.write(0,i,col[i]) #列名
        for i in range(0,250):
            data = datalist[i]
            for j in range(0,8):
                sheet.write(i+1,j,data[j])    #数据
        file.save('豆瓣电影Top250.xls')

    def start(self):
        print('现开始抓取豆瓣电影Top250的数据：')
        while self.pageIndex<=225:
            print('----现抓取第%d页----'% (self.pageIndex/25+1))
            self.getMovies()
            self.pageIndex+=25
        print("----抓取完成----")
        self.load(self.movie_list)


movie = DoubanMovie(0)
movie.start()