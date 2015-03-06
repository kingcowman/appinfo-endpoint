from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from flask import request, render_template, flash, url_for, redirect, jsonify, Flask
from application import app
from models import  User, Client, Grant, Token
from google.appengine.api import users
from flask_oauthlib.provider import OAuth2Provider
oauth = OAuth2Provider(app)

@app.route("/", methods=["GET"])
def login():
  user = users.get_current_user()
  if user:
    if not User.query(User.userid==user.user_id()).fetch():
      a = User()
      a.name = user.nickname()
      a.email = user.email()
      a.userid = user.user_id()
      a.put()
    greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                  (user.nickname(), users.create_logout_url('/')))
  else:
    greeting = ('<a href="%s">Sign in or register</a>.' %
                users.create_login_url('/'))
  return greeting


@app.route("/appinfo", methods=["GET", "POST"])
def appinfo():
  if request.method =='POST':
    return jsonify(status="not implemented")
  else:
    apps = []
    for x in Application.query().fetch():
      apps.append(x.to_dict())

    appInfo = {
      "schema": "http://openid.net/schema/napps/1.0",
      "branding": {
        "companyname": "Virginia Tech",
        "companyiconurl": "http://www.ABS.com/logo.gif"
      },

      "apps": apps

      #[x.to_dict() for x in Application.query().fetch()]
    }
    return jsonify(appInfo)

#add functionality to ensure a user is logged in
#clean up and add lots of error checking
@app.route("/oauth/authorize", methods=['GET', 'POST'])
def authorize():
  if request.method == 'GET':
    user = users.get_current_user()
    client_id = request.args.get('client_id')
    response_type = request.args.get('response_type')
    redirect_uri = request.args.get('redirect_uri')
    scope = request.args.get('scope')

    client_key = ""

    if not (Client.query(Client.client_id==client_id).fetch()):
      c = Client()
      c.redirect_uris = []
      c.default_scopes = []
      c.client_id = client_id
      c.redirect_uris.append(redirect_uri)
      c.default_scopes.append(scope)
      c.user_id = user.user_id()
      c.client_secret = "abcde12345"  #maybe? and if so is this arbritrary?

      client_key = c.put()

    #probably should call grant setter if needed, maybe not needed from example
    #state not implemented for now, only when passed from ta

    if (client_key == ""):
      temp = Client.query(Client.client_id==client_id).fetch()
      redirect = temp[0].Redirect_uris
      return redirect[0] + "?code=" + temp[0].client_secret

    temp = client_key.get()
    redirect = temp.Redirect_uris
    return redirect[0] + "?code=" + temp.client_secret

"""
@app.route("/oauth/token", methods=['POST'])
def token_handler():
  if request.method == 'POST':
    grant_type = request.form['grant_type'] #must be "authorization_code"
    code = request.form['code']             #must match code we sent
    redirect_uri = request.form['redirect_uri'] #must match original in authorize
    client_id = request.form['client_id']   #must be able to authenticate

    temp = Client.query(Client.client_id==client_id).fetch()
    if not temp:
      return "Error: Client ID not recognized"

    if not (temp[0].client_secret == code):
      return "Error: Incorrect Code"

    #check redirect_uri and user
    #call token setter if possible

    replyDict = {
      "access_token": "dumby_access_asd123",
      "toke_type": "Bearer",
      "refresh_token": "dumby_refresh_mnb987",
      "expires_in": "3600",   #not gonna be a string
      "id_token": "dumby_id_zxc456"
    }

    return jsonify(replyDict)
"""


@oauth.clientgetter
def load_client(client_id):
  return Client.query(Client.client_id==client_id).get()

@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query(Grant.client_id==client_id, Grant.code==code).get()

@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant()
    grant.client_id = client_id
    grant.code = code
    grant.redirect_uri = request.redirect_uri
    grant.scopes = ' '.join(request.scopes)
    grant.expires = expires
    grant.put()
    return grant

@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query(access_token==access_token).get()
    elif refresh_token:
        return Token.query(refresh_token==refresh_token).get()

from datetime import datetime, timedelta

@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query(client_id==request.client.client_id,
                                 user_id==request.user.id)
    # make sure that every client has only one token connected to a user
    for t in toks:
        t.key.delete()

    expires_in = token.pop['expires_in']
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token()
    tok.access_token = token['access_token']
    tok.refresh_token = token['refresh_token']
    tok.token_type = token['token_type']
    tok.scopes = token['scope']
    tok.expires = expires
    tok.client_id = request.client_id
    tok.user_id = request.user_id

    tok.put()
    return tok

@app.route('/oauth/token')
@oauth.token_handler
def access_token():
    return None
