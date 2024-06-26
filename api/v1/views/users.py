#!/usr/bin/python
"""
    The Following Objects Handle all RestFul API actions for Users
    Author: Peter Ekwere
"""
from models.user import User
from api.v1.auth.user_auth import RegistrationForm, LoginForm, ResetForm, UpdatePasswordForm, VerifyEmailForm
from api.v1.views import app_views
from flask_login import login_user, current_user, logout_user, login_required
from flask import abort, jsonify, make_response, request, session, send_from_directory
from flask import redirect, url_for, flash, render_template
from functools import wraps
from flasgger.utils import swag_from
from datetime import datetime
from wtforms import ValidationError
from api.v1.extensions import admin_required, strong_password, auth, login_manager, cache, ReCaptcha
import urllib.request
import os
from werkzeug.utils import secure_filename
from sqlalchemy.exc import NoResultFound



recaptcha = ReCaptcha(
    app_views,
    site_key="6LcWGewpAAAAAJ_pTOCycIUhR4FoD4DuhiVHsyS8",
    version=2
)


UPLOAD_FOLDER = 'api/v1/static/uploads/kyc'
PROFILE_FOLDER =  'api/v1/static/uploads/profiles'
RECEIPT_FOLDER = 'api/v1/static/uploads/receipts'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPG'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     

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
                    response = redirect(url_for('app_views.profile'))
                    response.cache_control.no_cache = True
                    return response
                else:
                    return redirect(url_for('app_views.verify_email', email=email.lower()))
            else:
                error_message = "These credentials do not match our records."
                return render_template('login.html', Login_form=form, error_message=error_message)
    # Render the login page with the form
    return render_template('login.html', Login_form=form)

@app_views.route('/users/profile/', strict_slashes=False, endpoint='profile')
@login_required
def profile():
    user_id = current_user.id
    try:
        user = auth.get_user_by_id(user_id)
    except NoResultFound:
        print("User was not found")
        
    if user.profile_photo:
        prefix_to_strip = "api/v1/static/"
        value = user.profile_photo['front']
        main_filename = value[len(prefix_to_strip):]
        main_filename = main_filename.replace("\\", "/")
        if user.first_name and user.last_name and user.address and user.email and user.PhoneNumber and user.state and user.city:
            return render_template('edit_profile.html', zipcode=user.zipcode, user_id=user_id, profile_path=main_filename, email=user.email, first_name=user.first_name, last_name=user.last_name, address=user.address, PhoneNumber=user.PhoneNumber, state=user.state, city=user.city)
        return render_template('edit_profile.html', user_id=user_id, profile_path=main_filename)
    return render_template('edit_profile.html', user_id=user_id)


@app_views.route('/users/deposit_logs/', strict_slashes=False, endpoint='deposit_logs')
@login_required
def deposit_logs():
    return render_template('deposit_log.html')


@app_views.route('/users/withdrawal_logs/', strict_slashes=False, endpoint='withdrawal_logs')
@login_required
def deposit_logs():
    return render_template('withdrawal_log.html')


@app_views.route('/users/swap_assets/', strict_slashes=False, endpoint='swap_assets')
@login_required
def deposit_logs():
    return render_template('swap_assets.html')


@app_views.route('/users/swap_history/', strict_slashes=False, endpoint='swap_history')
@login_required
def deposit_logs():
    return render_template('swap_history.html')


@app_views.route('/users/wallets/', strict_slashes=False, endpoint='wallets')
@login_required
def deposit_logs():
    return render_template('wallets.html')


@app_views.route('/users/auto_trade/', strict_slashes=False, endpoint='auto_trade')
@login_required
def auto_trade():
    return render_template('auto_trade.html')


@app_views.route('/users/deposit_data_insert/', strict_slashes=False, endpoint='deposit_data_insert')
@login_required
def deposit_data_insert():
    #amount = request.get_json()
    amount2 = request.args.get("amount")
    return render_template('deposit_data_insert.html', amount=amount2)

@app_views.route('/users/account_types/', strict_slashes=False, endpoint='account_types')
@login_required
def account_types():
    return render_template('account_types.html')

