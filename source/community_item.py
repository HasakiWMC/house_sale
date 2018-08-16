#!usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:51211 
@file: community_item.py 
@time: 2017/07/08 
"""


class HouseItem(object):
    def __init__(self, img_src, community_list_title, address, completion_date,
                 second_hand_housing_for_sale, unit_price, price_change):
        self.img_src = img_src
        self.community_list_title = community_list_title
        self.address = address
        self.completion_date = completion_date
        self.second_hand_housing_for_sale = second_hand_housing_for_sale
        self.unit_price = unit_price
        self.price_change = price_change

    def my_print(self):
        print("""小区名称：%s\n地址：%s\n竣工日期：%s\n二手房数量：%s\n平均地价：%s\n涨幅：%s\n
        """ % (self.community_list_title, self.address, self.completion_date, self.second_hand_housing_for_sale,
               self.unit_price, self.price_change))
