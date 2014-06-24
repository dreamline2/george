# -*- coding: utf-8 -*-
import json
import json
#from models import Food, FoodDailyInfo
from itertools import groupby
from datetime import datetime
from bs4 import BeautifulSoup
import re


def urlget(url):
    try:
        from google.appengine.api import urlfetch
        resp = urlfetch.fetch(url, deadline=30)
        return resp.content
    except:
        import urllib2
        return urllib2.urlopen(url).read()

api = 'http://m.coa.gov.tw/OpenData/AnimalTransData.aspx'
def get_base(date):
    url = api + "?TransDate={}{}".format(date.year-1911, date.strftime("%m%d")) 
    content = urlget(url)
    items = sorted(json.loads(content), key=lambda x:x[u'交易日期'])
    data = dict()
    for item in groupby(items, lambda x:x[u'交易日期']):
        key, values = item
        total_price = 0
        total_amount = 0
        total_count = 0
        for value in values:
            total_price += float(value[u'成交頭數-平均價格'])
            total_amount += float(value[u'成交頭數-總數'])
            total_count += 1
        return round(total_price/total_count, 1), total_amount


def parse_width(width):
    if 'Kg' in width:
        return round(float(width.replace('Kg', '').strip()) * 1000 / 600, 1)
    return round(float(width.replace('g', '').strip()) /600, 1)


def get(date):
    try:
        content = urlget('http://shopping.my-fresh.com/%E8%B1%AC%E8%82%89%E9%A1%9E')
        body = BeautifulSoup(content)
        products = body.select('.product-item')
        
        wholesale_price, amount = get_base(date)
    except:
        return
    for product in products:
        item = {}
        title = product.select('.product-title')[0].text.replace(u'【買新鮮】', '').strip()
        if u'肉' not in title:
            continue

        title = re.sub('\d+.*', '', title)

        width = re.search( '[.\d]+K?g', product.select('.description')[0].text).group()
        
        rate = parse_width(width)
        price = float(product.select('.actual-price')[0].text.replace('$', '') )
        price = price / rate

        item['name'] = title
        item['price'] = price
        item['wholesale_price'] = wholesale_price
        item['amount'] = amount
        item['date'] = date
        item['image'] = product.select('img')[0].attrs.get('src').replace('150.jpeg', '300.jpeg')
        item['type'] = 'meat'
        yield item

        


