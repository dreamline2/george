#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 george 
#
# Distributed under terms of the MIT license.
from google.appengine.ext import ndb, db

class Food(ndb.Model):
    name = ndb.StringProperty()
    price = ndb.IntegerProperty()
    wholesale_price = ndb.IntegerProperty()
    amount = ndb.IntegerProperty()
   


class FoodModel(ndb.Model):
    recommand = ndb.FloatProperty()

