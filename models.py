from google.appengine.ext import ndb

class Note(ndb.Model):
    
    title = ndb.StringProperty()
    content = ndb.TextProperty(required=False)
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    