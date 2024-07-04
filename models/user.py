#!/usr/bin/env python3
"""
    This Module Contains a a User Model
    Author: Peter Ekwere
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime

class User(Base, UserMixin, BaseModel):
    """
    Representation of a user
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    first_name = Column(String(80), unique=True, nullable=True)
    last_name = Column(String(80), unique=True, nullable=True)
    PhoneNumber = Column(String(20), nullable=True, default="0")
    address = Column(String(2000), nullable=True)
    city = Column(String(250), nullable=True)
    state = Column(String(250), nullable=True)
    zipcode = Column(String(80), nullable=True)
    hashed_password = Column(String(250), nullable=False)
    role = Column(String(20), nullable=True, default='regular')
    gender = Column(String(20), nullable=True)
    profile_photo = Column(JSON, nullable=True)
    reset_token = Column(String(250), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    demo_balance = Column(Float, nullable=False, default=2000.0)
    live_balance = Column(Float, nullable=False, default=0.0)
    switch_check = Column(String(50), nullable=True, default='demo')
    default_wallet = Column(String(50), nullable=True, default='Bitcoin_Cash')
    usd_value = Column(Float, nullable=False, default=0.0)
    eth_balance = Column(Float, nullable=False, default=0.0)
    usdt_balance = Column(Float, nullable=False, default=1000.0)
    btc_balance = Column(Float, nullable=False, default=0.0)
    sol_balance = Column(Float, nullable=False, default=0.0)
    Bitcoin_Cash = Column(Float, nullable=False, default=0.0)
    Tether_USD = Column(Float, nullable=False, default=0.0)
    Dogecoin = Column(Float, nullable=False, default=0.0)
    Ripple = Column(Float, nullable=False, default=0.0)
    Polkadot = Column(Float, nullable=False, default=0.0)
    Cardano = Column(Float, nullable=False, default=0.0)
    xlm_balance = Column(Float, nullable=False, default=0.0)
    stellar_balance = Column(Float, nullable=False, default=0.0)
    chainlink = Column(Float, nullable=False, default=0.0)
    live_eth_balance = Column(Float, nullable=False, default=0.0)
    live_usdt_balance = Column(Float, nullable=False, default=1000.0)
    live_btc_balance = Column(Float, nullable=False, default=0.0)
    live_sol_balance = Column(Float, nullable=False, default=0.0)
    live_Bitcoin_Cash = Column(Float, nullable=False, default=0.0)
    live_Tether_USD = Column(Float, nullable=False, default=0.0)
    live_Dogecoin = Column(Float, nullable=False, default=0.0)
    live_Ripple = Column(Float, nullable=False, default=0.0)
    live_Polkadot = Column(Float, nullable=False, default=0.0)
    live_Cardano = Column(Float, nullable=False, default=0.0)
    live_xlm_balance = Column(Float, nullable=False, default=0.0)
    live_stellar_balance = Column(Float, nullable=False, default=0.0)
    live_chainlink = Column(Float, nullable=False, default=0.0)
    demo_open_positions = Column(JSON, nullable=True)  # Store open positions as a JSON list
    demo_closed_positions = Column(JSON, nullable=True)  # Store closed positions as a JSON list
    demo_earnings = Column(JSON, nullable=True)
    live_open_positions = Column(JSON, nullable=True)  # Store open positions as a JSON list
    live_closed_positions = Column(JSON, nullable=True)  # Store closed positions as a JSON list
    live_earnings = Column(JSON, nullable=True)
    kyc_data = Column(JSON, nullable=True)
    payment_proof = Column(JSON, nullable=True)
    is_kyc_approved = Column(Boolean, nullable=True, default=False)
    login_history = Column(JSON, nullable=True)  # Store login details as a JSON list
    # 4 & 5 - Admin approval and ban indicators
    is_banned = Column(Boolean, nullable=True, default=False)  # Indicate if the user is banned
    
    
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
    
    @property
    def is_authenticated(self):
        return self.is_active
    
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"