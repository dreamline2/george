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

import json



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
        result = json.dumps(result)

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
        result = [
                    {"day":"2014-05-05", "wholesaler_price": 1000, "price": 100, "amount": 400},
                    {"day":"2014-05-06", "wholesaler_price": 1170, "price": 117, "amount": 460},
                    {"day":"2014-05-07", "wholesaler_price": 660, "price": 66, "amount": 1120},
                    {"day":"2014-05-10", "wholesaler_price": 1030, "price": 103, "amount": 540},
                    {"day":"2014-05-11", "wholesaler_price": 1000, "price": 100, "amount": 400},
                    {"day":"2014-05-12", "wholesaler_price": 1170, "price": 117, "amount": 460},
                    {"day":"2014-05-13", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-14", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-15", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-16", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-17", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-18", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-19", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-20", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-21", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-22", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-23", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-24", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-25", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-26", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-27", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-28", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-29", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-30", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-31", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-06-01", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-06-02", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-06-03", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-06-04", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-06-05", "wholesaler_price": 50, "price": 120, "amount": 1200},

                ]
        self.output(result)


class ListApi(ApiHandler):
    def get(self, _type):
        order = self.request.get('order')
        result = [
                {"name": "高麗菜", "price": 34 , "wholesaler_price": 34, "image":"http://ext.pimg.tw/moongenie/4a4ef8009fc44.jpg", "order":1},
                {"name": "空心菜", "price": 45 , "wholesaler_price": 37, "image":"http://ext.pimg.tw/megusa1/1340294486-3417654905.jpg", "order":2},
                {"name": "大白菜", "price": 65 , "wholesaler_price": 76, "image":"http://www.baicaolu.com/uploads/201206/1338654120GUlOHyNF.jpg", "order":3},
                {"name": "花菜", "price": 67 , "wholesaler_price": 89, "image":"http://image.cn.made-in-china.com/2f0j01JtTaIsEKsQPO/%E4%BF%9D%E9%B2%9C%E7%99%BD%E8%8A%B1%E8%8F%9C.jpg", "order":4},
                {"name": "大陸妹", "price": 65 , "wholesaler_price": 76, "image":"http://www.baicaolu.com/uploads/201206/1338654120GUlOHyNF.jpg", "order":5},
                {"name": "星星菜", "price": 67 , "wholesaler_price": 89, "image":"http://ext.pimg.tw/megusa1/1340294486-3417654905.jpg", "order":6}
                ]
        self.output(result)

class InfoApi(ApiHandler):
    def get(self, _id):
        if _id == "高麗菜":
            result = {}
            result = {"name": "高麗菜", "price": 50 , "wholesaler_price": 30, "image":"https://s.yimg.com/hg/pimg2/69/95/p053035437625-item-3812xf2x0600x0600-m.jpg", "order":1, "next":"大白菜", "description": "夏季水果盛產，momo電視購物即日起推出多款本土及進口水果下殺4.8折起，而販售的水果皆為產地直送。"},
        elif _id == '空心菜':
            result = {"name": "空心菜", "price": 50 , "wholesaler_price": 30, "image":"http://ext.pimg.tw/megusa1/1340294486-3417654905.jpg", "order":2, "next":"大白菜", "prev":"高麗菜", "description": "夏季水果盛產，momo電視購物即日起推出多款本土及進口水果下殺4.8折起，而販售的水果皆為產地直送。"},
        elif _id == '大白菜':
            result = {"name": "大白菜", "price": 50 , "wholesaler_price": 30, "image":"http://www.baicaolu.com/uploads/201206/1338654120GUlOHyNF.jpg", "order":3, "next":"花菜", "prev":"空心菜", "description": "夏季水果盛產，momo電視購物即日起推出多款本土及進口水果下殺4.8折起，而販售的水果皆為產地直送。"},
        elif _id == '花菜':
            result = {"name": "花菜", "price": 50 , "wholesaler_price": 30, "image":"http://image.cn.made-in-china.com/2f0j01JtTaIsEKsQPO/%E4%BF%9D%E9%B2%9C%E7%99%BD%E8%8A%B1%E8%8F%9C.jpg", "order":4, "prev":"大白菜", "description": "夏季水果盛產，momo電視購物即日起推出多款本土及進口水果下殺4.8折起，而販售的水果皆為產地直送。"}

        self.output(result)



class UserLogin(ApiHandler):
    def get(self):
        token = self.request.get('token')
        self.session['is_login'] = True
        result = {"name":"test"}
        self.output(result)

class UserLogout(ApiHandler):
    def get(self):
        token = self.request.get('token')
        self.session['is_login'] = False
        result = {"status":True}
        self.output(result)

class UserInfo(ApiHandler):
    def get(self):
        is_login = self.session.get('is_login')
        if is_login:
            result = {"name":"test"}
        else:
            result = {"status": False}
        self.output(result)
