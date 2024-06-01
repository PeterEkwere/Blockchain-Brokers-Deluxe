#!/usr/bin/python
"""
    This Module contains the Api's point of entry
    Author: Peter Ekwere
"""
#from models import storage
from api.v1.views import app_views
from os import environ
from os import getenv
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from api.v1.extensions import mail
from flasgger import Swagger
from flasgger.utils import swag_from
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from api.v1.extensions import auth, socketio, login_manager, cache, ReCaptcha
from datetime import timedelta
import threading
import asyncio


app = Flask(__name__, static_url_path='/static')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
#csrf.init_app(app)
app.config['WTF_CSRF_CHECK_DEFAULT'] = False
app.secret_key = getenv('Deluxe_SecretKey', None)
app.config['SESSION_TYPE'] = 'filesystem'  # Or a suitable session backend
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # Persists for 60 mins
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}}, expose_headers=["Content-Type", "X-CSRFToken"], supports_credentials=True)
app.config['SWAGGER'] = {
    'title': 'Deluxe Restful API',
    'ui_version': 1 
}
#app.config["SESSION_COOKIE_SAMESITE"] = "strict"
#app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["REMEMBER_COOKIE_SECURE"] = True
app.config['MAIL_SERVER'] = 'smtp-relay.brevo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = '759a9d001@smtp-brevo.com'
app.config['MAIL_DEFAULT_SENDER'] = 'Deluxe@gmail.com'
app.config['MAIL_PASSWORD'] = 'jm7hEWcJRB4IgkHv'
app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = True
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
login_manager.init_app(app)
login_manager.login_view = 'app_views.login'
login_manager.login_message_category = 'info'
mail.init_app(app)
socketio.init_app(app)
cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})
app.register_blueprint(app_views)
Swagger(app)


@login_manager.user_loader
def load_user(user_id):
    #print("I AM IN USER LOADER FUNCTION")
    uid = auth.get_user_by_id(user_id)
    if uid:
        #print(f"User ID returned is type {type(uid).__name__} and user returned is {uid.__dict__}")
        return uid
    else:
        #print(f"I am Returning NONE User ID returned is type {type(uid).__name__} and user returned is {uid.__dict__}")
        return None

@app.errorhandler(403)
def not_found_403(error):
    """ not found error for 403
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def not_found_401(error):
    """ not found error for 401
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

def create_app():
#    """
#    """
    return app