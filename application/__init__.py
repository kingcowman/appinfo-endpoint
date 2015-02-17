"""
Initialize Flask app

"""
from flask import Flask
import os
from werkzeug.debug import DebuggedApplication
from flask_oauthlib.provider import OAuth2Provider

app = Flask('application')
oauth = OAuth2Provider(app)

if os.getenv('FLASK_CONF') == 'DEV':
    # Development settings
    app.config.from_object('application.settings.Development')
    # Flask-DebugToolbar
    toolbar = DebugToolbarExtension(app)
    
    @app.context_processor
    def inject_profiler():
        return dict(profiler_includes=templatetags.profiler_includes())
    app.wsgi_app = profiler.ProfilerWSGIMiddleware(app.wsgi_app)

elif os.getenv('FLASK_CONF') == 'TEST':
    app.config.from_object('application.settings.Testing')

else:
    app.config.from_object('application.settings.Production')

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
import views

