#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 george
#
# Distributed under terms of the MIT license.


import webapp2
from template.handler import HtmlHandler

class MainHandler(HtmlHandler):
    def get(self):
        types = ['fish', 'vegetable', 'meat']
        baseURL = '/george?category='
        _type = self.request.GET.get('category')
        types = {
            'fish': u'魚類',
            'vegetable': u'蔬菜',
            'meat': u'蛋與肉'
        }
        if _type not in types:
            _type = 'fish'

        if _type == 'meat':
            right = u'魚類'
            left = u'蔬果'
            rightURL = baseURL + 'fish'
            leftURL = baseURL + 'vegetable'
        elif _type == 'vegetable':
            right = u'蛋與肉'
            left = u'魚類'
            rightURL = baseURL + 'meat'
            leftURL = baseURL + 'fish'
        elif _type == 'fish':
            right = u'蔬果'
            left = u'蛋與肉'
            rightURL = baseURL + 'vegetable'
            leftURL = baseURL + 'meat'


        self.HtmlResponse("page_index.html", {"mode": "index", "type": _type, "name": types[_type], "right": right, "left": left, "rightURL": rightURL, "leftURL": leftURL })

class DetailHandler(HtmlHandler):
    def get(self):

        baseURL = '/detail?id='
        right = u'下一個'
        left = u'上一個'
        rightURL = baseURL + 'vegetable'
        leftURL = baseURL + 'meat'

        self.HtmlResponse("page_detail.html", {"mode": "detail" ,"right": right, "left": left, "rightURL": rightURL, "leftURL": leftURL})
