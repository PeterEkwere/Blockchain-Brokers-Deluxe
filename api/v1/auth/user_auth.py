#!/usr/bin/env python3
"""
    This Module Contains a a User Model
    Author: Peter Ekwere
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer
#from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, Form, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=4, max=20, message="username cannot be less than 4 and more than 20 characters")])
    password = PasswordField('Password', validators=[DataRequired(),
                                                    Length(min=6, message="Password must be at least 6 characters long.")])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(),
        validators.Length(min=6, message="Password must be at least 6 characters long"),
        validators.EqualTo("password", message='Passwords must match'),
        validators.DataRequired()
    ])
    phonenumber = StringField('PhoneNumber', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class ResetForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    
class UpdatePasswordForm(Form):
    email = HiddenField('Email')
    new_password = PasswordField('NewPassword', validators=[DataRequired(),
        validators.Length(min=6, message="Password must be at least 6 characters long"),
        validators.DataRequired()
    ])
    confirm_new_password = PasswordField('ConfirmPassword', validators=[DataRequired(),
        validators.Length(min=6, message="Password must be at least 6 characters long"),
        validators.EqualTo("new_password", message='Passwords must match'),
        validators.DataRequired()
    ])
    code = StringField('Code', validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField('Update Password')
    

class VerifyEmailForm(Form):
    email = HiddenField('Email')
    code = StringField('Code', validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField('Submit')
    
