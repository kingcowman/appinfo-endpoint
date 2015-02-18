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

class Client(ndb.Model):
  name = ndb.StringProperty()
  description=ndb.StringProperty()
  user_id = ndb.StringProperty()
  client_id = ndb.StringProperty()
  client_secret = ndb.StringProperty()
  is_confident = ndb.BooleanProperty()

  _redirect_uris = ndb.StringProperty()
  _default_scopes = ndb.StringProperty(
    )
  @property
  def client_type(self):
    if self.is_confidential:
    return 'confidential'
  return 'public'

  @property
  def redirect_uris(self):
  if self._redirect_uris:
    return self._redirect_uris.split()
  return []

  @property
  def default_redirect_uri(self):
    return self.redirect_uris[0]

  @property
  def default_scopes(self):
  if self._default_scopes:
    return self._default_scopes.split()
  return []

  class Grant(ndb.Model):
    id = ndb.IntegerProperty()
    user_id = ndb.IntegerProperty()

    client_id=ndb.StringProperty()

    code = ndb.StringProperty()

    redirect_uri = ndb.StringProperty()
    expires = ndb.DateTimeProperty()

    _scopes = ndb.StringProperty()
    @property
    def scopes(self):
      if self._scopes:
        return self._scopes.split()
      return []

  class Token(ndb.Model):
    id = ndb.IntegerProperty()
    client_id = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    token_type = ndb.StringProperty()
    access_token = ndb.StringProperty()
    refresh_token = ndb.StringProperty()
    id_token = ndb.StringProperty()
    expires = ndb.DateTimeProperty()

    _scopes = ndb.StringProperty()

    @property
    def scopes(self):
      if self._scopes:
        return self._scopes.split()
      return [] 