# -*- coding: utf-8 -*-
import json
import json
#from models import Food, FoodDailyInfo
from itertools import groupby
from datetime import datetime
import re

def urlget(url):
    try:
        from google.appengine.api import urlfetch
        resp = urlfetch.fetch(url, deadline=30)
        return resp.content
    except:
        import urllib2
        return urllib2.urlopen(url).read()

api = 'http://m.coa.gov.tw/OpenData/AquaticTransData.aspx'
def get(date):
    url = api + "?TransDate={}{}".format(date.year-1911, date.strftime("%m%d")) 
    content = urlget(url)
    items = sorted(json.loads(content)['items'], key=lambda x:x[u'魚貨名稱'])
    data = dict()
    for product in groupby(items, lambda x:x[u'魚貨名稱']):
        item = {}
        title, values = product

        if re.search("|".join([u'其他', u'待定', u'智仔', u'烏殼']), title):
            print title
            continue
        total_price = 0
        total_amount = 0
        total_count = 0
        for value in values:
            total_price += float(value[u'平均價'])
            total_amount += float(value[u'交易量'])
            total_count += 1

        item['name'] = title
        item['wholesale_price'] = round(total_price/total_count)
        item['amount'] = total_amount
        item['date'] = date
        item['type'] = 'fish'
        yield item







for item in  get(datetime(2014,6,8)):
    pass
