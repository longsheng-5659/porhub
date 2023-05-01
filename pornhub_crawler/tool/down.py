import datetime
import random
import requests
import execjs
import pymysql
import re
import json
import time
from bs4 import BeautifulSoup
def xxx():
    db = pymysql.Connect(host="120.25.161.159", user="videohub", password="MHHaiO3UKBASaZxC3Ov", port=3306, database="videohub", autocommit=True)
    # db = pymysql.Connect('120.25.161.159', 'test', '数据库名', '表名')
    cursor = db.cursor()

    # sql1 = "select * from video"
    #
    # cursor.execute(sql1)
    # rest = cursor.fetchall()
    # for i in rest:
    #     print(i)
    # db.close()
    #
    #

    category = ["热门", "电影"]
    tag = ["国产"]
    for page in range(1):
        page += 1
        url = 'https://jp.pornhub.com'
        url_page = url + '/video?page=' + str(page)
        # print(url_page)
        html = requests.get(url_page)
        # print(html.text)
        # soup = BeautifulSoup(html.text, 'lxml')
        soup = BeautifulSoup(html.text, 'html.parser')

        li = soup.find_all('li')
        for i in li:
            if i.img and i.button:
                try:
                    href = url + i.a['href']
                    print(i.a['href'])
                    # 获取链接地址
                    html1 = requests.get(href)
                    soup1 = BeautifulSoup(html1.text, 'html.parser')

                    pattern = re.compile(r'var (.*?);', re.MULTILINE | re.DOTALL)
                    script = soup1.findAll("script", string=pattern)
                    videoUrl = ""
                    for x in script:
                        # 找到有视频链接的script
                        m3u8 = re.findall("m3u8", x.text)
                        if len(m3u8) != 0:
                            pat = r'(.*?)var nextVideoPlaylistObject'
                            # 获取js代码
                            script1 = re.findall(pat, x.text, re.S)
                            # print(script1)
                            # 编译js代码
                            js_compiled = execjs.compile(script1[0])
                            # eval 是获取js变量
                            videoUrl = js_compiled.eval('media_2')
                            print(videoUrl)
                            break

                    poster = i.img["src"]
                    description = i.img["alt"]
                    title = i.a['title']
                    var = i.find_all('var')
                    # time, visitor, release_time = var[0].string, var[1].string, var[2].string
                    time, release_time = var[0].string, var[2].string
                    Rating_rate = i.find_all('div')[-1].string

                    create_time = int(datetime.datetime.now().timestamp()*1000)
                    # 观看人数
                    visitor = random.randint(1000000, 10000000000)
                    id = int(datetime.datetime.now().timestamp()*100)
                    vid = "V"+str(int(random.random()*10000))
                    uid = int(random.random()*10000)
                    data = {"videoSrc": videoUrl, "videoHref": href}
                    sources = json.dumps(data)

                    # INSERT
                    # INTO
                    # video
                    # (id, vid, uid, title, poster, description, sources, category, tag, visitor, create_time)
                    # VALUES(6, 'V6', 24531, '闪电侠',
                    #        'https://pic3.zhimg.com/80/v2-0c2ab2347118f8e743cf1678608230ba_720w.webp',
                    #        '跳票多年的《闪电侠》肩负重任，它将会回溯DC宇宙的历史，利用平行宇宙的概念，改变整个原定世界观的历史，开启DC电影多元宇宙',
                    #        '{"test": "http://media.w3.org/2010/05/video/movie_300.webm", "bunnyMovie": "http://media.w3.org/2010/05/bunny/movie.mp4", "bunnyTrailer": "http://media.w3.org/2010/05/bunny/trailer.mp4", "sintelTrailer": "http://media.w3.org/2010/05/sintel/trailer.mp4"}',
                    #        '热门', '国产', 116800, 1679845967000);

                    # sql = "INSERT INTO video \
                    # (id, vid, uid, title, poster, description, sources, category, tag, visitor, create_time) \
                    # VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                    #       (id, vid, uid, title, poster, description, sources, random.choice(category),
                    #        random.choice(tag), visitor, create_time)
                    sql = "INSERT INTO video \
                    ( vid, uid, title, poster, description, sources, category, tag, visitor, create_time) \
                    VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                          (vid, uid, title, poster, description, sources, random.choice(category),
                           random.choice(tag), visitor, create_time)

                    try:
                        cursor.execute(sql)
                        # db.commit()
                    except Exception as e:
                        print(e)
                    finally:
                        print('视频标题：' + title)
                        print('视频链接：' + href)
                        print('视频图片：' + poster)
                        print('视频描述：' + description)
                        print('视频描述：' + random.choice(category))
                        print('时长：' + time)
                        # print('当前观看总量：' )
                        print('点赞率：' + Rating_rate)
                        print('发布时间：' + release_time)
                        print('--------------------------')
                except Exception as e:
                    print(e)
        print('当前已经爬取到了第' + str(page) + '页千！')
    db.close()

if __name__ == '__main__':
    xxx()