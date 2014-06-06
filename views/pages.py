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
    	self.HtmlResponse("index.html", {"mode": "auto"})

