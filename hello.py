#lngae-173610

import webapp2

import os
import jinja2
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.api import users
from models import Note
from google.appengine.ext import ndb

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout_url=users.create_logout_url(self.request.uri)
            template_context = {
                'user': user.nickname(),
                'logout-url': logout_url,
            }
            self.response.out.write(self._render_template('main.html', template_context))
            
        else:
            login_url = users.create_login_url(self.request.uri)
            self.redirect(login_url)
            
    def post(self):
        user = users.get_current_user()
        
        if user is None:
            self.error(401)
        
        ancestor_key = ndb.Key("User", user.nickname())
        qry = Note.owner_query(ancestor_key)
        notes = qry.fetch()
        
        note = Note(parent=ndb.Key("User",user.nickname()),
                    title=self.request.get('title'),
                    content=self.request.get('content'))
        note.put()
        
        logout_url = users.create_logout_url(self.request.uri)
        template_context = {
            'user': user.nickname(),
            'logout_url': logout_url,
            'note_title': self.request.get('title'),
            'note_content': self.request.get('content'),
        }
        self.response.out.write(self._render_template('main.html', template_context))
        
    def _render_template(self, template_name, context=None):
        if context is None:
            context = {}
        
        user = users.get_current_user()
        ancestor_key = ndb.Key("User", user.nickname())
        qry = Note.owner_query(ancestor_key)
        context['notes'] = qry.fetch()
        
        template = jinja_env.get_template(template_name)
        return template.render(context)    
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ], debug=True)