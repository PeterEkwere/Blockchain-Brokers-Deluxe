#!/usr/bin/python
"""
    The Following Objects Handle all RestFul API actions for Users
    Author: Peter Ekwere
"""
from models.user import User
from api.v1.auth.user_auth import RegistrationForm, LoginForm, ResetForm, UpdatePasswordForm
from api.v1.views import app_views
from flask_login import login_user, current_user, logout_user, login_required
from flask import abort, jsonify, make_response, request, session
from flask import redirect, url_for, flash, render_template
from functools import wraps
from flasgger.utils import swag_from
from datetime import datetime
from wtforms import ValidationError
from api.v1.extensions import admin_required, strong_password, auth, login_manager, cache, ReCaptcha

recaptcha = ReCaptcha(
    app_views,
    site_key="6LcWGewpAAAAAJ_pTOCycIUhR4FoD4DuhiVHsyS8",
    version=2
)

@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
@admin_required
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    all_users =  auth.all_users()
    list_users = []
    for user in all_users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)

@app_views.route('/users/register/', methods=['GET', 'POST'], strict_slashes=False, endpoint='register')
@swag_from('documentation/user/post_user.yml', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        PhoneNumber = form.PhoneNumber.data
        
        # Create a new user object with the extracted details
        try:
            new_user = auth.register_user(username.lower(), email.lower(), password, PhoneNumber)
        except ValueError:
            error_message = "This email address has already been used."  
            return render_template('signup.html',
                                   register_form = form, error_message=error_message)
        
        return redirect(url_for('app_views.login'))
    return render_template('signup.html',
                           register_form = RegistrationForm())
    

@app_views.route('/users/login/', methods=['GET', 'POST'], strict_slashes=False, endpoint='login')
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        #form = LoginForm(request.POST)
        if form.validate():
            email = form.email.data
            password = form.password.data

            # Verify user credentials (you need to implement this)
            user = auth.valid_login(email.lower(), password)
            if user:
                if current_user.is_authenticated and current_user.role == 'admin':
                    login_user(user)
                    response = redirect(url_for('app_views.admin'))
                    return response
                else:
                    check = login_user(user)
                    response = redirect(url_for('app_views.dashboard'))
                    response.cache_control.no_cache = True
                    return response
            else:
                error_message = "These credentials do not match our records."
                return render_template('login.html', Login_form=form, error_message=error_message)
    # Render the login page with the form
    return render_template('login.html', Login_form=form)

@app_views.route('/admin/', strict_slashes=False, endpoint='admin')
@login_required
@admin_required
def admin():
    return render_template('admin_dashboard.html')

@app_views.route('/dashboard/', strict_slashes=False, endpoint='dashboard')
@cache.cached(timeout=50)
def profile():
    #print(f"In Profile endpoint authentication status is {current_user.is_authenticated}")
    return render_template('user_dashboard.html')


@app_views.route('/users/logout/', strict_slashes=False, endpoint='logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app_views.login'))

@app_views.route('/users/reset_password', methods=['GET', 'POST'], strict_slashes=False, endpoint='reset_password')
def reset_password():
    form = ResetForm(request.form)
    if form.validate():
        email = form.email.data
        user = auth.validate_user(email.lower())
        if user:
            try:
                token = auth.get_reset_password_token(email.lower())
                try:
                    auth.send_password_reset_email(user, token)
                except Exception as e:
                    print(e)
                return redirect(url_for('app_views.update_password'))
                #return jsonify({"message": f"user {user.username} has recieved a reset token at {user.email} and token is {token}"})
            except ValueError:
                error_message = "User does not exist Please Input Correct email or Signup"
                return render_template('login.html', Reset_form=form, error_message=error_message)
        else:
            return render_template('reset_password.html', Reset_form=form)
    else:
        return render_template('reset_password.html', Reset_form=form)

@app_views.route('/users/update_password', methods=['GET', 'POST'], strict_slashes=False, endpoint='update_password')
def update_password():
    """ This endpoint updates a password
    """
    form = UpdatePasswordForm(request.form)
    if form.validate():
        email = form.email.data
        new_password = form.new_password.data
        token = form.Token.data
        
        try:
            strong_password(new_password)
        except ValidationError as e:
            return render_template('update_password.html', update_form=form, error_message=e)
        
        user = auth.validate_user(email.lower())
        if user:
            try:
                updated = auth.update_password(token, new_password)
                if updated:
                    return redirect(url_for('app_views.login'))
            except ValueError:
                error_message = "Invalid reset Token"
                return render_template('update_password.html', update_form=form, error_message=error_message)
        else:
            error_message = "User does not exist Please Input Correct email or Signup"
            return render_template('update_password.html', update_form=form, error_message=error_message)
            # return jsonify({"email": f"{email}", "message": "User doesnt exist"})
    else:
        return render_template('update_password.html', update_form=form)
