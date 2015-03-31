from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from flask import request, render_template, flash, url_for, redirect, jsonify, Flask
from application import app
from models import  User, Client, Grant, Token
from google.appengine.api import users
from flask_oauthlib.provider import OAuth2Provider
from werkzeug.security import gen_salt
from datetime import datetime, timedelta
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


@app.route('/client')
def client():
  user = users.get_current_user()
  if not user:
    return redirect('/')
  item = Client()
  item.client_id = gen_salt(40)
  item.client_secret = gen_salt(50)
  item.user_id = user.user_id()
  item.redirect_uris.append("http://localhost:8080/zack")
  item.default_scopes.append("email")
  item.put()
  return jsonify(
    client_id = item.client_id,
    client_secret = item.client_secret
  )  

@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
  user = users.get_current_user()
  if not user:
    return redirect('/')
  if request.method == 'GET':
    client_id = request.args.get('client_id')
    return True
  return True

@oauth.clientgetter
def load_client(client_id):
  return Client.query(Client.client_id==client_id).get()

@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query(Grant.client_id==client_id, Grant.code==code).get()

@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=600)
    grant = Grant()
    grant.client_id = client_id
    grant.code = code['code']
    grant.redirect_uri = request.redirect_uri
    grant.scopes = request.scopes
    grant.expires = expires
    grant.put()
    return grant

@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query(access_token==access_token).get()
    elif refresh_token:
        return Token.query(refresh_token==refresh_token).get()

@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query(
      Token.client_id==request.client.client_id,
      Token.user_id==request.user.userid)
    # make sure that every client has only one token connected to a user
    for t in toks:
        t.key.delete()

    expires_in = token['expires_in']
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token()
    tok.access_token = token['access_token']
    tok.refresh_token = token['refresh_token']
    tok.token_type = token['token_type']
    #tok.scopes = token['scope']
    tok.expires = expires
    tok.client_id = request.client_id
    tok.user_id = request.user_id

    tok.put()
    return tok

@app.route('/zack', methods=['GET', 'POST'])
def test():
  print("HEERRREEEEE2")
  return "hey"

@app.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token():
  print("YOLO SWAG")
  return None
