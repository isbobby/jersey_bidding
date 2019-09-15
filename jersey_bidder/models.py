from flask import current_app
from jersey_bidder import db
from flask_login import UserMixin
from datetime import datetime

class Admin(db.Model):
    __tablename__ = 'admin'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)

    adminLoginID = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    roomNumber = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Foreign key constraints (only can have one)
    gender_id = db.Column(db.Integer, db.ForeignKey(
        'gender.id'), nullable=False)
    preference_id = db.Column(db.Integer, db.ForeignKey('jerseyNumber.id'))
    jerseyNumber_id = db.Column(db.Integer, db.ForeignKey('jerseyNumber.id'))
    # choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'))

    # Relationships
    gender = db.relationship('Gender', back_populates="User")
    choice = db.relationship('Choice', back_populates='user', uselist=False, lazy=True)
    sports = db.relationship('Sport', secondary='userSports', lazy=True)
    jerseyNumber = db.relationship('JerseyNumber', foreign_keys=[jerseyNumber_id], backref='users', lazy=True)
    preference = db.relationship('JerseyNumber', foreign_keys=[preference_id], backref='users_preference', lazy=True)

class Gender(db.Model):
    __tablename__ = 'gender'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    genderName = db.Column(db.String(10), nullable=False)

    # Relationships
    User = db.relationship('User', back_populates="gender", lazy=True)
    JerseyNumber = db.relationship('JerseyNumber')


class Choice(db.Model):
    __tablename__ = 'choice'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    submitDatetime = db.Column(db.DateTime, nullable=False)
    firstChoice = db.Column(db.Integer, nullable=False)
    secondChoice = db.Column(db.Integer, nullable=False)
    thirdChoice = db.Column(db.Integer, nullable=False)
    fourthChoice = db.Column(db.Integer, nullable=False)
    fifthChoice = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='choice', lazy=True)

class Sport(db.Model):
    __tablename__ = 'sport'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    sportName = db.Column(db.String(100), nullable=False)

    # foreign key constraints
    gender_id = db.Column(db.Integer, db.ForeignKey(
        'gender.id'), nullable=False)

    # relationships
    Users = db.relationship('User', secondary='userSports')
    Gender = db.relationship('Gender', backref="Sport")

# UserSports is a junction table between Sport and User


class UserSports(db.Model):
    __tablename__ = 'userSports'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)

    # foreign key constraints
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# male 0-99 female 100-199 (100 bias for female)


class JerseyNumber(db.Model):
    __tablename__ = 'jerseyNumber'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    isTaken = db.Column(db.Boolean, default=False, nullable=False)

    # foreign key constraint
    gender_id = db.Column(db.Integer, db.ForeignKey(
        'gender.id'), nullable=False)

    # relationship
    gender = db.relationship('Gender', back_populates="JerseyNumber")
