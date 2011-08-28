import markdown as md

from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.filter
def markdown(value):
    return md.markdown(value, extensions['codehilite'])
