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
    def get(self, _id):
        result = Food.get_by_id(_id).infos
        result = [r.to_dict() for r in result]
        self.output(result)


class ListApi(ApiHandler):
    def get(self, _type):
        size = int(self.request.get('size', 6))
        page = int(self.request.get('page', 1))

        foods = Food.query(Food.type==_type).fetch(1000)
        foods = sorted(foods, key= lambda x:x.rank)[size*page - size : size*page]
        result = [{"name":v.name, "price": v.price, "wholesale_price": v.wholesale_price, "image":v.image, "order": v.rank} for v in foods]
        self.output(result)

class InfoApi(ApiHandler):
    def get(self, _id):

        food = Food.get_by_id(_id)
        result = {
            "name": food.name,
            "price": food.price,
            "wholesale_price": food.wholesale_price,
            "order": food.rank,
            "next": food.next_one,
            "prev": food.prev,
            "description": food.get_recommand(),
            "image": food.image
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
