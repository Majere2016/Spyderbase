#!/usr/bin/env python  
# coding=utf-8

""" 
* author: Yuan
* time: 2017/6/2 14:22 
"""
import requests
import qichacha
from db import *


def getProxy():
    url = 'http://10.0.92.6:5000/get'
    response = requests.get(url)
    proxy = {'http': 'http://' + response.text}
    return proxy


def main():
    _db = RedisClient()
    # proxy_db = RedisClient(db=3)
    while True:
        # proxy = proxy_db.pop(PROXIES_ADDR).decode('utf-8')
        # proxy = getProxy()
        search_word = _db.pop().decode('utf-8')
        print(search_word)
        res = qichacha.main(search_word)
        if res['code'] == 0:
            print('  成功获取！')
            _db.put(res['data'])
        elif res['code'] == -1:
            print('  抓取不全！')
            _db.put(res['data'])
        elif res['code'] == -2:
            print('  {}'.format(res['msg']))
            _db.put(search_word, COMPANY_NAME_ADDR_2)
        else:
            print('  {}'.format(res['msg']))
            _db.put(search_word, COMPANY_NAME_ADDR_2)
        time.sleep(5)


if __name__ == "__main__":
    main()