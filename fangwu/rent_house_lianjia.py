from bs4 import BeautifulSoup
import requests
import pymongo
import time

import headers

import ip_proxy

client = pymongo.MongoClient('localhost', 27017)  # 链接数据库
ceshi = client['ceshi']
url_list = ceshi['url_list']
item_list = ceshi['item_info']
url_list1 = []

channel = 'https://bj.lianjia.com/zufang/dongcheng/'


# spider1 爬取房屋信息链接并用mongodb存储
def get_pages_url(channel, pag):
    url = str(channel + 'pg' + pag)
    wb_data = requests.get(url, headers=headers.requests_headers(), proxies=ip_proxy.ip_proxy())
    soup = BeautifulSoup(wb_data.text, 'lxml')
    time.sleep(1)
    no_data = '呣..没有找到相关内容，请您换个条件试试吧~'
    # 面包屑模块
    # 面包屑 breadcrumbs
    bread_crumbs = soup.select('#house-lst > li')
    item_url = soup.select('#house-lst > li > div > h2 > a')
    blank_url = str(soup.find(text=no_data))
    if no_data != blank_url:
        for url in item_url:
            url1 = url.get('href')
            url_list1.append(url1)
            # url_list.insert_one({'url':url1})
            print(url1)
    else:
        pass


# get_pages_url(channel,'2')
# spider2 爬取详细信息并用mongodb存储
def get_massages(url):
    web_data = requests.get(url, headers=requests_headers(), proxies=ip_proxy())
    soup = BeautifulSoup(web_data.text, 'lxml')
    title = (soup.title.text).split('|')[0]  # 房名
    address = soup.select('div.zf-room > p > a')[0].text  # 地址
    price = soup.select(' div.price > span.total')[0].text + '元'
    area = (soup.select('div.zf-room > p ')[0].text).split('：')[-1]
    home_url = url
    print({'title': title,
           'address': address,
           'price': price,
           'area': area,
           'home_url': home_url,
           })
    item_list.insert_one({'title': title,
                          'address': address,
                          'price': price,
                          'area': area,
                          'home_url': home_url})


get_massages('https://bj.lianjia.com/zufang/101101635089.html')
