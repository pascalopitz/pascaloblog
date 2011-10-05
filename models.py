from google.appengine.ext import db

class Post(db.Model):
    title = db.StringProperty()
    text = db.TextProperty()
    url_token = db.StringProperty()
    active = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now_add=True)
    published = db.DateTimeProperty()
    user = db.UserProperty()
