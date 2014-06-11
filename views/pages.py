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
        _type = self.request.GET.get('category')
        types = {
            'fish': u'魚類',
            'vegetable': u'蔬菜',
            'meat': u'肉和蛋'
        }
        if _type not in types:
            _type = 'fish'

        self.HtmlResponse("page_index.html", {"mode": "index", "type": _type, "name": types[_type] })

class DetailHandler(HtmlHandler):
    def get(self):
        self.HtmlResponse("page_detail.html", {"mode": "detail"})
