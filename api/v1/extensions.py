#!/usr/bin/python3
from flask_executor import Executor
import uuid
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from wtforms import ValidationError
from flask import redirect, url_for, flash, render_template
from functools import wraps

login_manager = LoginManager()

from flask_mail import Mail, Message
mail = Mail()

from api.v1.auth.auth import Auth
auth = Auth()

from flask_socketio import SocketIO, emit
socketio = SocketIO()

from flask_caching import Cache
cache = Cache()

from google_recaptcha import ReCaptcha



def admin_required(func):
    """
    Decorator that checks if the current user is an admin.
    If not, redirects to the login page.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':  # Replace with your logic to check if user is admin
            return func(*args, **kwargs)
        return redirect(url_for('app_views.login'))  # Replace 'login' with your login route name
    return decorated_function

def strong_password(password: str):
    """
    Custom validator to enforce strong password requirements:
    - At least 9 characters long
    - Contains lowercase, uppercase, and special characters
    - Contains at least one digit

    Raises a ValidationError if the password doesn't meet these criteria.
    """
    if len(password) < 9:
        raise ValidationError("Password must be at least 9 characters long.")
    if not any(char.islower() for char in password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit.")
