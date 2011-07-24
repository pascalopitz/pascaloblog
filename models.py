from google.appengine.ext import db

class Post(db.Model):
    title = db.StringProperty()
    excerpt = db.StringProperty()
    text = db.StringProperty()
    url_token = db.StringProperty()