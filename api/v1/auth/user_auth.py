#!/usr/bin/env python3
"""
    This Module Contains a a User Model
    Author: Peter Ekwere
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer
#from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, Form
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=4, max=20, message="username cannot be less than 4 and more than 20 characters")])
    password = PasswordField('Password', validators=[DataRequired(),
                                                    Length(min=6, message="Password must be at least 6 characters long.")])
    #role = StringField('role', validators=[Length(min=5, max=7)])
    submit = SubmitField('Register')

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class ResetForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    
class UpdatePasswordForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    new_password = PasswordField('NewPassword', validators=[DataRequired(),
        validators.Length(min=8, message="Password must be at least 8 characters long"),
        validators.DataRequired()
    ])
    Confirm_new_password = PasswordField('ConfirmPassword', validators=[
        validators.EqualTo('new_password', message="Passwords must match"),
        validators.DataRequired()
    ])
    Token = StringField('Token', validators=[DataRequired(), Length(min=5, max=50)])
    submit = SubmitField('Reset')
    
