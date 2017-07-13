#lngae-173610

import webapp2

import os
import jinja2
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.api import users

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout_url=users.create_logout_url(self.request.uri)
            template_context = {
                'user': user.nickname(),
                'logout-url': logout_url,
            }
            template = jinja_env.get_template('main.html')
            self.response.out.write(template.render(template_context))
            
        else:
            login_url = users.create_login_url(self.request.uri)
            self.redirect(login_url)
            
    def post(self):
        user = users.get_current_user()
        
        if user is None:
            self.error(401)
        
        logout_url = users.create_logout_url(self.request.uri)
        template_context = {
            'user': user.nickname(),
            'logout_url': logout_url,
            'note_title': self.request.get('title'),
            'note_content': self.request.get('content'),
        }
        template = jinja_env.get_template('main.html')
        self.response.out.write(template.render(template_context))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
    ], debug=True)