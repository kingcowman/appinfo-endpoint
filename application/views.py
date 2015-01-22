from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from flask import request, render_template, flash, url_for, redirect, jsonify
from application import app
from models import Application 

@app.route("/appinfo", methods=["GET", "POST"])
def appinfo():
  if request.method =='POST':
    return jsonify(status="not implemented")
  else:
    appInfo = {
      "schema": "http:openid.net/schema/napps/1.0",
      "branding": {
        "companyname": "Virginia Tech",
        "companyiconurl": "http://www.ABS.com/logo.gif"
      },

      "apps": [x.to_dict() for x in Application.query().fetch()]
    }
    return jsonify(appInfo)