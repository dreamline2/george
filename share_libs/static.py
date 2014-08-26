# HINT: based on
# https://github.com/Arachnid/bloggart/blob/part1/static.py
# by Nick

from datetime import datetime
import webapp2
import hashlib
from google.appengine.ext import ndb
import os
import logging


class StaticContent(ndb.Model):
    # serve static & cache content
    path = ndb.TextProperty(required=True)
    body = ndb.BlobProperty(required=True, indexed=False)
    content_type = ndb.StringProperty(required=True, indexed=False)

    last_modified = ndb.DateTimeProperty(required=True, auto_now=True, indexed=False)

    etag = ndb.ComputedProperty(lambda self: hashlib.sha1(self.body).hexdigest(), indexed=False)
    branch = ndb.ComputedProperty(lambda self: self.version_id.split('.')[0], indexed=False)
    version_id = ndb.StringProperty(required=True, indexed=False)

    timeout = ndb.IntegerProperty(default=0)

    @classmethod
    def _get_key_name(cls, path):
        branch_name = os.environ.get("CURRENT_VERSION_ID").split('.')[0]
        return abs(hash(path + "|" + branch_name))

    @classmethod
    def get(cls, path):
        # HINT: in order to support different branch, use brench name + path as id
        obj = cls.get_by_id(cls._get_key_name(path))
        if not obj:
            return None
        elif (obj.timeout and (datetime.now() - obj.last_modified).total_seconds() > obj.timeout):
            return None
        else:
            return obj

    @classmethod
    def set(cls, path, body, content_type, timeout=0):
        # HINT: in order to support different branch, use brench name + path as id
        version_id = os.environ.get("CURRENT_VERSION_ID")
        branch_name = version_id.split('.')[0]

        content = StaticContent(
                                id=abs(hash(path + "|" + branch_name)),
                                path=path,
                                body=body,
                                content_type=content_type,
                                timeout = timeout,
                                version_id=version_id,
                                )

        content.put()
        return content

# HINT:
# http://stackoverflow.com/questions/12423614/local-variables-in-python-nested-functions
# the python nested function has some limit

HTTP_DATE_FMT_GMT = "%a, %d %b %Y %H:%M:%S GMT"
HTTP_DATE_FMT_UTC = "%a, %d %b %Y %H:%M:%S UTC"

class expires(object):
    """class based decorator is easier (because closure)
    """
    def __init__(self, expire_interval=None, force_expires=None, edge=True, t="webapp2"):
        self.t = t.lower()
        self.expire_interval = expire_interval
        self.force_expires = force_expires
        self.edge = edge

    def __call__(self, handler_method):
        return getattr(self, self.t)(handler_method)

    def webapp2(self, handler_method):
        if not self.expire_interval and not self.force_expires:
            return handler_method

        def wrapper(h, *args, **kwds):
            result = handler_method(h, *args, **kwds)

            if self.force_expires:
                expires = self.force_expires
                self.expire_interval = expires - datetime.now()
            else:
                expires = datetime.now() + self.expire_interval

            if self.expire_interval.days > 364:
                max_age = 364 * 24 * 60 * 60
            else:
                max_age = self.expire_interval.total_seconds()

            h.response.headers['Expires'] = expires.strftime(HTTP_DATE_FMT_GMT)

            # enable edge cache (proxy)
            # ref: https://github.com/lucemia/Tagtoo/issues/528
            if self.edge:
                h.response.headers['Cache-Control'] = 'public, max-age=%d' % max_age
                h.response.headers['Pragma'] = 'Public'

            return result

        return wrapper

    def django(self, handler_method):
        if not self.expire_interval and not self.force_expires:
            return handler_method

        def wrapper(request, *args, **kwds):
            response = handler_method(request, *args, **kwds)

            if self.force_expires:
                expires = self.force_expires
                self.expire_interval = expires - datetime.now()
            else:
                expires = datetime.now() + self.expire_interval

            if self.expire_interval.days > 364:
                max_age = 364 * 24 * 60 * 60
            else:
                max_age = self.expire_interval.total_seconds()

            response['Expires'] = expires.strftime(HTTP_DATE_FMT_GMT)

            # enable edge cache (proxy)
            # ref: https://github.com/lucemia/Tagtoo/issues/528
            if self.edge:
                response['Cache-Control'] = 'public, max-age=%d' % max_age
                response['Pragma'] = 'Public'

            return response

        return wrapper



class cache_content(object):
    def __init__(self, cache_key_func = None, timeout = None):
        self.cache_key_func = cache_key_func
        self.timeout = timeout

    def add_response_header(self, h, content):
        last_modified = content.last_modified.strftime(HTTP_DATE_FMT_GMT)
        h.response.headers.add('Last-Modified', last_modified)
        h.response.headers.add('ETag', content.etag)

    def output_content(self, h, content, status = None):
        self.add_response_header(h, content)

        if status != 304:
            h.response.headers.add('Content-Type', str(content.content_type))
            h.response.out.write(content.body)

        if status:
            h.response.set_status(status)

    def __call__(self, handler_method):
        def wrapper(h, *args, **kwds):
            if h.request.get("no-cache"):
                return handler_method(h, *args, **kwds)

            path = (self.cache_key_func(h) if self.cache_key_func else h.request.url)
            content = StaticContent.get(path)

            if content and content.version_id == os.environ.get('CURRENT_VERSION_ID'):
                if content.timeout != self.timeout:
                    content.timeout = self.timeout
                    content.put()

                if 'If-Modified-Since' in h.request.headers:
                    if_modified_since = h.request.headers['If-Modified-Since']
                    if ';' in if_modified_since:
                        if_modified_since = if_modified_since.split(';')[0]
                    if "GMT" in if_modified_since:
                        try:
                            last_seen = datetime.strptime(if_modified_since, HTTP_DATE_FMT_GMT)
                        except:
                            last_seen = None
                    elif "UTC" in if_modified_since:
                        try:
                            last_seen = datetime.strptime(if_modified_since, HTTP_DATE_FMT_UTC)
                        except:
                            last_seen = None
                    else:
                        last_seen = None

                    if last_seen and last_seen >= content.last_modified.replace(microsecond=0):
                        return self.output_content(h, content, status=304)

                if 'If-None-Match' in h.request.headers:
                    etags = [x.strip() for x in h.request.headers['If-None-Match'].split(',')]

                    if content.etag in etags:
                        return self.output_content(h, content, status=304)

                return self.output_content(h, content, status=200)

            result = handler_method(h, *args, **kwds)

            content = StaticContent.set(path, h.response.body, h.response.headers.get('Content-Type'), self.timeout)
            self.add_response_header(h, content)

            return result

        return wrapper
