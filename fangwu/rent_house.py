import requests

from bs4 import BeautifulSoup

import pymysql

import re

import headers

import ip_proxy


def get_page(url):
    response = requests.get(url, headers=headers.requests_headers(), proxies=ip_proxy.ip_proxy())

    # 通过BeautifulSoup进行解析出每个房源详细列表并进行打印
    soup_idex = BeautifulSoup(response.text, 'html.parser')
    result_li = soup_idex.find_all('div', {'class': 'zu-itemmod'})

    # 进行循环遍历其中的房源详细列表
    for i in result_li:
        # 由于BeautifulSoup传入的必须为字符串，所以进行转换
        page_url = str(i)
        soup = BeautifulSoup(page_url, 'html.parser')
        # 由于通过class解析的为一个列表，所以只需要第一个参数
        result_href = soup.find_all('a', {'class': 'img'})[0]
        # 详细页面的函数调用
        get_page_detail(result_href.attrs['href'])

    # 进行下一页的爬取
    result_next_page = soup_idex.find_all('a', {'class': 'aNxt'})
    if len(result_next_page) != 0:
        # 函数进行递归
        get_page(result_next_page[0].attrs['href'])
    else:
        print('没有下一页了')


# 进行字符串中空格，换行，tab键的替换及删除字符串两边的空格删除
def my_strip(s):
    return str(s).replace(" ", "").replace("\n", "").replace("\t", "").strip()


# 由于频繁进行my_beautiful_soup的使用，封装一下，很鸡肋
def my_beautiful_soup(response):
    return BeautifulSoup(str(response), 'html.parser')


# 详细页面的爬取
def get_page_detail(url):
    response = requests.get(url, headers=headers.requests_headers(), proxies=ip_proxy.ip_proxy())
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 房间标签
        house_title = soup.find_all('h3', {'class': 'house-title'})

        # 房间标签
        house_label = soup.find_all('ul', {'class': 'title-label cf'})

        # 房屋编码和发布时间
        house_release_time = soup.find_all('div', {'class': 'right-info'})

        # 房屋信息
        house_info = soup.find_all('ul', {'class': 'house-info-zufang cf'})

        # 房间配套
        house_matching = soup.find_all('ul', {'class': 'house-info-peitao cf'})
        # 房间概述
        house_summary = soup.find_all('div', {'class': 'auto-general'})

        # 平台
        channel = '安居客'
        # 房子id
        house_id = get_house_id(url)
        cur.execute('select * from rent_house where house_id = %s', (str(house_id)))
        values = cur.fetchall()

        if values:
            return []

        # 标题
        title = my_strip(house_title[0].text)

        # 价格
        house_price = my_strip(house_info[0].contents[1].contents[1].text).replace("元/月", "")
        # 交押金方式
        house_rent_day = my_strip(house_info[0].contents[1].contents[3].text)
        # # 房屋多少
        house_number = my_strip(house_info[0].contents[3].text).replace("户型：", "")
        # 房子面积
        house_size = my_strip(house_info[0].contents[5].text).replace("面积：", "").replace("平方米", "")
        # 所在楼层
        house_floor = my_strip(house_info[0].contents[9].text).replace("楼层：", "")
        # 装修
        house_renovation = my_strip(house_info[0].contents[11].text).replace("装修：", "")
        # 类型
        house_type = my_strip(house_info[0].contents[13].text).replace("类型：", "")

        # 小区
        house_residential_areas = my_strip(house_info[0].contents[15].contents[3].text)

        # 区域
        house_areas = my_strip(house_info[0].contents[15].contents[5].text)

        # 具体区域
        house_sub_areas = my_strip(house_info[0].contents[15].contents[7].text)

        # 租房类型
        if house_label[0].contents[1]:
            rent_type = my_strip(house_label[0].contents[1].text)
        else:
            rent_type = ''

        # 房屋朝向
        if house_label[0].contents[3]:
            house_orientation = my_strip(house_label[0].contents[3].text)
        else:
            house_orientation = ''

        # 临近地铁沿线
        if house_label[0].contents[5]:
            house_subway = my_strip(house_label[0].contents[5].text)
        else:
            house_subway = ''

        # 房屋编码和发布时间
        release_time = my_strip(house_release_time[0].text)

        # 房间配套信息
        if house_matching:
            matching = my_strip(house_matching[0].text)
        else:
            matching = ''

        # 房间概述
        summary = my_strip(house_summary[0].text)

        cur.execute(
            'insert into rent_house(channel,house_id,title,price,rent_day,number,size,floor,renovation,type,'
            'residential_areas,areas,sub_areas,rent_type,orientation,subway,release_time,matching,summary) '
            'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (
                channel, house_id, title, house_price, house_rent_day, house_number, house_size, house_floor,
                house_renovation, house_type, house_residential_areas, house_areas, house_sub_areas, rent_type,
                house_orientation, house_subway, release_time, matching, summary))

        conn.commit()


# 正则获取房屋id
def get_house_id(url):
    re1 = '.*?'  # Non-greedy match on filler
    re2 = '(\\d+)'  # Integer Number 1

    rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
    m = rg.search(url)
    if m:
        house_id = m.group(1)

    return house_id


if __name__ == '__main__':
    # 連接mysql
    conn = pymysql.connect(host='172.16.12.46', user='root', password='lW5711947', db='python', charset='utf8')
    cur = conn.cursor()
    # url链接
    url = 'https://wh.zu.anjuke.com/'
    # 页面爬取函数调用
    get_page(url)

    cur.close()
    conn.close()
