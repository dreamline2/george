import jinja2
import webapp2
import dot

import codecs
import os


def js_template(js_file):
    return dot.template(codecs.open(js_file,'r','utf8').read())


class HtmlHandler(webapp2.RequestHandler):
    jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader('george')
    )
    jinja_environment.globals['js_template'] = js_template



    def HtmlResponse(self, template_path, data):
        template = self.jinja_environment.get_template(template_path)
        self.response.out.write(template.render(data))

