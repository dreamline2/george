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

api = 'http://m.coa.gov.tw/OpenData/FarmTransData.aspx'
def get(date):
    item = {}
    url = api + "?StartDate={0}{1}&EndDate={0}{1}".format(date.year-1911, date.strftime(".%m.%d")) 
    content = urlget(url)
    items = sorted(json.loads(content), key=lambda x:x[u'作物名稱'])
    data = dict()
    for product in groupby(items, lambda x:x[u'作物名稱'].strip()):

        title, values = product

        if re.search("|".join([u'康乃馨', u'美女撫子', u'火鶴花', u'菊', u'劍蘭', u'其它花卉', u'柔麗絲', u'八卦草', u'黃梔花', u'松蟲草', u'百合', u'鳥', u'鶴', u'垂焦', u'觀音蓮', u'美人蕉', u'薑荷花', u'薑花', u'火炬花', u'夜來香', u'秀線', u'向日葵', u'大理花', u'雞冠花', u'鳳梨花', u'珊瑚鳳梨', u'麒麟草', u'繡球花', u'海芋', u'睡蓮', u'伯利恆之星', u'茉莉', u'櫻', u'百子蓮', u'羅迪納', u'蘭', u'玫瑰', u'希拉', u'薇薇安娜', u'曼尼薩', u'羅賓娜', u'多娜托', u'洋桔梗', u'星辰花', u'孔雀', u'卡斯比亞', u'滿天星', u'切葉類', u'尤加利葉', u'壽松', u'木', u'七里香', u'柳', u'棉', u'松', u'火鶴葉', u'八角金盤', u'柏', u'鋸齒蔓綠絨葉', u'觀賞', u'竹', u'水燭花', u'圓葉', u'水燭葉', u'山防風', u'葵', u'金魚草', u'其他', u'花', u'草', u'千日紅', u'卓我', u'天鵝絨', u'射干', u'小可愛', u'水晶香水', u'珠廉', u'白松', u'鬱金', u'黃椰心', u'進口連翹', u'鬱金香', u'錦鳳垂蕉', u'長春籐', u'香椿', u'高山羊齒', u'傘高梁', u'垂雞冠', u'萬引', u'黃金葛葉', u'進口臘梅', u'斑葉女真', u'萬引']), title):
            continue

        total_price = 0
        total_amount = 0
        total_count = 0
        for value in values:
            total_price += float(value[u'平均價'])
            total_amount += float(value[u'交易量'])
            total_count += 1

        if not title:
            continue
        item['name'] = title
        item['wholesale_price'] = round(total_price/total_count)
        item['amount'] = total_amount
        item['date'] = date
        item['type'] = "vegetable"
        yield item






if __name__ == '__main__':
    tmp = []
    for i in get(datetime(2014,6,1)):
        tmp.append(i)
        print i['name']

