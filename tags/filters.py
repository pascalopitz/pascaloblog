import os
import markdown as md
from google.appengine.ext import webapp
register = webapp.template.create_template_register()

from google.appengine.ext.webapp import template

@register.filter
def markdown(value):
    return md.markdown(value, extensions=['codehilite'], safe_mode="escape")

@register.filter
def formatdate(d):
    return d.strftime("%a %d %b %Y")
    
@register.filter
def atomdate(d):
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")
