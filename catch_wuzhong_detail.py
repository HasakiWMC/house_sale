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
    url = 'https://suzhou.anjuke.com/sale/wuzhong/'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
                 '59.0.3071.115 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

