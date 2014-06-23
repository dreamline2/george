#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 george 
#
# Distributed under terms of the MIT license.
from google.appengine.ext import ndb, db
from datetime import datetime

class FoodDailyInfo(ndb.Model):
    date = ndb.DateProperty()
    wholesale_price = ndb.FloatProperty(indexed=False)
    price = ndb.FloatProperty(indexed=False)
    amount = ndb.FloatProperty(indexed=False)

class Food(ndb.Model):
    next_one = ndb.StringProperty(indexed=False)
    prev = ndb.StringProperty(indexed=False)
    point = ndb.FloatProperty()
    infos = ndb.StructuredProperty(FoodDailyInfo, repeated=True)
    image = ndb.StringProperty(indexed=False)
    name = ndb.StringProperty()
    type = ndb.StringProperty(choices=['meat', 'fish', 'vegetable'])

    lowset_price = ndb.FloatProperty()
    lowset_wholesale_price = ndb.FloatProperty()
    avg_price = ndb.FloatProperty()
    avg_wholesale_price = ndb.FloatProperty()
    avg_amount = ndb.FloatProperty()

    price = ndb.FloatProperty()             ## today price
    wholesale_price = ndb.FloatProperty()   ## today wholesale_price
    amount = ndb.FloatProperty()          ## today amount

    rank = ndb.IntegerProperty()            ## today rank
    
    content = ndb.StringProperty()

    rich = ndb.BooleanProperty(default=False)
    updated = ndb.DateProperty(auto_now=True)

    def get_point(self):
        point = 0
        if self.updated <= datetime.now().date():
            point = -100
        else:
            ## 市價記分
            if self.avg_price:
                point += round(1-self.price / self.avg_price, 1) * 10
            ## 批發價記分
            if self.avg_wholesale_price:
                point += round(1-self.wholesale_price / self.avg_wholesale_price, 1) * 10
            ## 交易量記分
            if self.avg_amount:
                point += round(self.amount / self.avg_amount -1 , 1) * 10
            ## 產季記分
            point += self.rich * 10 

        return point

    def get_recommand(self):
        result = []
        ## 市價記分
        if self.avg_price:
            point = round(1-self.price / self.avg_price, 1) * 10
            if point > 0:
                result.append("市價低於平均價 {}% !!".format(point))
        ## 批發價記分
        if self.avg_wholesale_price:
            point += round(1-self.wholesale_price / self.avg_wholesale_price, 1) * 10
            if point > 0:
                result.append("批發價低於平均價 {}% !!".format(point))
        ## 交易量記分
        if self.avg_amount:
            point = round(self.amount / self.avg_amount - 1, 1) * 10
            if point > 0:
                result.append("交易量大 盛產 !!".format(point))
        ## 產季記分
        point = self.rich * 10 
        if point > 0:
            result.append("產季!!")


        return "\n".join(result)


    def aggregate(self):
        count = 0
        total_wholesale_price = 0
        total_amount = 0
        total_price = 0
        for info in self.infos:
            count+=1
            total_wholesale_price += info.wholesale_price or 0
            total_price += info.price or 0
            total_amount += info.amount or 0

        return total_wholesale_price, total_price, total_amount, count

    def push_info(self, date):
        info = FoodDailyInfo(date=date, wholesale_price=self.wholesale_price, price=self.price, amount=self.amount)
        self.infos.append(info)


        
   

