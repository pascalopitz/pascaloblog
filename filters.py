import os
import markdown as md
from google.appengine.ext import webapp
register = webapp.template.create_template_register()

from google.appengine.ext.webapp import template

@register.filter
def markdown(value):
    return md.markdown(value, extensions=['codehilite(force_linenos=True)'], safe_mode="escape")

@register.filter
def formatdate(d):
    return d.strftime("%a %d %b %Y")
    
@register.filter
def render_post(post, template_name):
    template_values = {}
    template_values['post'] = post
    template_path = os.path.join(os.path.dirname(__file__), 'templates', template_name +'.html')
    return template.render(template_path, template_values)    