@app_views.route('/users/convert/', methods=['POST'], strict_slashes=False, endpoint='convert')
@login_required
def convert():
    data = request.get_json()
    try:
        user = auth.get_user_by_id(current_user.id)
    except NoResultFound:
        return jsonify({"error": "User was not found"}), 500
        
    from_currency = data["from_currency"]
    to_currency = data["to_currency"]
    amount = data["amount"]
    addtocurrency = data["addtocurrency"]
    switch_check = current_user.switch_check
    demo_user_balance = {
            "BUSD": user.demo_balance,
            "ETH": user.eth_balance,
            "BTC": user.btc_balance,
            "SOL": user.sol_balance,
            "BCH": user.Bitcoin_Cash,
            "USDT": user.Tether_USD,
            "DOGE": user.Dogecoin,
            "XRP": user.Ripple,
            "DOT": user.Polkadot,
            "ADA": user.Cardano,
            "XLM": user.stellar_balance,
            "LINK": user.chainlink,
    }
    
    demo_attr = {
            "BUSD": "demo_balance",
            "ETH": "eth_balance",
            "BTC": "btc_balance",
            "SOL": "sol_balance",
            "BCH": "Bitcoin_Cash",
            "USDT": "Tether_USD",
            "DOGE": "Dogecoin",
            "XRP": "Ripple",
            "DOT": "Polkadot",
            "ADA": "Cardano",
            "XLM": "stellar_balance",
            "LINK": "chainlink",
    }
    
    live_user_balance = {
            "USD": user.live_balance,
            "ETH": user.live_eth_balance,
            "BTC": user.live_btc_balance,
            "SOL": user.live_sol_balance,
            "BCH": user.live_Bitcoin_Cash,
            "USDT": user.live_Tether_USD,
            "DOGE": user.live_Dogecoin,
            "XRP": user.live_Ripple,
            "DOT": user.live_Polkadot,
            "ADA": user.live_Cardano,
            "XLM": user.live_stellar_balance,
            "LINK": user.live_chainlink,
    }
    
    live_attr = {
            "USD": "live_balance",
            "ETH": "live_eth_balance",
            "BTC": "live_btc_balance",
            "SOL": "live_sol_balance",
            "BCH": "live_Bitcoin_Cash",
            "USDT": "live_Tether_USD",
            "DOGE": "live_Dogecoin",
            "XRP": "live_Ripple",
            "DOT": "live_Polkadot",
            "ADA": "live_Cardano",
            "XLM": "live_stellar_balance",
            "LINK": "live_chainlink",
    }
    
    if switch_check == 'demo':
        if demo_user_balance[from_currency] < amount:
            return({"error": "insufficient balance"})
    elif switch_check == 'live':
        if live_user_balance[from_currency] < amount:
            #print(f"in the check balance condition switch is live and from currency is {from_currency} and amount is {amount} and to currency is {to_currency} and from currency balance is {live_user_balance[from_currency]}")
            return({"error": "insufficient balance"})
    
    try:
        if switch_check == 'demo':
            sub_currency = demo_user_balance[from_currency] - amount
            add_currency = demo_user_balance[to_currency] + addtocurrency
            setattr(user, demo_attr[from_currency], sub_currency)
            setattr(user, demo_attr[to_currency], add_currency)
            auth._db.save()
        elif switch_check == 'live':
            sub_currency = live_user_balance[from_currency] - amount
            add_currency = live_user_balance[to_currency] + addtocurrency
            setattr(user, live_attr[from_currency], sub_currency)
            setattr(user, live_attr[to_currency], add_currency)
            auth._db.save()
    except Exception as e:
        return jsonify({"error": "ATTRIBUTE ERROR"}), 500
    
    if switch_check == 'demo':
        return jsonify({"success": user.demo_balance}), 200
    elif switch_check == 'live':
        return jsonify({"success": user.live_balance}), 200

    return jsonify({"success": "You have successfully updated "}), 200


@app_views.route('/users/onboard/', strict_slashes=False, endpoint='onboard')
@login_required
def onboard():
    user_id = current_user.id
    return render_template('user_id.html', user_id=user_id)


@app_views.route('/admin/', strict_slashes=False, endpoint='admin')
@login_required
@admin_required
def admin():
    return render_template('admin_dashboard.html')

@app_views.route('/dashboard/', strict_slashes=False, endpoint='dashboard')
@cache.cached(timeout=50)
def dashboard():
    return render_template('user_dashboard')


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
    if form.validate():
        print("FORM HAS BEEN VALIDATED")
        email = form.email.data
        new_password = form.new_password.data
        token = form.code.data
        confirm_new_password = form.confirm_new_password.data
        try:
            updated = auth.update_password(token, new_password)
            if updated:
                return redirect(url_for('app_views.login'))
        except ValueError:
            error_message = "Invalid Reset Code"
            print(error_message)
            return render_template('update_password.html', update_form=form, error_message=error_message)
    return render_template('update_password.html', update_form=form)
 
 
@app_views.route('users/profile_picture/upload', methods=['GET', 'POST'], endpoint="upload_profile_image")
@login_required
def upload_profile_image():
    """ THis Endpoint handles the retrieval and update of the user's profile photo

    Returns:
        _type_: _description_
    """
    #user_id = request.form['user_id']
    user_id = current_user.id
    try:
        user = auth.get_user_by_id(user_id)
    except NoResultFound:
        print("User was not found")
    if request.method == 'POST':
        if 'file1' not in request.files:
            error_message = "File 1 input missing"
            return render_template('edit_profile.html', error_message=error_message, user_id=user_id)
        file1 = request.files['file1']
        if file1.filename == '':
            error_message = 'Oops! It looks like you forgot to select a Valid Image, Please Choose one'
            print(error_message)
            return render_template('edit_profile.html', error_message=error_message, user_id=user_id)
        if file1 and allowed_file(file1.filename):
            file1name = secure_filename(file1.filename)
            file1_path = os.path.join(PROFILE_FOLDER, file1name)
            file1.save(file1_path)
            auth._db.update_user(user.id,  profile_photo={"front": file1_path})
            prefix_to_strip = "api/v1/static/"
            value = user.profile_photo['front']
            main_filename = value[len(prefix_to_strip):]
            main_filename = main_filename.replace("\\", "/")
            message = "Your Profile Image Has Been Uploaded."
            print(message)
            return jsonify({"user_id": user_id, "profile_path": main_filename}), 200
    else:
        return render_template('edit_profile.html', user_id=user_id)
    return render_template('edit_profile.html', user_id=user_id)
        
        
        
