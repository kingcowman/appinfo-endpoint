from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from flask import request, render_template, flash, url_for, redirect, jsonify
from application import app
from models import Application 

@app.route("/appinfo", methods=["GET", "POST"])
def appinfo():
  return jsonify(status="hello")


