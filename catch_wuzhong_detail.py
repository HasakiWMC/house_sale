#!usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:51211 
@file: catch_wuzhong_detail.py 
@time: 2017/07/02 
"""
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'https://suzhou.anjuke.com/sale/yuanqu/'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
                 '59.0.3071.115 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    region_items = soup.select('html body #container #content > div.div-border.items-list > div:nth-of-type(1)')
    children = region_items[0].contents
    region_items_details = children[1]
    selected_region = region_items_details.find("span", class_="selected-item")
    region = selected_region.string

    sub_items = region_items_details.find("div", class_="sub-items")
    sub_items_list = sub_items.find_all("a")
    print(sub_items_list)



