from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from flask import request, render_template, flash, url_for, redirect, jsonify, Flask
from application import app
from models import Application, User, Client, Grant, Token
from google.appengine.api import users

#app = Flask(__name__)
#oauth = OAuth2Provider(app)

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

@app.route("/oauth/authorize", methods=['GET', 'POST'])
def authorize():
  if request.method == 'GET':
    client_id = request.args.get('client_id')
    response_type = request.args.get('response_type')
    redirect_uri = request.args.get('redirect_uri')
    scope = request.args.get('scope')

    argDict = {
      "client_id": client_id,
      "response_type": response_type,
      "redirect_uri": redirect_uri,
      "scope": scope
    }

    return jsonify(argDict)
