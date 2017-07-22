#!/usr/bin/env python  
# coding=utf-8

""" 
* author: Yuan
* time: 2017/5/31 19:24 
"""
import redis
import time
from setting import *


class RedisClient(object):
    def __init__(self, host=HOST, port=PORT, db=2):
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD, db=db)
        else:
            self._db = redis.Redis(host=host, port=port, db=db)

    def put(self, string, addr=COMPANY_INFO_ADDR):
        self._db.rpush(addr, string)

    def pop(self, addr=COMPANY_NAME_ADDR_1):
        try:
            return self._db.lpop(addr)
        except Exception as e:
            print(e)

    def get(self, addr):
        while True:
            try:
                return self._db.get(addr)
            except:
                time.sleep(10)
