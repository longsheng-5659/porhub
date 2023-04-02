from random import random

import requests
import datetime
import pymysql
from bs4 import BeautifulSoup
def xxx():
    # db = pymysql.Connect('你的ip', '用户名', '数据库名', '表名')
    # db = pymysql.Connect('120.25.161.159', 'test', '数据库名', '表名')
    # cursor = db.cursor()
    for page in range(1):
        page += 1
        url = 'https://jp.pornhub.com'
        url_page = url + '/video?page=' + str(page)
        print(url_page)
        html = requests.get(url_page)
        # print(html.text)
        # soup = BeautifulSoup(html.text, 'lxml')
        soup = BeautifulSoup(html.text, 'html.parser')
        li = soup.find_all('li')
        for i in li:
            if i.img and i.button:
                # print(i)
                try:
                    href = url + i.a['href']
                    poster  =   i.img["src"]
                    description  =   i.img["alt"]
                    title = i.a['title']
                    var = i.find_all('var')
                    time, visitor, release_time = var[0].string, var[1].string, var[2].string
                    Rating_rate = i.find_all('div')[-1].string
                    time_now = str(datetime.datetime.now())[:-7]
                    vid = "V"+str(int(random()*10000))
                    uid =   24531

                    # sql = "insert into pornhub (视频标题,时长,当前观看总量," \
                    #       "点赞率,发布时间,视频链接,抓取时间) VALUES ('%s','%s','%s','%s','%s','%s','%s')" \
                    #       % (title, time, looking, Rating_rate, release_time, href, time_now)
                    # cursor.execute(sql)
                    # db.commit()
                    print('视频标题：' + title)
                    print('视频链接：' + href)
                    print('视频图片：' + poster)
                    print('视频描述：' + description)
                    print('时长：' + time)
                    print('当前观看总量：' + visitor)
                    print('点赞率：' + Rating_rate)
                    print('发布时间：' + release_time)
                    print('--------------------------')
                except Exception:
                    pass
        print('当前已经爬取到了第' + str(page) + '页！')
    # db.close()

if __name__ == '__main__':
    xxx()