#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 george
#
# Distributed under terms of the MIT license.


import webapp2

import re

import webapp2
from template.handler import HtmlHandler
from webapp2_extras import sessions
from models import Food
import json
import datetime
from google.appengine.api import urlfetch
from share_libs import static
from datetime import timedelta

def parserDate(obj):
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')



class ApiHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def output(self, result):
        result = json.dumps(result, default=parserDate)

        if self.request.method == 'GET' and self.request.GET.get('callback', False):
            result = "{}({})".format(self.request.GET.get('callback'), result)
            content_type = 'application/javascript'
        else:
            content_type = 'application/json'

        self.response.content_type = content_type
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(result)

    def handle_exception(self, exception, debug):
        result = {
                'status': 'error',
                'msg': exception.message
            }
        result = json.dumps(result)

        self.response.status = 500
        self.response.write(result)


import datetime
class TrendApi(ApiHandler):
    @static.expires(expire_interval=timedelta(0, 360000))
    def get(self, _id):
        result = Food.get_by_id(_id).infos
        result = [r.to_dict() for r in result]
        days = [r['date'] for r in result]

        day = datetime.datetime(2014,6,1)
        today = datetime.datetime.today() - datetime.timedelta(1)
        while day < today:
            day = day + datetime.timedelta(1)
            if day.date() in days:
                continue
            data = {}
            data['amount'] = 0
            data['date'] = day.date()
            data['wholesale_price'] = 0
            data['price'] = 0
            result.append(data)

        result.sort(key=lambda x:x['date'])
        self.output(result)


class ListApi(ApiHandler):
    @static.expires(expire_interval=timedelta(0, 360000))
    def get(self, _type):
        size = int(self.request.get('size', 6))
        page = int(self.request.get('page', 1))

        foods = Food.query(Food.type==_type).fetch(1000)
        foods = sorted(foods, key= lambda x:x.rank)[size*page - size : size*page]
        result = [{"name":v.name, "price": v.price, "wholesale_price": v.wholesale_price, "image":v.image, "order": v.rank} for v in foods]
        self.output(result)

class InfoApi(ApiHandler):
    @static.expires(expire_interval=timedelta(0, 360000))
    def get(self, _id):

        food = Food.get_by_id(_id)

        composition = [{"name": "維生素B群  & C 菸鹼素", "amount": 5.2000, 'unit': "mg"}, {"name":"維生素E α-生育醇", "amount": 1.2400, "unit": "mg"}, {"name":"維生素E   維生素E總量", "amount": 3.0200, "unit": "mg"}, {"name":"礦物質   鈣", "amount": 33.0000, "unit": "mg"}]

        result = {
            "name": food.name,
            "price": food.price,
            "wholesale_price": food.wholesale_price,
            "order": food.rank,
            "next": food.next_one,
            "prev": food.prev,
            "description": food.get_recommand(),
            "image": food.image,
            "composition": composition,
            "type": "豬肉",
        }

        self.output(result)



class UserLogin(ApiHandler):
    def get(self):
        try:
            if self.session.get('is_login'):
                profile = self.session.get('profile')
            else:
                token = self.request.cookies.get('accessToken')
                api = "https://graph.facebook.com/me?fields=id,name,picture,email&access_token={}"
                
                resp = urlfetch.fetch(api.format(token))
                profile = json.loads(resp.content)

                self.session['is_login'] = True
                self.session['token'] = token
                self.session['profile'] = profile

            result = {
                "name" : profile.get('name'),
                "email": profile.get('email'),
                "image": profile.get('picture').get('data').get('url'),
                "id": profile.get('id')
            }
            self.output(result)
        except Exception as e:
            logging.info(e)
            self.session['is_login'] = False
            self.output({"status": False})

class UserLogout(ApiHandler):
    def get(self):
        token = self.request.get('token')
        self.session['is_login'] = False
        result = {"status":True}
        self.output(result)

class UserInfo(ApiHandler):
    def get(self):
        try:
            is_login = self.session.get('is_login')
            if is_login:
                profile = self.session.get('profile')

                result = {
                    "name" : profile.get('name'),
                    "email": profile.get('email'),
                    "image": profile.get('picture').get('data').get('url'),
                    "id": profile.get('id')
                }
            else:
                result = {"status": False}
            self.output(result)
        except Exception as e:
            logging.info(e)
            self.session['is_login'] = False
            self.output({"status": False})


