#!/usr/bin/env python  
# coding=utf-8

""" 
* author: Yuan
* time: 2017/6/1 10:28 
"""
import requests
from pyquery import PyQuery as pq
from lxml.html import etree
import urllib.parse
import json
import re
import time
from setting import *


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
    url = 'https://www.baidu.com/s?wd={0}&oq={0}'.format(urllib.parse.quote(keyword))
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


def allString(tree, xpath):
    tag = tree.xpath(xpath)
    if len(tag) == 1:
        return tag[0].xpath('string(.)')
    else:
        return None


def Xpath(tree, xpath):
    try:
        info = tree.xpath(xpath)[0].strip('\n')
        return info
    except:
        return None


class parseQiChaCha():
    def __init__(self, html):
        self.html = html

    def parseBaseInfo(self):
        tree = etree.HTML(self.html)
        base_info = {}
        res = tree.xpath('//td[@class="m_cl_left"]')
        if not res:
            res = tree.xpath('//td[@class="ma_left"]')
        tds = res
        if len(tds) == 17:
            try:
                base_info['name'] = allString(tree, '//span[@class="text-big font-bold"]')
                base_info['credit_code'] = tds[0].xpath('string(.)').strip('\n')
                base_info['business_id'] = tds[1].xpath('string(.)').strip('\n')
                base_info['state'] = tds[3].xpath('string(.)').strip('\n')
                base_info['corporation'] = tds[4].xpath('string(.)').strip('\n')
                base_info['capital'] = tds[5].xpath('string(.)').strip('\n')
                base_info['business_type'] = tds[6].xpath('string(.)').strip('\n')
                base_info['creation_date'] = tds[7].xpath('string(.)').strip('\n')
                operation_period = tds[8].xpath('string(.)').strip('\n')
                if operation_period and operation_period != '			   					 - - 			   				':
                    base_info['sdate'] = operation_period.split(' 至 ')[0]
                    base_info['edate'] = operation_period.split(' 至 ')[1]
                base_info['commercial_bureau'] = tds[9].xpath('string(.)').strip('\n')
                base_info['approved_date'] = tds[10].xpath('string(.)').strip('\n')
                base_info['old_name'] = tds[14].xpath('string(.)').strip('\n').replace('\xa0\xa0', '').replace(' ', ',')
                base_info['address'] = tds[15].xpath('string(.)').replace('查看地图', '').strip('\n')
                base_info['business_scope'] = tds[16].xpath('string(.)').strip('\n')

                return {'code': 0, 'data': base_info, 'msg': 'ok'}
            except:
                return {'code': -6, 'msg': '页面结构变化'}
        else:
            return {'code': -5, 'msg': '基本信息解析失败！'}

    def parseHolders(self):
        tree = etree.HTML(self.html)
        holder_list = []
        trs = tree.xpath('//section[@id="Sockinfo"]/table//tr')
        if trs:
            for tr in trs:
                holder_info = {}
                inv = tr.xpath('./td[1]/a[@class="text-lg c_a"]')
                if inv:
                    holder_info['inv'] = inv[0].xpath('string(.)')
                    holder_info['liSubConAm'] = Xpath(tr, './td[3]/text()')
                    holder_info['invType_CN'] = Xpath(tr, './td[5]/text()')
                    holder_list.append(holder_info)
            return {'code': 0, 'data': holder_list, 'msg': 'ok'}
        else:
            return {'code': -5, 'msg': '股东信息解析失败！'}

    def parseKeyPerson(self):
        tree = etree.HTML(self.html)
        keyPerson_list = []
        lis = tree.xpath('//ul[@class="m_mb"]//li')
        if lis:
            for li in lis:
                person_info = {}
                person_info['position_CN'] = Xpath(li, './label/text()')
                person_info['name'] = Xpath(li, './div/a[2]/text()')
                keyPerson_list.append(person_info)
            return {'code': 0, 'data': keyPerson_list, 'msg': 'ok'}
        else:
            return {'code': -5, 'msg': '主要成员信息解析失败！'}

    def parseBranchInfo(self):
        tree = etree.HTML(self.html)
        branch_list = []
        branches = tree.xpath('//div[@class="panel-body m_sc"]/div/a')
        if branches:
            for br in branches:
                branch_info = {}
                branch_info['brName'] = br.xpath('string(.)')
                branch_list.append(branch_info)
            return {'code': 0, 'data': branch_list, 'msg': 'ok'}
        else:
            return {'code': -5, 'msg': '主要成员信息解析失败！'}

    def parseAlterInfo(self):
        tree = etree.HTML(self.html)
        alter_list = []
        trs = tree.xpath('//*[@id="Changelist"]/table//tr')
        altItem_CN = ''
        if trs:
            for tr in trs:
                alter_info = {}
                altItem_1 = Xpath(tr, './th[@class="m_cl_cr_th"]/text()')
                altItem_2 = Xpath(tr, './th[@id="ma_cr_th2"]/text()')
                if altItem_1:
                    altItem_CN = altItem_1
                elif altItem_2:
                    altItem_CN = altItem_2
                altDate = Xpath(tr, './td[2]/text()')
                if altDate:
                    alter_info['altDate'] = altDate
                    alter_info['altItem_CN'] = altItem_CN
                    altBe = tr.xpath('./td[3]/div')
                    if altBe:
                        alter_info['altBe'] = altBe[0].xpath('string(.)')
                    altAf = tr.xpath('./td[4]/div')
                    if altAf:
                        alter_info['altAf'] = altAf[0].xpath('string(.)')
                    alter_list.append(alter_info)
            return {'code': 0, 'data': alter_list, 'msg': 'ok'}
        else:
            return {'code': -5, 'msg': '变更信息解析失败！'}

    def run(self):
        data = {}
        base_res = self.parseBaseInfo()
        if base_res['code'] == 0:
            data['base_info'] = base_res['data']

        holder_res = self.parseHolders()
        if holder_res['code'] == 0:
            data['page_partners'] = holder_res['data']

        person_res = self.parseKeyPerson()
        if person_res['code'] == 0:
            data['page_employees'] = person_res['data']

        branch_res = self.parseBranchInfo()
        if branch_res['code'] == 0:
            data['page_branches'] = branch_res['data']

        alter_res = self.parseAlterInfo()
        if alter_res['code'] == 0:
            data['page_changes'] = alter_res['data']

        if data:
            return {'code': 0, 'data': data, 'msg': 'ok'}
        else:
            return base_res


def main(search_word, proxy=None):
    list_res = getListPage(search_word, proxy)
    if list_res['code'] == 0:
        print(list_res['data'])
        content = []
        for link in list_res['data']:
            time.sleep(2)
            html_res = getPage(link, proxy)
            print(html_res['msg'])
            if html_res['code'] == 0:
                qichacha = parseQiChaCha(html_res['html'])
                data = qichacha.run()
                if data['code'] == 0:
                    content.append(data['data'])
        if content and len(content) == len(list_res['data']):
            return {'code': 0, 'data': json.dumps(content), 'msg': 'ok'}
        elif content and len(content) < len(list_res['data']):
            return {'code': -1, 'data': json.dumps(content), 'msg': '抓取不全!'}
        else:
            return {'code': -2, 'msg': '详情页抓取失败！'}
    else:
        return {'code': -3, 'msg': list_res['msg']}