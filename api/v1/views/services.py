#!/usr/bin/python
"""
    The Following Objects Handle all RestFul API actions for WagerBrain Services
    Author: Peter Ekwere
"""
from models.user import User
from api.v1.auth.user_auth import RegistrationForm, LoginForm, ResetForm, UpdatePasswordForm
#from api.v1.auth.auth import Auth
from api.v1.views import app_views
from flask_login import login_user, current_user, logout_user, login_required
from flask import abort, jsonify, make_response, request, session
from flask import redirect, url_for, flash, render_template
from functools import wraps
from flasgger.utils import swag_from
from datetime import datetime, timedelta
from wtforms import ValidationError
import time
from api.v1.extensions import admin_required, auth, socketio, emit, cache