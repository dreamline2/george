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
            _type = 'meat'

        if _type == 'meat':
            right = u'魚類'
            left = u'蔬果'
            rightURL = baseURL + 'fish'
            leftURL = baseURL + 'vegetable'
            text = u'蛋和肉'
            img = 'http://lh6.ggpht.com/v6fWaUdR0Lop64ug2zBScQ8u4k4L1UZsQJorOlk_Qfidj-pbPPNHglXZflS0FxElxaaKcPFdxTWc2wV-GlYG_g=w200'
        elif _type == 'vegetable':
            right = u'蛋與肉'
            left = u'魚類'
            rightURL = baseURL + 'meat'
            leftURL = baseURL + 'fish'
            text = u'蔬菜與水果'
            img = 'http://lh5.ggpht.com/MOSYap9u2Da62aUJpIXQEOaBaLPzS69T9k4iIGHCJvx9uHYHBqWknG3Z5llAIVPQQn3M3-Za1HkPLsYGfyY2Kcs=w200'
        elif _type == 'fish':
            right = u'蔬果'
            left = u'蛋與肉'
            rightURL = baseURL + 'vegetable'
            leftURL = baseURL + 'meat'
            text = u'魚類'
            img = 'http://lh3.ggpht.com/YmVrZbSRnlruPOjVcWBzNAVd-g8ReXFZ20LjKaHiqA9aPQJDNb0KHfIztWxG81Pe7ddR9Je0UhUDNeHU92VUgBk=w200'

        className = _type


        self.HtmlResponse("page_index.html", {"mode": "index", "type": _type, "name": types[_type], "right": right, "left": left, "rightURL": rightURL, "leftURL": leftURL, "text": text , "className": className, "img": img })

class DetailHandler(HtmlHandler):
    def get(self):

        baseURL = '/detail?id='
        right = u'下一個'
        left = u'上一個'
        rightURL = baseURL + 'vegetable'
        leftURL = baseURL + 'meat'

        self.HtmlResponse("page_detail.html", {"mode": "detail" ,"right": right, "left": left, "rightURL": rightURL, "leftURL": leftURL})



import webapp2
from models import Food
class UpdateImage(webapp2.RequestHandler):
    def get(self):
        foods = Food.query().fetch(1000)
        template = u"<label><img src='{1}'>{2}<input name='data' value='{0}@{1}'></label>"
        foods_template = "<br/>".join([template.format(food.name, food.image, food.type) for food in foods])

        html = u'''
            <form method='post'>
                {}
                <input type='submit'>
            </form>

        '''.format(foods_template)

        self.response.write(html)
    def post(self):
        items = self.request.POST.items()
        food_pool = []
        for item in items:
            key, url = item[1].encode('utf-8').split('@', 1)
            print key
            food = Food.get_by_id(key)
            if food.image == url:
                continue
            else:
                food.image = url
                food.put()
