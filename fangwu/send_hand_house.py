import requests

from bs4 import BeautifulSoup

import pymysql

import re

from django.utils.http import urlquote

# 网页的请求头
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}


def get_page(url):
    response = requests.get(url, headers=header)

    # 通过BeautifulSoup进行解析出每个房源详细列表并进行打印
    soup_idex = BeautifulSoup(response.text, 'html.parser')
    result_li = soup_idex.find_all('li', {'class': 'list-item'})

    # 进行循环遍历其中的房源详细列表
    for i in result_li:
        # 由于BeautifulSoup传入的必须为字符串，所以进行转换
        page_url = str(i)
        soup = BeautifulSoup(page_url, 'html.parser')
        # 由于通过class解析的为一个列表，所以只需要第一个参数
        result_href = soup.find_all('a', {'class': 'houseListTitle'})[0]
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
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 房屋编码和发布时间
        base_house_info = soup.find_all('h4', {'class': 'block-title houseInfo-title'})

        # 房子卖点
        result_house_explain = soup.find_all('div', {'class': 'houseInfo-item-desc'})

        # 房子基本信息
        result_house_where = soup.find_all('li', {'class': 'houseInfo-detail-item'})

        # 房子相关
        result_house_number = soup.find_all('span', {'class': 'info-tag'})

        # 平台
        channel = '安居客'
        # 房子id
        house_id = get_house_id(url)
        cur.execute('select * from second_hand_house where house_id = %s', (str(house_id)))
        values = cur.fetchall()

        if values:
            return []

        # 标题
        title = my_strip(soup.find_all('h3', {'class': 'long-title'})[0].text)

        # 价格
        price = my_strip(result_house_number[0].text).replace("万", "")

        # 住宅小区
        residential_areas = my_strip(result_house_where[0].text).replace("所属小区：", "")
        # 房屋多少
        house_number = my_strip(result_house_where[1].text).replace("房屋户型：", "")
        # 单价
        unit_price = my_strip(result_house_where[2].text).replace("房屋单价：", "").replace("元/m²", "")
        # 住址
        address = my_strip(result_house_where[3].text).replace("所在位置：", "")
        # 房子面积
        house_size = my_strip(result_house_where[4].text).replace("建筑面积：", "").replace("平方米", "")
        # 参考首付
        down_payment = my_strip(result_house_where[5].text).replace("参考首付：", "").replace("万", "")
        # 建造年代
        build_time = get_build_year(my_strip(result_house_where[6].text))
        # 房屋朝向
        house_orientation = my_strip(result_house_where[7].text).replace("房屋朝向：", "")
        # 所在楼层
        floor = my_strip(result_house_where[10].text).replace("所在楼层：", "")
        # 产权年限
        years_age = my_strip(result_house_where[12].text).replace("产权年限：", "").replace("年：", "")
        # 配套电梯
        is_elevator = my_strip(result_house_where[13].text).replace("配套电梯：", "")
        # 产权性质
        property_rights = my_strip(result_house_where[15].text).replace("产权性质：", "")
        # 唯一住房
        sole_housing = my_strip(result_house_where[16].text).replace("唯一住房：", "")

        # 卖点说明
        selling_point = my_strip(result_house_explain[0].text)
        # 房主说明
        master_description = my_strip(result_house_explain[1].text)
        # 小区说明
        house_description = my_strip(result_house_explain[2].text)

        # 发布时间
        release_time = my_strip(base_house_info[0].text)

        cur.execute(
            'insert into second_hand_house(channel,house_id,title,price,residential_areas,house_number,unit_price,'
            'address,house_size,down_payment,build_time,house_orientation,floor,years_age,is_elevator,property_rights,'
            'sole_housing,selling_point,master_description,house_description,release_time) '
            'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (
                channel, house_id, title, price, residential_areas, house_number, unit_price, address, house_size,

                down_payment, build_time, house_orientation, floor, years_age, is_elevator, property_rights,

                sole_housing, selling_point, master_description, house_description, release_time))

        conn.commit()


# 正则获取房屋id
def get_house_id(url):
    re1 = '.*?'  # Non-greedy match on filler
    re2 = '((?:[a-z][a-z]*[0-9]+[a-z0-9]*))'  # Alphanum 1

    rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
    m = rg.search(url)
    if m:
        house_id = m.group(1)

    return house_id


# 获取房屋id
def get_house_code(house_info):
    house_info = urlquote(house_info)
    re1 = '.*?'  # Non-greedy match on filler
    re2 = '\\d+'  # Uninteresting: int
    re3 = '.*?'  # Non-greedy match on filler
    re4 = '\\d+'  # Uninteresting: int
    re5 = '.*?'  # Non-greedy match on filler
    re6 = '\\d+'  # Uninteresting: int
    re7 = '.*?'  # Non-greedy match on filler
    re8 = '\\d+'  # Uninteresting: int
    re9 = '.*?'  # Non-greedy match on filler
    re10 = '\\d+'  # Uninteresting: int
    re11 = '.*?'  # Non-greedy match on filler
    re12 = '\\d+'  # Uninteresting: int
    re13 = '.*?'  # Non-greedy match on filler
    re14 = '\\d+'  # Uninteresting: int
    re15 = '.*?'  # Non-greedy match on filler
    re16 = '\\d+'  # Uninteresting: int
    re17 = '.*?'  # Non-greedy match on filler
    re18 = '\\d+'  # Uninteresting: int
    re19 = '.*?'  # Non-greedy match on filler
    re20 = '(\\d+)'  # Integer Number 1

    rg = re.compile(
        re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10 + re11 + re12 + re13 + re14 + re15 + re16 + re17 + re18 + re19 + re20,
        re.IGNORECASE | re.DOTALL)
    m = rg.search(house_info)
    if m:
        house_code = m.group(1)
    return house_code


def get_build_year(year):
    re1 = '.*?'  # Non-greedy match on filler
    re2 = '((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3})))(?![\\d])'  # Year 1

    rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
    m = rg.search(year)
    if m:
        build_time = m.group(1)
    return build_time


if __name__ == '__main__':
    # 連接mysql
    conn = pymysql.connect(host='172.16.12.46', user='root', password='lW5711947', db='python', charset='utf8')
    cur = conn.cursor()
    # url链接
    url = 'https://wuhan.anjuke.com/sale/'
    # 页面爬取函数调用
    get_page(url)

    cur.close()
    conn.close()
