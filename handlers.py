import os
import datetime

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models import *

from appengine_utilities import sessions



class BaseHandler(webapp.RequestHandler):
    def __init__(self):
        self.session = sessions.Session()
        self.is_admin = users.is_current_user_admin()
        self.user = users.get_current_user()
        
    def render(self, template_file, template_values):
        
        template.register_template_library('filters')        
        
        template_path = os.path.join(os.path.dirname(__file__), 'templates', template_file)
        layout_path = os.path.join(os.path.dirname(__file__), 'templates', 'layout.html')
        
        template_values['is_admin'] = self.is_admin
        template_values['user'] = self.user
        template_values['logout_url'] = users.create_logout_url('/')

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


class AdminBaseHandler(BaseHandler):
    def initialize(self, request, response):
        BaseHandler.initialize(self, request, response)
        
        if(None == self.user):
            self.redirect(users.create_login_url(request.url))
        elif(False == users.is_current_user_admin()):
            self.message('No admin rights')
            self.redirect('/')


class IndexHandler(BaseHandler):
    def get(self):

        q = Post.all()
        q.filter("active =", True)
        posts = q.fetch(5)

        template_values = {}
        template_values['title'] = 'Homepage'
        template_values['posts'] = posts
        self.render('index.html', template_values)


class DraftsHandler(AdminBaseHandler):
    def get(self):

        q = Post.all()
        q.filter("active =", False)
        posts = q.fetch(1000)
        
        template_values = {}
        template_values['title'] = 'Homepage'
        template_values['posts'] = posts
        self.render('index.html', template_values)
                                 

class PostHandler(BaseHandler):
    def get(self, url_token):
        
        post = Post.get_by_key_name(url_token)
        
        if(True == post.active or True == self.is_admin):
            template_values = {}
            template_values['title'] = 'Post - ' + post.title
            template_values['post'] = post
            self.render('post.html', template_values)
        else:
            self.message('Not allowed')
            return self.redirect('/')
        


class PostDeleteHandler(AdminBaseHandler):
    def get(self, key=None):
        post = Post.get(key)
        post.delete()
        self.message('Deleted post')
        self.redirect('/')


class LoginHandler(BaseHandler):
    def get(self):
        if(self.user):
            self.message('Already logged in')
            self.redirect('/')
        else:
            self.redirect(users.create_login_url('/'))

            
class PostFormHandler(AdminBaseHandler):
    def get(self, key=None):
        template_values = {}

        if key is not None:
            post = Post.get(key)
            template_values['title'] = 'Edit Post - ' + post.title
            template_values['post'] = post
        else:
            template_values['title'] = 'Add Post'
        
        self.render('post_form.html', template_values)

        
    def post(self):
        url_token = self.request.get('url_token')

        post = Post.get_or_insert(url_token)
        
        if(False == post.active):
            post.published = datetime.datetime.now()
        
        post.title = self.request.get('title')
        post.url_token = self.request.get('url_token')
        post.excerpt = self.request.get('excerpt')
        post.text = self.request.get('text')
        post.active = bool(self.request.get('active'))
        post.user = users.get_current_user()

        post.save()

        if post.is_saved():
            self.message('Saved post')
            self.redirect('/')
        else:
            self.message('Error saving')
            self.render('post_form.html', template_values)
            
            