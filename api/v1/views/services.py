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
import urllib.request
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 

 
@app_views.route('/KYC', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app_views.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('user-id.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app_views.route('/KYC/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)