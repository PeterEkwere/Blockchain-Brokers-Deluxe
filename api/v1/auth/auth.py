#!/usr/bin/env python3
"""
    This Module contains some auth functions
    Author: Peter Ekwere
"""
from models.engine.db_storage import DBStorage
import bcrypt
from typing import Dict, List, Union
from models.user import User
from typing import Dict, List
from api.v1.extensions import mail, Message
from sqlalchemy.exc import NoResultFound
from itsdangerous import URLSafeTimedSerializer
import random
from uuid import uuid4
import datetime


def _hash_password(password: str) -> bytes:
    """ THis Function converts a password to a hash

    Args:
        password (str): this is the string password

    Returns:
        bytes: this is the returned salt
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    #print(f"in password hashing function Salt is {salt}\nits type is {type(salt).__name__}\npassword is {password}\npassword bytes is {password_bytes} and password_bytes type is {type(password_bytes).__name__}")
    return salt


def _generate_uuid() -> str:
    """ returns a UUID in string repr
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DBStorage()

    def register_user(self, username: str, email: str, password: str, PhoneNumber: str, role: str = "regular") -> User:
        """ This method register users

        Args:
            email (str): new user email
            password (str): new user password

        Returns:
            User: a new user object
        """
        try:
            user = self._db.find_by('user', email=email)
            #print("User Was Found")
        except NoResultFound:
            #hashed_password = _hash_password(password)
            #print(f"\n in register function \n")
            #print(f"\nin register function hashed_password is {hashed_password}\nits type is {type(hashed_password).__name__}\nits decoded version saved to the db is {hashed_password.decode('utf-8')}")
            new_user = self._db.add_user(username, email, password, PhoneNumber, role)
            return new_user
        raise ValueError

    def valid_login(self, email: str, password: str) -> bool:
        """ THis method validates a user

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            bool: _description_
        """
        try:
            user = self._db.find_by('user', email=email)
        except NoResultFound:
            return None
        #password_bytes = password.encode('utf-8')
        #hash_password = user.hashed_password.encode('utf-8')
        #print(f"\nin function to verify login password passed is {password} \n and hashed password gotten from found user is {user.hashed_password}")
        #print(f"\npassword encoded version passed is {password_bytes} \n and hashed_password encoded version gotten from found user is {hash_password}")
        if password == user.hashed_password:
            return user
        else:
            return None
        
    def validate_user(self, email: str) -> bool:
        """ THis method validates a user

        Args:
            email (str): _description_

        Returns:
            bool: _description_
        """
        try:
            user = self._db.find_by('user', email=email)
        except NoResultFound:
            return None
        return user

    def get_code(self, email: str) -> str:
        """ This method is used for resetting a users password

        Args:
            email (str): _description_

        Returns:
            str: _description_
        """
        user = self._db.find_by('user', email=email)
        if user:
            digits = ''.join([str(random.randint(0, 9)) for _ in range(5)])
            self._db.update_user(user.id, reset_token=digits)
            # user.reset_token = _generate_uuid()
            return user.reset_token
        raise ValueError
    
    def send_password_reset_email(self, user, token):
        try:
            # Create the password reset email message
            msg = Message('PASSWORD RESET CODE', recipients=[user.email])
            msg.body = f"SUBJECT: Reset Password for Deluxe4.com\n\nHi {user.username},\n\nTo reset your password, use the following token: {token}\n\nIf you didn't request this, please ignore this email."
            mail.send(msg)
        except Exception as e:
            print(f"Error sending password reset code to  email({user.email}) error:{e}")
            
    def send_verification_code(self, user, token):
        try:
            # Create the password reset email message
            msg = Message('EMAIL VERIFICATION CODE', recipients=[user.email])
            msg.body = f"Subject: Email Verification Code for Deluxe4.com **\n\nHi {user.username},\n\nYout Code IS {token}\n\nIf you didn't request this, please ignore this email."
            mail.send(msg)
        except Exception as e:
            print(f"Error sending verification code for Email({user.email}) Error:{e}")
            
    
    def verify_code(self, code: str, user: object) -> bool:
        """ THis method Verify's the user's mail

        Args:
            code (str): _description_
            user (object): _description_

        Returns:
            bool: _description_
        """
        try:
            user = self._db.find_by('user', reset_token=code)
        except NoResultFound:
            return False
        except Exception as e:
            print(f"Error Found while verifing code: {e}")
        if user:
            self._db.update_user(user.id, reset_token=None)
            return True
        return False
        

    def update_password(self, reset_token: str, password: str):
        """ This method updates a users password
        """
        user = self._db.find_by('user', reset_token=reset_token)
        if user:
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, reset_token=None, hashed_password=hashed_password.decode('utf-8'))
            # hashed_password = _hash_password(password)
            # user.hashed_password = hashed_password
            # user.reset_token = None
            return True
        raise ValueError
    
    def get_user(self, email: str) -> User:
        """ This method returns a user
        """
        user = self._db.find_by("user", email=email)
        return user
    
    def get_user_by_id(self, id: str) -> User:
        #print(f"get user by id called")
        return self._db.find_by("user", id=id)
    
    def all_users(self) -> List[User]:
        """ returns all users
        """
        users = self._db.all(User)
        return users
