from google.appengine.ext import ndb

class Application(ndb.Model):
  name = ndb.StringProperty()
  type = ndb.StringProperty(repeated=True)
  scope = ndb.StringProperty()
  default_scopes = ndb.StringProperty(repeated=True)
  icon_uri = ndb.StringProperty()
  web_init_ep = ndb.StringProperty()
  bundle_id = ndb.StringProperty()
  custom_uri = ndb.StringProperty()
  
class User(ndb.Model):
  name = ndb.StringProperty()
  email = ndb.StringProperty()
  userid = ndb.StringProperty()
  image = ndb.StringProperty()
