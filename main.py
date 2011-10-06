#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# from google.appengine.dist import use_library
# use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from handlers import *

# Run the application
mappings = [
    ('/', IndexHandler),
    ('/post/([\d\w_-]+)', PostHandler),
    ('/posts/more', AjaxMoreHandler),
    ('/login', LoginHandler),
    ('/admin/drafts', DraftsHandler),
    ('/admin/post', PostFormHandler),
    ('/admin/post/([\d\w_-]+)', PostFormHandler),
    ('/admin/post/delete/([\d\w_-]+)', PostDeleteHandler),
    ('/.*', NotFoundHandler),
]

def main():
    application = webapp.WSGIApplication(mappings, debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
