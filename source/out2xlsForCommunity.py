#!usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:51211 
@file: out2xlsForSale.py
@time: 2017/07/07
"""
import requests
import xlsxwriter
from bs4 import BeautifulSoup

from source.community_item import HouseItem


# 根据县区名字找到下面街道或者镇的url链接
def find_sub_link_by_region_name(param_url):
    global headers
    response = requests.get(url=param_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    region_items = soup.select('body > div.w1180 > div.div-border.items-list > div:nth-of-type(1)')
    children = region_items[0].contents
    region_items_details = children[2]
    selected_region = region_items_details.find("a", class_="selected-item")
    param_region_name = selected_region.string
    sub_items = region_items_details.find("div", class_="sub-items")
    sub_items_list = sub_items.find_all("a", class_="")
    # print(sub_items_list)
    param_sub_items_dict = {}
    for item in sub_items_list:
        print(item.string.strip())
        print(item['href'])
        param_sub_items_dict[item.string.strip()] = item['href']
    return param_region_name, param_sub_items_dict


# 从当前页上把房产信息添加到house_items列表上
def add2house_items_from_one_page():
    global item_index
    global is_has_next
    soup = BeautifulSoup(sub_response.text, 'html.parser')
    house_list = soup.select('#list-content > div.li-itemmod')
    is_has_next = len(soup.find_all("a", class_="aNxt"))
    for item in house_list:
        item_index = item_index + 1
        print("**********************" + str(item_index) + "**************************")
        children = item.contents
        div_item_img = children[1]
        img_src = div_item_img.contents[1]['src']

        div_house_details = children[3]
        div_details_item = div_house_details

        community_list_title = div_details_item.contents[1].find("a").string
        adress = div_details_item.contents[3].string.strip()
        completion_date = div_details_item.contents[5].contents[0].strip().split('：')[1]
        second_hand_housing_for_sale = div_details_item.contents[7].contents[1].find("a").string[1:-1]
        if len(children[5].contents[1].contents) > 1:
            unit_price = children[5].contents[1].contents[1].string + '元/平米'
        else:
            unit_price = '暂无均价'
        price_change = children[5].contents[3].contents[0]

        # 构造item实例
        house_item = HouseItem(img_src, community_list_title, adress, completion_date, second_hand_housing_for_sale,
                               unit_price, price_change)
        house_item.my_print()
        house_items.append(house_item)


# 根据城镇名在xls添加sheet
def add_sheet_by_town_name(param_key):
    ws = wb.add_worksheet(param_key)
    ws.set_column('A:A', 23)
    ws.set_column('B:B', 34)
    ws.set_column('C:C', 10)
    ws.set_column('D:D', 11)
    ws.set_column('E:E', 14)
    ws.set_column('F:F', 10)
    i = 0
    while i < len(house_items) + 1:
        if i == 0:
            # 小区名称：%s\n地址：%s\n竣工日期：%s\n二手房数量：%s\n平均地价：%s\n涨幅
            ws.write(i, 0, '小区名称', )
            ws.write(i, 1, '地址', )
            ws.write(i, 2, '竣工日期', )
            ws.write(i, 3, '二手房数量', )
            ws.write(i, 4, '平均地价', )
            ws.write(i, 5, '涨幅', )
        else:
            # community_list_title, address, completion_date,second_hand_housing_for_sale, unit_price, price_change
            ws.write(i, 0, house_items[i - 1].community_list_title, )
            ws.write(i, 1, house_items[i - 1].address, )
            ws.write(i, 2, house_items[i - 1].completion_date, )
            ws.write(i, 3, house_items[i - 1].second_hand_housing_for_sale, )
            ws.write(i, 4, house_items[i - 1].unit_price, )
            ws.write(i, 5, house_items[i - 1].price_change, )
        i = i + 1


# 根据县区名创建xls
def add_workbook_by_region_name(param_region_name):
    global wb, house_items, item_index, is_has_next, sub_response
    wb = xlsxwriter.Workbook('../house_sale_xls/' + param_region_name + '小区.xls')
    for key in sub_items_dict.keys():
        print(key)
        sub_url = sub_items_dict[key] + 'p%s'
        print(sub_url)
        page_index = 1
        house_items = []
        item_index = 0
        is_has_next = 0
        while True:
            sub_response = requests.get(url=sub_url % str(page_index), headers=headers)
            print('page_index=' + str(page_index))
            add2house_items_from_one_page()
            page_index = page_index + 1
            if is_has_next == 0:
                break

        print(len(house_items))

        add_sheet_by_town_name(key)
    wb.close()


if __name__ == '__main__':
    url = 'https://suzhou.anjuke.com/community/changshua/'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
                 '59.0.3071.115 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
    }
    region_name, sub_items_dict = find_sub_link_by_region_name(url)
    print(region_name)
    print(sub_items_dict.keys())

    add_workbook_by_region_name(region_name)
