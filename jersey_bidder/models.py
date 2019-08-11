from flask import current_app
from jersey_bidder import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 

class CombinedList (db.Model):
    __table_args__ = {'extend_existing': True} 
    roomnumber = db.Column(db.String(10), primary_key=True, unique=True)
    points = db.Column(db.integer, nullable=False)
    