data = '''
花蓮縣  格全食品工業股份有限公司花蓮分公司  花蓮縣玉里鎮三民里三民路6之5號  冷藏、冷凍畜禽生鮮肉品【冷凍鴨肉分切】  98,102      
花蓮縣  銘驊農畜行  花蓮縣花蓮市國強里豐村113號 冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍雞肉分切】    99,102      
花蓮縣  阿漾咕咕體驗園區暨肉品加工廠【光豐地區農會】    花蓮縣光復鄉西富村中正路二段6巷10號 冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍豬肉分切】    101     
花蓮縣  花蓮市農會超市配貨中心  花蓮縣花蓮市中山路二段1號   冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍豬肉分切】    101     
宜蘭縣  台灣菸酒股份有限公司宜蘭酒廠    宜蘭縣宜蘭市大道里舊城西路3號   香腸【中式香腸】    98,102      
宜蘭縣  呈康食品股份有限公司    宜蘭縣五結鄉利工一路二段64號    調理肉品【義大利肉醬、菩提齋、羅漢齋_全素】 98      
宜蘭縣  立暉食品有限公司    宜蘭縣蘇澳鎮聖湖里中山路二段395號   醃漬肉品【臘肉】    99      
宜蘭縣  博士鴨畜產品實業有限公司    宜蘭縣五結鄉福興村新五路1-1號   調理肉品【鴨排】    100     
宜蘭縣  勝贏屠宰股份有限公司    宜蘭縣壯圍鄉11鄰新南村【路】96-7號  調理肉品【烤鴨、水煮雞、水煮鴨】    101     
宜蘭縣  謝記畜產食品股份有限公司    宜蘭縣五結鄉利工三路71號    醃漬肉品【鴨賞切片】    101     
基隆市  郁貿企業有限公司    基隆市武隆街105號   生鮮肉品【冷藏小分切雞肉】  101     
基隆市  樹森開發股份有限公司基隆廠  基隆市七堵區工建南路23號    冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍牛肉分切】    102     
台北市  衛鮮食品股份有限公司    台北市內湖區民善街128號B2   冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍牛肉分切】    101,102     
新北市  嘉一香食品股份有限公司樹林廠    新北市樹林區俊安街43號  冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍豬肉分切】    97,102      
新北市  協麟食品企業股份有限公司    新北市三峽區正義街16號  醃漬肉品【培根、火腿】  97      
新北市  中國青年商店股份有限公司    新北市五股區興珍里37鄰五工六路53-2號    冷藏、冷凍畜禽生鮮肉品【冷藏豬肉分切】  98      
新北市  愛味香食品股份有限公司  新北市鶯歌區中正三路491巷7號    調理肉品【宮保雞丁】    98      
新北市  美淇食品有限公司    新北市中和區中山路二段342號 ※冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍豬肉分切】※調理肉品【豬、牛、羊】 98      
新北市  芬芳烹材股份有限公司    新北市樹林區武林街9-6號 冷藏、冷凍畜禽生鮮肉品【冷凍豬肉分切】  98      
新北市  貴族世家企業股份有限公司土城廠  新北市土城區沛陂里中興路17號    調理肉品【丁骨牛排、沙朗牛排】  99      
新北市  廣達香食品股份有限公司  新北市新莊區化成路382巷18號 乾燥肉品【肉鬆】    99      
新北市  西北食品工業股份有限公司    新北市林口區工二工業區粉寮路一段102號   調理肉品【水晶餃】  99      
新北市  鼎耀食品股份有限公司    新北市新店區寶橋路235巷14號1樓  冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍雞肉】    99,102      
新北市  金軒揚食品有限公司  新北市中和區錦和路30號  乾燥肉品【豬肉乾】  100     
新北市  百傑國際食品有限公司    新北市三重區重新路五段661巷2號  調理肉品【黑胡椒豬排】  100     
新北市  新力香食品有限公司【一廠】  新北市三峽區介壽街一段338巷12號【一廠】 乾燥肉品【肉胚、肉鬆】  100     
新北市  新力香食品有限公司【二廠】  新北市三峽區介壽街一段318巷17號【二廠】 乾燥肉品【肉胚、肉鬆】  100     
新北市  弘燁實業股份有限公司    新北市三重區光復路二段90號  香腸【中式香腸_廣式臘腸】   100     
新北市  立台食品工業股份有限公司    新北市三重區光華路59號  冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍雞肉】    100     
新北市  強富食品股份有限公司    新北市三重區光復路二段42巷39號5樓   調理肉品【漢堡肉】  100     
新北市  皇上皇食品股份有限公司汐止廠    新北市汐止區水源路二段179號 香腸【中式香腸_廣式臘腸】   100     
新北市  鬍鬚張股份有限公司五股廠    新北市五股區五工ㄧ路106號1樓    調理肉品【雞肉絲】  101     
新北市  泓霖食品工業有限公司    新北市土城區承天路71巷4弄21號   冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍豬肉】    101     
新北市  統好興業有限公司    新北市土城區中華路1段70巷21號   冷藏、冷凍畜禽生鮮肉品【冷凍豬肉】  101     
新北市  統賀冷凍食品有限公司    新北市三重區中正北路530巷18弄1號    調理肉品【冷凍牛肉片】  101     
新北市  唯一行食業股份有限公司  新北市五股區五權三路24號    乾燥肉品【牛肉乾】  101     
桃園縣  雅勝冷凍食品股份有限公司    桃園縣蘆竹鄉山腳村泉州路3號 冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍豬肉】    97,101      
桃園縣  保障責任台灣省北台雞肉運銷合作社：大成長城企業股份有限公司大園廠    桃園縣大園鄉三石村五鄰三塊石45-51號 冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍雞肉】    97,101      
桃園縣  新東陽股份有限公司  桃園縣大園鄉大工路11號  香腸【中式香腸】    97,101      
桃園縣  樂山股份有限公司    桃園縣龍潭鄉八德村八張犁55-7號  調理肉品【冷凍咖哩雞調理包】    97      
桃園縣  超秦企業股份有限公司    桃園縣桃園市中埔里永安路1063號  冷藏、冷凍畜禽生鮮肉品【冷藏、冷凍雞肉】    98,102      
桃園縣  碁富食品股份有限公司觀音廠  桃園縣觀音鄉經建四路21號    醃漬肉品【洋火腿】  98      
桃園縣  富豐國際食品股份有限公司    桃園縣大園鄉大觀路550號 醃漬肉品【培根】    98      
桃園縣  瑞輝食品股份有限公司    桃園縣大園鄉大工路13號  香腸【西式香腸_博客Q肉丁德國香腸】  98      
桃園縣  欣光食品股份有限公司    桃園縣中壢市中壢工業區南園路2-50號  調理肉品【冷凍咖哩肉片、香蒜排骨】  99      
桃園縣  瑞美食品股份有限公司    桃園縣大園鄉田心村大觀路255號   醃漬肉品【煙燻鴨胸】    100     
桃園縣  上德食品有限公司    桃園縣觀音鄉玉林路一段522號 冷藏、冷凍畜禽生鮮肉品【冷藏冷凍雞肉分切】  102     
新竹市  海瑞食品有限公司    新竹市香山區牛埔東路568巷17號   調理肉品【貢丸】    98,102      
新竹市  華品食品有限公司    新竹市香山區埔前里埔前路231巷28號   調理肉品【貢丸】    101     
新竹市  昶瑞食品有限公司    新竹市香山區埔前里牛埔南路169-3號   調理肉品【貢丸】    101     
新竹市  新宇禎福記食品有限公司  新竹市南港街7巷35號 調理肉品【貢丸】    101     
新竹市  振坊有限公司：阿中丸子  新竹市香山區海埔路171巷73號 調理肉品【貢丸】    101     
新竹市  鼎昱食品有限公司    新竹市香山區埔前里牛埔南路169-5號   調理肉品【貢丸】    102     
新竹縣  三憶食品股份有限公司    新竹縣芎林鄉文林村柯子林56之10號    冷藏、冷凍畜禽生鮮肉品【冷凍雞肉分切】  101     

'''
data = data.strip()


class FoodProcessFactor(ApiHandler):
    def get(self):
        rows = data.split('\n')
        tmp = []
        for row in rows:
            city, name, address, title, date = row.split()[:5]
            tmp.append({'icon': 'http://momkitchen.com/images/logo.png','name': name, 'title':title, 'city':city, 'address': address, 'date': date})

        self.output(tmp)


