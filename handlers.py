import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext.webapp import template

from models import *

from appengine_utilities import sessions


class BaseHandler(webapp.RequestHandler):
    def __init__(self):
        self.session = sessions.Session()

    def render(self, template_file, template_values):
        
        is_admin = True
        
        template_path = os.path.join(os.path.dirname(__file__), 'templates', template_file)
        layout_path = os.path.join(os.path.dirname(__file__), 'templates', 'layout.html')
        
        template_values['is_admin'] = is_admin
        
        if(self.session.has_key('message')):
            template_values['message'] = self.session['message']
            del self.session['message']
        else:
            template_values['message'] = False
        
        layout_values = template_values
        layout_values['content'] = template.render(template_path, template_values)
        
        output = template.render(layout_path, layout_values)
        self.response.out.write(output)

        
    def message(self, message):
        self.session['message'] = message;



class IndexHandler(BaseHandler):
    def get(self):
        template_values = {}
        template_values['title'] = 'Homepage'
        template_values['posts'] = Post.all()
        self.render('index.html', template_values)
                                 


class PostHandler(BaseHandler):
    def get(self, url_token):
        post = Post.get_by_key_name(url_token)
        
        template_values = {}
        template_values['title'] = 'Post - ' + post.title
        template_values['post'] = post
        self.render('post.html', template_values)



class PostDeleteHandler(BaseHandler):
    @login_required
    def get(self, key=None):
        post = Post.get(key)
        post.delete()
        self.message('Deleted post')
        self.redirect('/')

            
            
class PostFormHandler(BaseHandler):
    @login_required
    def get(self, key=None):
        
        template_values = {}
        template_values['title'] = 'Add Post'

        if key is not None:
            post = Post.get(key)
            template_values['title'] = 'Edit Post - ' + post.title
            template_values['post'] = post
        
        self.render('post_form.html', template_values)

        
    def post(self):
        url_token = self.request.get('url_token')

        post = Post.get_or_insert(url_token)
        post.title = self.request.get('title')
        post.url_token = self.request.get('url_token')
        post.excerpt = self.request.get('excerpt')
        post.text = self.request.get('text')
        post.save()

        if post.is_saved():
            self.message('Saved post')
            self.redirect('/')
        else:
            self.message('Error saving')
            self.render('post_form.html', template_values)
            
            