#lngae-173610

import webapp2

from google.appengine.api import users

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout_url=users.create_logout_url(self.request.uri)
            self.response.write("welcomE you FUCKING LEGEND")
            
        else:
            login_url = users.create_login_url(self.request.uri)
            self.redirect(login_url)

app = webapp2.WSGIApplication([
('/', MainHandler)
], debug=True)