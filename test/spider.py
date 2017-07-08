#!usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:51211 
@file: spider.py 
@time: 2017/07/01 
"""

import requests
import xlsxwriter
from bs4 import BeautifulSoup

from source.sale_item import HouseItem


def house_list2xls(region, town, house_items):
    # 设置字体风格
    # style0 = xlsxwriter.easyxf('font: name Times New Roman, color-index blue, bold on', num_format_str='#,##0.00')
    # style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    # 打开excel，添加sheet
    wb = xlsxwriter.Workbook(region + '.xls')
    ws = wb.add_worksheet(town)
    ws.set_column('A:A', 60)
    ws.set_column('D:D', 15)
    ws.set_column('E:E', 13)
    ws.set_column('F:F', 44)
    ws.set_column('H:H', 11)
    # 写入文本

    i = 0
    while i < len(house_items) + 1:
        if i == 0:
            ws.write(i, 0, '房产标题', )
            ws.write(i, 1, '几室几厅', )
            ws.write(i, 2, '面积', )
            ws.write(i, 3, '楼层', )
            ws.write(i, 4, '建成时间', )
            ws.write(i, 5, '地理位置', )
            ws.write(i, 6, '总价', )
            ws.write(i, 7, '均价', )
        else:
            ws.write(i, 0, house_items[i - 1].house_list_title, )
            ws.write(i, 1, house_items[i - 1].structure, )
            ws.write(i, 2, house_items[i - 1].area, )
            ws.write(i, 3, house_items[i - 1].floor, )
            ws.write(i, 4, house_items[i - 1].time, )
            ws.write(i, 5, house_items[i - 1].address, )
            ws.write(i, 6, house_items[i - 1].price_det, )
            ws.write(i, 7, house_items[i - 1].unit_price, )
        i = i + 1
    wb.close()


def add2house_items_from_one_page():
    global house_item
    global item_index
    global is_has_next
    soup = BeautifulSoup(response.text, 'html.parser')
    house_list = soup.select('html body #container div #houselist-mod-new li')
    is_has_next = len(soup.find_all("a", class_="aNxt"))

    for item in house_list:
        item_index = item_index + 1
        print("**********************" + str(item_index) + "**************************")
        children = item.contents
        div_item_img = children[1]
        img_src = div_item_img.contents[1]['src']

        div_house_details = children[3]
        div_house_title = div_house_details.contents[1]

        house_list_title = div_house_title.contents[1]['title']
        div_details_item = div_house_details.contents[3]

        structure = div_details_item.contents[1].string
        area = div_details_item.contents[3].string
        floor = div_details_item.contents[5].string
        time = div_details_item.contents[7].string

        div_details_item2 = div_house_details.contents[5]
        address = div_details_item2.contents[1]['title']

        div_pro_price = children[5]
        price_det = div_pro_price.contents[1].contents[0].string + '万'
        unit_price = div_pro_price.contents[2].string

        # 构造item实例
        house_item = HouseItem(img_src, house_list_title, structure, area, floor, time, address, price_det, unit_price)
        house_item.my_print()
        house_items.append(house_item)

        # 下载图片
        # r = requests.get(img_src, stream=True)  # here we need to set stream = True parameter
        # with open("pic/" + str(x) + '.jpg', 'wb') as f:
        #     for chunk in r.iter_content(chunk_size=1024):
        #         if chunk:  # filter out keep-alive new chunks
        #             f.write(chunk)
        #             f.flush()
        #     f.close()


if __name__ == '__main__':
    url = 'https://suzhou.anjuke.com/sale/guoxiang/p%s'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
                 '59.0.3071.115 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
    }
    page_index = 1
    house_items = []
    item_index = 0
    is_has_next = 0
    while True:
        response = requests.get(url=url % str(page_index), headers=headers)
        print('page_index=' + str(page_index))
        add2house_items_from_one_page()
        page_index = page_index + 1
        if is_has_next == 0:
            break

    print(len(house_items))
    house_list2xls('吴中', '郭巷', house_items)
