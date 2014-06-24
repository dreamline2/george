# -*- coding: utf-8 -*-
import json
import re
#from models import Food, FoodDailyInfo
from itertools import groupby
from datetime import datetime
from bs4 import BeautifulSoup


def urlget(url):
    try:
        from google.appengine.api import urlfetch
        resp = urlfetch.fetch(url, deadline=30)
        return resp.content
    except:
        import urllib2
        return urllib2.urlopen(url).read()

api = 'http://m.coa.gov.tw/OpenData/PoultryTransBoiledChickenData.aspx'
def get_base(date):
    url = api + "?StartDate={0}&EndDate={0}".format(date.strftime("%Y/%m/%d")) 
    content = urlget(url)
    item = json.loads(content)[0]
    data = dict()
    price = float(item[u'白肉雞(門市價高屏)'])
    egg_price = float(item[u'雞蛋(產地)'])
    return price, egg_price


def parse_width(width):
    if 'Kg' in width:
        return round(float(width.replace('Kg', '').strip()) * 1000 / 600, 1)
    return round(float(width.replace('g', '').strip()) /600, 1)

def get(date):
    content = urlget('http://shopping.my-fresh.com/%E5%AE%B6%E7%A6%BD%E9%A1%9E')
    body = BeautifulSoup(content)
    products = body.select('.product-item')
    try:
        wholesale_price, wholesale_egg_price = get_base(date)
    except Exception as e:
        return

    item = {}
    item['name'] = u'雞蛋'
    item['wholesale_price'] = wholesale_egg_price
    item['date'] = date
    item['type'] = 'meat'
    yield item

    for product in products:
        item = {}
        title = product.select('.product-title')[0].text.replace(u'【買新鮮】', '').strip()
        if u'省產' not in title:
            continue

        width = re.search( '[.\d]+K?g', product.select('.description')[0].text).group()
        
        rate = parse_width(width)
        price = float(product.select('.actual-price')[0].text.replace('$', '') )
        price = price / rate

        item['name'] = title
        item['price'] = price
        item['wholesale_price'] = wholesale_price
        item['date'] = date
        item['image'] = product.select('img')[0].attrs.get('src').replace('150.jpeg', '300.jpeg')
        item['type'] = 'meat'
        yield item
        




