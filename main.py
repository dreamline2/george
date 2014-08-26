#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from views import pages
from views import apis_true as apis

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    (r'/george', pages.MainHandler),
    (r'/george/google7626d4c2a7531a07.html', pages.GoogleUser),
    (r'/detail', pages.DetailHandler),
    (r'/img', pages.UpdateImage),
    (r'/api/food/([^\/]+)/$', apis.InfoApi),
    (r'/api/food/([\w]+)/list', apis.ListApi),
    (r'/api/food/([^/]+)/trend$', apis.TrendApi),
    (r'/api/user/login', apis.UserLogin),
    (r'/api/user/logout', apis.UserLogout),
    (r'/api/user/info', apis.UserInfo),

    (r'/api/foodprocessfactor', apis.FoodProcessFactor),

], config=config, debug=True)

