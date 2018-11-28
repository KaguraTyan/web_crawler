'''
    爬取百度百科中所有的子连接

'''
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random

'''
获取需要爬虫的网址
'''
base_url = "https://baike.baidu.com"
his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]


'''
选取'his'中最后一个值，输出网站的标题和url
'''
url = base_url + his[-1]
# 打开读取html
html = urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
# find只返回第一个'h1'，find_all返回所有'h1'
print(soup.find('h1').get_text(), '    url: ', his[-1])

# Find all sub_urls for baidu baike (item page), randomly select a sub_urls and store it in "his".
# If no valid sub link is found, than pop last url in "his".
'''
    查询百科网页内的所有的子链接sub_urls，随机选择sub_urls中的一个非0元素并存储在'his'中。
    如果没有找到有效的子链接,就pop返回上一个url于'his'中。
'''
sub_urls = soup.find_all("a", {"target": "_blank", "href": re.compile("/item/(%.{2})+$")})
# print(sub_urls)
# ex:[<a href="/item/%E4%B8%87%E7%BB%B4%E7%BD%91" target="_blank">万维网</a>,...]

if len(sub_urls) != 0:
    his.append(random.sample(sub_urls, 1)[0]['href'])
else:
    # no valid sub link found
    his.pop()
print(his)

his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]

for i in range(20):
    url = base_url + his[-1]

    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    print(i, soup.find('h1').get_text(), '    url: ', his[-1])

    # find valid urls
    sub_urls = soup.find_all("a", {"target": "_blank", "href": re.compile("/item/(%.{2})+$")})

    if len(sub_urls) != 0:
        his.append(random.sample(sub_urls, 1)[0]['href'])
    else:
        # no valid sub link found
        his.pop()