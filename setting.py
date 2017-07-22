#!/usr/bin/env python  
# coding=utf-8

""" 
* author: Yuan
* time: 2017/6/1 10:42 
"""
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

# Redis地址和端口
HOST = '192.168.32.215'
PORT = 6379

# Redis密码
PASSWORD = None

# Redis公司名存放位置
COMPANY_NAME_ADDR_1 = 'huo_yan:company_name'
COMPANY_NAME_ADDR_2 = 'huo_yan:company_name_2'

# Redis企业信息存放位置
COMPANY_INFO_ADDR = 'huo_yan:shuidi'

# 代理IP存放位置
PROXIES_ADDR = 'proxies'