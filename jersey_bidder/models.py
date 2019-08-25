from flask import current_app
from jersey_bidder import db
from flask_login import UserMixin
from datetime import datetime

class combinedUser(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    roomNumber = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    #password is hashed
    password = db.Column(db.String(60), nullable=False)




#To do in documentation! initialize/changing databse models:
"""
1. python3 
2. from jersey_bidder import create_app, db
3. create an app: app = create_app()
4. run:
    with app.app_context():
        db.create_all()
5. this creates a new relation in the specified DB 
6. quit() to leave the python3 interpretor
"""

    

    
