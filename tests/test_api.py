#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 george 
#
# Distributed under terms of the MIT license.

from mock import patch, MagicMock
import unittest
import webtest
import webapp2
from google.appengine.ext import testbed
import json
from main import *
import random
import base64
import re
from collections import defaultdict
from faker import Factory
from datetime import datetime
import urllib

class Api_test(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_all_stubs()
        self.cookies = {}
        self.testapp = webtest.TestApp(app, cookiejar=self.cookies)
        


    #----- product query test --------------
    def test_pipeline(self):
        resp = self.testapp.get('/api/food/1/')
        resp = self.testapp.get('/api/food/1/trand')
        resp = self.testapp.get('/api/food/mean/list')
