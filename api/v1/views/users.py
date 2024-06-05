#!/usr/bin/python
"""
    The Following Objects Handle all RestFul API actions for Users
    Author: Peter Ekwere
"""
from models.user import User
from api.v1.auth.user_auth import RegistrationForm, LoginForm, ResetForm, UpdatePasswordForm, VerifyEmailForm
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
        confirm_password = form.confirm_password.data
        phonenumber = form.phonenumber.data
        
        # Create a new user object with the extracted details
        try:
            new_user = auth.register_user(username.lower(), email.lower(), password, phonenumber)
        except ValueError:
            error_message = "This email address has already been used."  
            return render_template('signup.html',
                                   register_form = form, error_message=error_message)
        
        return redirect(url_for('app_views.verify_email', email=email.lower()))
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
                if user.is_verified and user.role == 'admin':
                    login_user(user)
                    response = redirect(url_for('app_views.admin'))
                    return response
                elif user.is_verified is True:
                    check = login_user(user)
                    response = redirect(url_for('app_views.dashboard'))
                    response.cache_control.no_cache = True
                    return response
                else:
                    return redirect(url_for('app_views.verify_email', email=email.lower()))
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
    return render_template('user-id.html')


@app_views.route('/users/logout/', strict_slashes=False, endpoint='logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app_views.login'))

@app_views.route('/users/verify_email', methods=['GET', 'POST'], strict_slashes=False, endpoint='verify_email')
def verify_email():
    form = VerifyEmailForm(request.form)
    user_email = request.args.get("email")
    user = auth.validate_user(user_email.lower())
    
    if form.validate():
        code = form.code.data
        check = auth.verify_code(code, user)

        if check:
            print(f"IN VERIFY EMAIL USER IS VERIFIED IS {user.is_verified}")
            auth._db.update_user(user.id, is_verified=True)
            return redirect(url_for('app_views.login'))
        else:
            if user:
                error_message = "Verification code is incorrect. Please make sure there are no spaces before or after the code and try again. "
                return render_template('validateEmail.html', verify_form=form, error_message=error_message, email=user_email.lower())
    else:
        if user:
            try:
                token = auth.get_code(user_email.lower())
                try:
                    auth.send_verification_code(user, token)
                except Exception as e:
                    print(e)
            except ValueError:
                error_message = "User does not exist Please Go Back and Input Correct email or Signup"
                return render_template('validateEmail.html', verify_form=form, error_message=error_message, email=user_email.lower())
    return render_template('validateEmail.html', verify_form=form, email=user_email.lower())
        
        
@app_views.route('/users/resend_code', methods=['GET', 'POST'], strict_slashes=False, endpoint='resend_code')
def resend_code():
    user_email = request.args.get("email")
    user = auth.validate_user(user_email.lower())
    if user:
        try:
            token = auth.get_code(user_email.lower())
            try:
                auth.send_verification_code(user, token)
                return redirect(url_for('app_views.verify_email', email=user_email.lower()))
            except Exception as e:
                error_message = "Error occurred while sending the verification code. Please try again later."
                return redirect(url_for('app_views.verify_email', email=user_email.lower(), error_message=error_message))
        except ValueError:
            error_message = "User does not exist Please Input Correct email or Signup"
            return redirect(url_for('app_views.verify_email', email=user_email.lower(), error_message=error_message))
    else:
        return redirect(url_for('app_views.verify_email', email=user_email.lower()))



@app_views.route('/users/reset_password', methods=['GET', 'POST'], strict_slashes=False, endpoint='reset_password')
def reset_password():
    form = ResetForm(request.form)
    
    if form.validate():
        email = form.email.data
        user = auth.validate_user(email.lower())
        if user:
            try:
                token = auth.get_code(email.lower())
                try:
                    auth.send_password_reset_email(user, token)
                except Exception as e:
                    print(e)
                return redirect(url_for('app_views.update_password', email=email.lower()))
                #return jsonify({"message": f"user {user.username} has recieved a reset token at {user.email} and token is {token}"})
            except ValueError:
                error_message = "User does not exist Please Input Correct email or Signup"
                return render_template('login.html', Reset_form=form, error_message=error_message)
        else:
            error_message = "User does not exist Please Input Correct email or Signup"
            return render_template('reset_password.html', Reset_form=form, error_message=error_message)
    return render_template('reset_password.html', Reset_form=form)

@app_views.route('/users/update_password', methods=['GET', 'POST'], strict_slashes=False, endpoint='update_password')
def update_password():
    """ This endpoint updates a password
    """
    form = UpdatePasswordForm(request.form)
    user_email = request.args.get("email")
    print(f"WE ARE IN UPDATE PASSWORD AND USER EMAIL IS {user_email}")
    if form.validate():
        print("FORM HAS BEEN VALIDATED")
        email = form.email.data
        new_password = form.new_password.data
        token = form.code.data
        confirm_new_password = form.confirm_new_password.data
        try:
            updated = auth.update_password(token, new_password)
            if updated:
                print("PASSWORD HAS BEEN UPDATED")
                return redirect(url_for('app_views.login'))
            print("PASSWORD NOT UPDATED")
        except ValueError:
            error_message = "Invalid Reset Code"
            print(error_message)
            return render_template('update_password.html', update_form=form, error_message=error_message)
    print("RENDERING AGAIN")
    return render_template('update_password.html', update_form=form)