@app_views.route('users/update_profile/', methods=['POST'], endpoint="update_profile")
@login_required
def update_profile():
    user_data = request.get_json()  # Use request.get_json() if data is JSON in request body
    #print(f"user_data is {user_data}")
    # Update user profile in your database
    try:
        user = auth.get_user_by_id(user_data['id'])
        auth._db.update_user(user.id,  **user_data)
    except NoResultFound:
        print("User was not found")
    
    
    return jsonify({"message": "success"})
        
@app_views.route('/KYC/', methods=['GET', 'POST'])
@login_required
def upload_image():
    if request.method == 'POST':
        #user_id = request.form['user_id']
        user_id = current_user.id
        user = auth.get_user_by_id(user_id)
        verification_mode = request.form.get('verification_mode')
        if verification_mode in ['drivers_license', 'national_id']:
            if 'file1' not in request.files or 'file2' not in request.files:
                error_message = "file 1 and 2 missing"
                return render_template('user_id.html', error_message=error_message, user_id=user_id)
            file1 = request.files['file1']
            file2 = request.files['file2']
            if file1.filename == '':
                error_message = 'Oops! It looks like you forgot to select a document for file 1. Please choose one before continuing'
                return render_template('user_id.html', error_message=error_message, user_id=user_id)
            if file2.filename == '':
                error_message = 'Oops! It looks like you forgot to select a document for file 2. Please choose one before continuing'
                return render_template('user_id.html', error_message=error_message, user_id=user_id)
            if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
                file1name = secure_filename(file1.filename)
                file2name = secure_filename(file2.filename)
                file1_path = os.path.join(UPLOAD_FOLDER, file1name)
                file2_path = os.path.join(UPLOAD_FOLDER, file2name)
                file1.save(file1_path)
                file2.save(file2_path)
                auth._db.update_user(user.id,  kyc_data={"front": file1_path, "back": file2_path})
                message = "Your KYC information has been submitted for verification."
                return render_template('user_id.html', message=message, user_id=user_id)
        else:
            if 'file1' not in request.files:
                error_message = "File 1 input missing"
                return render_template('user_id.html', error_message=error_message, user_id=user_id)
            file1 = request.files['file1']
            if file1.filename == '':
                error_message = 'Oops! It looks like you forgot to select a document for file 1. Please choose one before continuing'
                return render_template('user_id.html', error_message=error_message, user_id=user_id)
            if file1 and allowed_file(file1.filename):
                file1name = secure_filename(file1.filename)
                file1_path = os.path.join(UPLOAD_FOLDER, file1name)
                file1.save(file1_path)
                auth._db.update_user(user.id,  kyc_data={"front": file1_path})
                message = "Your KYC information has been submitted for verification."
                return render_template('user_id.html', message=message, user_id=user_id)
    else:
            error_message = 'Please upload a document in one of the following formats: PNG, JPG, JPEG, or GIF.'
            return render_template('user_id.html', error_message=error_message, user_id=user_id)
    return render_template('user_id.html')
 
 
@app_views.route('users/payment_proof/', methods=['POST'], endpoint="payment_proof")
@login_required
def payment_proof():
    """ THis Endpoint handles the retrieval and update of the user's profile photo

    Returns:
        _type_: _description_
    """
    #user_id = request.form['user_id']
    user_id = current_user.id
    try:
        user = auth.get_user_by_id(user_id)
    except NoResultFound:
        print("User was not found")
    if request.method == 'POST':
        if 'file1' not in request.files:
            error_message = "File 1 input missing"
            print(error_message)
        file1 = request.files['file1']
        if file1.filename == '':
            error_message = 'Oops! It looks like you forgot to select a Valid Image, Please Choose one'
            print(error_message)
        if file1 and allowed_file(file1.filename):
            file1name = secure_filename(file1.filename)
            file1_path = os.path.join(RECEIPT_FOLDER, file1name)
            file1.save(file1_path)
            auth._db.update_user(user.id,  payment_proof={"receipt": file1_path})
            message = "Your reciept Has Been Uploaded."
            print(message)
            return jsonify({"success": message}), 200
        
        
@app_views.route('users/switch', methods=['POST'], endpoint="switch")
@login_required
def switch():
    """ This endpoint updates the switch
    """
    switch = request.get_json().get('switch')
    
    try:
        user = auth.get_user_by_id(current_user.id)
    except NoResultFound:
        print("User was not found")
        
    auth._db.update_user(user.id,  switch_check=switch)
    
    
    return jsonify({"ok": "Switch Updated successfully"}), 200
    