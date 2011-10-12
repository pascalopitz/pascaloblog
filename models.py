from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class PostItem(polymodel.PolyModel):
    active = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now_add=True)
    published = db.DateTimeProperty()
    user = db.UserProperty()

class BlogPost(PostItem):
    title = db.StringProperty()
    text = db.TextProperty()
    url_token = db.StringProperty()

class BookmarkPost(PostItem):
    title = db.StringProperty()
    url_token = db.StringProperty()
    tags = db.ListProperty(str)

class TwitterPost(PostItem):
    title = db.StringProperty()
