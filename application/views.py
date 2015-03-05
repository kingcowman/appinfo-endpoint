from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from flask import request, render_template, flash, url_for, redirect, jsonify, Flask
from application import app
from models import Application, User, Client, Grant, Token
from google.appengine.api import users

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
