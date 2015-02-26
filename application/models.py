from google.appengine.ext import ndb
from flask_oauthlib.provider import OAuth2Provider
from flask import Flask

app = Flask(__name__)
oauth = OAuth2Provider(app)

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

class Client(ndb.Model):
  name = ndb.StringProperty()
  desc = ndb.StringProperty()
  user_id = ndb.StringProperty()
  user = ndb.StringProperty()
  client_id = ndb.StringProperty()
  client_secret = ndb.StringProperty()
  is_confidential = ndb.BooleanProperty()
  redirect_uris = ndb.StringProperty()
  default_scopes = ndb.StringProperty()

  @property
  def client_type(self):
    if self.is_confidential:
      return 'confidential'
    return 'public'

  @property
  def Redirect_uris(self):
    if self.redirect_uris:
      return self.redirect_uris.split()
    return []

  @property
  def default_redirect_uri(self):
    return self.redirect_uris[0]

  @property
  def Default_scopes(self):
    if self.default_scopes:
      return self.default_scopes.split()
    return []

class Grant(ndb.Model):
  id = ndb.StringProperty()
  user_id = ndb.StringProperty()
  user = User()
  client_id = ndb.StringProperty()
  client = Client()
  code = ndb.StringProperty()
  redirect_uri = ndb.StringProperty()
  expires = ndb.DateTimeProperty()
  scopes = ndb.StringProperty()

  @property
  def Scopes(self):
    if self.scopes:
      return self.scopes.split()
    return []

  #Gotta be able to delete ourself

class Token(ndb.Model):
  id = ndb.StringProperty()
  client_id = ndb.StringProperty()
  client = Client()
  user_id = ndb.StringProperty()
  user = User()
  token_type = ndb.StringProperty()
  access_token = ndb.StringProperty()
  refresh_token = ndb.StringProperty()
  expires = ndb.DateTimeProperty()
  scopes = ndb.StringProperty()

  @property
  def scopes(self):
    if self.scopes:
      return self.scopes.split()
    return []

  #Gotta be able to delete ourself
