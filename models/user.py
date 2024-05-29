#!/usr/bin/env python3
"""
    This Module Contains a a User Model
    Author: Peter Ekwere
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, JSON
from flask_login import UserMixin

class User(Base, UserMixin, BaseModel):
    """
    Representation of a user
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    hashed_password = Column(String(250), nullable=False)
    role = Column(String(20), nullable=True, default='regular')
    reset_token = Column(String(250), nullable=True)
    is_active = Column(Boolean, default=True)
    demo_balance = Column(Float, nullable=False, default=0.0)
    live_balance = Column(Float, nullable=False, default=0.0)
    # 2 - KYC verification data
    kyc_data = Column(JSON, nullable=True)  # Store KYC data as a JSON object (ssn, id number, etc.)
    is_kyc_approved = Column(Boolean, nullable=True, default=False)  # Indicate if KYC is approved
    # 3 - List of login details (unhashed)
    login_history = Column(JSON, nullable=True)  # Store login details as a JSON list
    # 4 & 5 - Admin approval and ban indicators
    is_banned = Column(Boolean, nullable=True, default=False)  # Indicate if the user is banned
    
    
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
    
    @property
    def is_authenticated(self):
        return self.is_active
    
    #@property
    #def role(self):
    #    return self.role
    
    def get_id(self):
        #print(f"get id was called and it is {self.id} and its type is {type(self.id).__name__}")
        return str(self.id)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"