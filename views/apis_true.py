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


        datas = open('20_r').readlines()
        
        composition = []
        
        pattern = re.sub("\(.*\)", "", _id)
        pattern = re.sub("-.*", "", pattern)

        for d in datas:
            if pattern in d:
                try:
                    t1, t2, name, unit, value = d.split(' ')
                    composition.append({"name": name, "amount":float(value.strip()), "unit":unit})
                except Exception as e:
                    print e


        composition = composition or [{"name": "碳水化合物", "unit": "mg", "amount": 1}]
        
        mapping = {"fish": '魚', 'meat': '肉', 'vegetable': '菜'}
        _type = mapping[food.type]
        
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
            "type": _type, 
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



safe = open('safe.csv').read().strip()
unsafe = open('unsafe.csv').read().strip()





class FoodProcessFactor(ApiHandler):
    def get(self):
        keyword = self.request.get('keyword').encode('utf-8')

        rows = safe.split('\n')
        tmp = []
        for row in rows:
            if keyword in row:
                try:
                    city, name, address, title, date = row.split()[:5]
                    tmp.append({'name': name, 'title':title, 'city':city, 'address': address, 'date': date})
                except Exception as e:
                    print e

        rows = unsafe.split('\n')
        for row in rows:
            if keyword in row:
                try:
                    title, name, address, date, issue = row.split()[:5]
                    tmp.append({'name': name, 'title':title, 'address': address, 'date': date, "issue": issue, "unsafe": True})
                except Exception as e:
                    print e


        self.output(tmp)


