#!/usr/bin/env python  
# coding=utf-8

""" 
* author: Yuan
* time: 2017/6/1 10:29 
"""
import requests
from pyquery import PyQuery as pq
from lxml.html import etree
import urllib.parse
import json
import re
from setting import *


def allString(tree, xpath):
    tag = tree.xpath(xpath)
    if len(tag) == 1:
        return tag[0].xpath('string(.)')
    else:
        return None


def Xpath(tree, xpath):
    try:
        info = tree.xpath(xpath)[0]
        return info.strip('\n')
    except:
        return None


def getPage(url, proxy=None, pub_headers=HEADERS):
    try:
        res = requests.get(url, headers=pub_headers, proxies=proxy, verify=False, timeout=5)
        regex = re.compile('验证后继续使用')
        if regex.findall(res.text):
            return {'code': -4, 'msg': '机器人验证！'}
        elif res.status_code == 200:
            return {'code': 0, 'html': res.content, 'msg': 'ok'}
        else:
            return {'code': -1001, 'msg': res.status_code}
    except Exception as e:
        print('Crawling Failed', url)
        return {'code': -1002, 'msg': str(e)}


def getListPage(search_word, proxy=None):
    keyword = search_word + '工商信息_电话_地址_信用信息_财务信息-企查查'
    url = 'http://www.baidu.com/s?wd={0}&oq={0}'.format(urllib.parse.quote(keyword))
    res = getPage(url, proxy)
    if res['code'] == 0:
        tree = etree.HTML(res['html'])
        divs = tree.xpath('//div[@class="result c-container "]/div[2]')
        if divs:
            regex = re.compile('^https://www\.qichacha\.com/firm_.+')
            links = []
            for div in divs:
                domain = Xpath(div, './a[1]/text()')
                if domain and regex.findall(domain):
                    link = Xpath(div, './a[2]/@href')
                    links.append(link)
            return {'code': 0, 'data': list(set(links)), 'msg': 'ok'}
        else:
            return {'code': -5, 'msg': '列表页解析失败！'}
    else:
        res['msg'] = '[列表页]' + res['msg']
        return res


search_word = '超群服装辅料商行'

res = getListPage(search_word)
print(res)








if __name__ == "__main__":
    pass  