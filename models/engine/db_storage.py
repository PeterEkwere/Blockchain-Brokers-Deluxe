#!/usr/bin/python
"""
    This will Contain the class DBStorage
    Author: Peter Ekwere
"""
import models
from models.base_model import Base
from models.user import User
import os
from os import getenv
from sqlalchemy import create_engine, and_, func, or_, distinct, select
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import DatabaseError
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta


classes = {"user": User}


class DBStorage:
    """ This class interacts with the MySQL database"""
    
    #"postgresql://peter:V5JDxR2YzTAJA2YMLWYLPlEmfJABbb7T@dpg-cojt800cmk4c73c3e4mg-a.oregon-postgres.render.com/wagerbrain_db_3i8j"
    def __init__(self):
        """Instantiate a DBStorage object"""
        Deluxe_MYSQL_USER = getenv('Deluxe_MYSQL_USER')
        Deluxe_MYSQL_PWD = getenv('Deluxe_MYSQL_PWD')
        Deluxe_MYSQL_HOST = getenv('Deluxe_MYSQL_HOST')
        Deluxe_MYSQL_DB = getenv('Deluxe_MYSQL_DB')
        self.__engine = create_engine(
                                      'mysql+mysqldb://{}:{}@{}/{}'.format(Deluxe_MYSQL_USER,
                                             Deluxe_MYSQL_PWD,
                                             Deluxe_MYSQL_HOST,
                                             Deluxe_MYSQL_DB), pool_recycle=280)
        #self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self.__engine)
        self.__session = None
        
    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
                DBSession = sessionmaker(bind=self.__engine, expire_on_commit=False)
                Session = scoped_session(DBSession)
                self.__session = Session
        return self.__session
    
    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self._session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + f"{obj.id}"
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self._session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        try:
            #print("\ni am in db save method\n")
            self._session.commit()
        except DatabaseError as e:
            self._session.rollback()
            raise e

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        #print("\nI am in db delete method \n")
        if obj is not None:
            self._session.delete(obj)
            self._session.commit()
            
    def close(self):
        """call remove() method on the private session attribute"""
        self._session.close()

    def reload(self):
        """reloads data from the database"""
        self._session()
        #Base.metadata.create_all(self.__engine)
        #sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        #Session = scoped_session(sess_factory)
        #self.__session = Session

    def find_by(self, object: str, **kwd: Dict) -> User:
        """ THis method finds users by keyworded arguments

        Returns:
            User: _description_
        """
        a_class = classes.get(object)
        try:
            obj = self._session.query(a_class).filter_by(**kwd).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        #print(f"\n findby was called and user id is {obj.id} and its type is {type(obj.id).__name__}")
        return obj
    
    def update_user(self, user_id: int, **kwd: Dict):
        """ THis method updates a user

        Args:
            user_id (int): this is the user id
        """
        user = self.find_by("user", id=user_id)
        if user_id != user.id:
            raise ValueError
        for key, value in kwd.items():
            setattr(user, key, value)
        self.save()
            
    def add_user(self, username: str, email: str, hashed_password: str, PhoneNumber: str,  role: str) -> User:
        """ This method takes an email and hashed_password
        And returns a user object

        Args:
            email (str): This is a user's email
            hashed_password (str): This is a user's hashed password

        Returns:
            User: THis is the created user object
        """
        new_user = User(email=email,
                        username=username,
                        hashed_password=hashed_password,
                        PhoneNumber=PhoneNumber,
                        role=role)
        try:
            self.new(new_user)
            self.save()
        except DatabaseError:
            pass
        #self._session.add(new_user)
        #self._session.commit()
        return new_user