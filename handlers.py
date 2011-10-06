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
        
        template_values['is_admin'] = self.is_admin
        template_values['user'] = self.user
        template_values['logout_url'] = users.create_logout_url('/')

        if(self.session.has_key('message')):
            template_values['message'] = self.session['message']
            del self.session['message']
        else:
            template_values['message'] = False
        
        output = template.render(template_path, template_values)
        self.response.out.write(output)
    
    def render404(self):
        self.error(404)
        self.render('404.html', {})
        
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


class NotFoundHandler(BaseHandler):
    def get(self):
        return self.render404()

    def post(self):
        return self.render404()

class IndexHandler(BaseHandler):
    def get(self):

        q = Post.all()
        q.filter("active =", True)
        q.order('-published')
        posts = q.fetch(5)

        template_values = {}
        template_values['posts'] = posts
        template_values['active'] = True
        template_values['title'] = 'Pascal\'s Blog'
        template_values['offset'] = 5
        template_values['count'] = 5
        self.render('posts.html', template_values)

class AjaxMoreHandler(BaseHandler):
    def get(self):

        q = Post.all()
        q.filter("active =", bool(self.request.get('active')))
        q.order('-published')
        posts = q.fetch(int(self.request.get('count')), int(self.request.get('offset')))

        template_values = {}
        template_values['posts'] = posts
        template_values['active'] = bool(self.request.get('active'))
        template_values['offset'] = int(self.request.get('count')) + int(self.request.get('offset'))
        template_values['count'] = int(self.request.get('offset'))
        self.render('posts_ajax.html', template_values)

class DraftsHandler(AdminBaseHandler):
    def get(self):

        q = Post.all()
        q.filter("active =", False)
        q.order('-published')
        posts = q.fetch(5)
        
        template_values = {}
        template_values['posts'] = posts
        template_values['active'] = False
        template_values['title'] = 'Drafts'
        template_values['offset'] = 5
        template_values['count'] = 5
        self.render('posts.html', template_values)
                                 

class PostHandler(BaseHandler):
    def get(self, url_token):
        
        q = Post.all()
        q.filter("url_token =", url_token)
        post = q.get()

        if(None == post):
            return self.render404()

        if(True == post.active or True == self.is_admin):
            template_values = {}
            template_values['post'] = post
            return self.render('post.html', template_values)

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
        template_values['title'] = 'Edit Post'

        if key is not None:
            post = Post.get(key)
            template_values['post'] = post
        
        self.render('post_form.html', template_values)

        
    def post(self, key=None):
        template_values = {}
        
        post = Post()

        if(None != key):
            post = Post.get(key)
            
        if(None == post.active or False == post.active):
            post.published = datetime.datetime.now()
        
        post.title = self.request.get('title')
        post.url_token = self.request.get('url_token')
        post.excerpt = self.request.get('excerpt')
        post.text = self.request.get('text')
        post.active = bool(self.request.get('active'))
        post.user = users.get_current_user()
        
        if(None != key):
            post.save()
        else:
            post.put()
        
        if post.is_saved():
            self.message('Saved post')
            if(post.active):
                self.redirect('/')
            else:
                self.redirect('/admin/drafts')
                
        else:
            template_values['post'] = post
            template_values['title'] = 'Edit Post'
        
            self.message('Error saving')
            self.render('post_form.html', template_values)
                        
