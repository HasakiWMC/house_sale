#!usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:51211 
@file: sale_item.py
@time: 2017/07/02 
"""


class HouseItem(object):
    def __init__(self, img_src, house_list_title, structure, area, floor, time, address, price_det, unit_price):
        self.img_src = img_src
        self.house_list_title = house_list_title
        self.structure = structure
        self.area = area
        self.floor = floor
        self.time = time
        self.address = address
        self.price_det = price_det
        self.unit_price = unit_price

    def my_print(self):
        print("""房产标题：%s\n几室几厅：%s\n面积：%s\n楼层：%s\n建成时间：%s\n地理位置：%s\n总价：%s\n均价：%s\n
        """ % (self.house_list_title, self.structure, self.area, self.floor, self.time, self.address, self.price_det,
               self.unit_price))
