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


import json
class ApiHandler(webapp2.RequestHandler):
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
                    {"day":"2014-05-05", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-06", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-07", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-10", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-11", "wholesaler_price": 50, "price": 120, "amount": 1200},
                    {"day":"2014-05-12", "wholesaler_price": 50, "price": 120, "amount": 1200},
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
                    {"name": "高麗菜", "price": 50 , "wholesaler_price": 30, "image":""},
                    {"name": "空心菜", "price": 50 , "wholesaler_price": 30, "image":""},
                    {"name": "大白菜", "price": 50 , "wholesaler_price": 30, "image":""},
                    {"name": "花菜", "price": 50 , "wholesaler_price": 30, "image":""}
                ]
        self.output(result)

class InfoApi(ApiHandler):
    def get(self, _id):
        result = {"name": "高麗菜", "day_price": "50", "description": ""}
    
        self.output(result)
