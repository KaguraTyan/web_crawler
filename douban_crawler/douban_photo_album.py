"""
    爬取目标
    + 爬取豆瓣XX相册
    + 把爬取图片保存本地
    https://www.douban.com/photos/album/31237087/?start=
    爬取豆瓣相册并保存图片至本地，
    第一页：start=0，第二页：start=25......
"""
# coding:utf-8

import re
import urllib.request
import urllib.error
import time


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'}
            '''发出请求'''
            request = urllib.request.Request(url=url, headers=header)
            '''获取结果'''
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        if response.getcode() != 200:
            return None
        html = response.read()
        response.close()
        return html


class Image(object):
    def ImageGet(self, imageurl, image_path):
        for li in imageurl:
            # print(li)
            image_name = li.split('/')[-1].split('.')[0]
            # print(image_name)
            urllib.request.urlretrieve(li, image_path % image_name)
            # '''休眠1s以免给服务器造成严重负担'''
            # time.sleep(1)


'''起始URL'''
pageIndex =0

# 1242为最大pageIndex，根据相册页数来定义
while pageIndex <= 1242:
    print('----现抓取第%d页----'% (pageIndex/18+1))

    url = 'https://www.douban.com/photos/album/31237087/?start=' + str(pageIndex)
    # print(url)
    '''保存目录'''
    image_path = r'photo\%s.jpg'
    '''定义实体类'''
    downloader = HtmlDownloader()
    html = downloader.download(url)
    '''SaveFile(html, html_path)'''
    html = html.decode('utf-8')
    # print(html)
    '''正则表达式'''
    reg1 = r'(https://img[\S]*?view/photo/m/public.*?.jpg)'
    # reg1 = r'="(https://img[\S]*?[jpg|png])'''
    '''提取图片的URL'''
    dbdata = re.findall(reg1, html)
    # print(dbdata)
    imgsave = Image()

    '''下载保存图片'''
    imgsave.ImageGet(dbdata, image_path)

    pageIndex += 18

    '''休眠1s以免给服务器造成严重负担'''
    time.sleep(1)

print('Finish')