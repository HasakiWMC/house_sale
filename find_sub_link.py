#!usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:51211 
@file: find_sub_link.py
@time: 2017/07/02 
"""
import requests
from bs4 import BeautifulSoup


def find_sub_link_by_region_name(param_url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
                 '59.0.3071.115 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(url=param_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    region_items = soup.select('html body #container #content > div.div-border.items-list > div:nth-of-type(1)')
    children = region_items[0].contents
    region_items_details = children[1]
    selected_region = region_items_details.find("span", class_="selected-item")
    param_region_name = selected_region.string
    sub_items = region_items_details.find("div", class_="sub-items")
    sub_items_list = sub_items.find_all("a")
    # print(sub_items_list)
    param_sub_items_dict = {}
    for item in sub_items_list:
        # print(item.string)
        # print(item['href'])
        param_sub_items_dict[item.string] = item['href']
    return param_region_name, param_sub_items_dict


if __name__ == '__main__':
    url = 'https://suzhou.anjuke.com/sale/jinchang/'
    region_name, sub_items_dict = find_sub_link_by_region_name(url)
    print(region_name)
    print(sub_items_dict)
