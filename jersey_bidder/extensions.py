#this file imports extensions and initialize for __init__.py
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager,login_user

#initialize db, SQLAlchemy is a convenient python extension to help manage database
db = SQLAlchemy()

#mongo: more description needed (bobby doesn't know what tf is mongo)
mongo = PyMongo()

#initialize admin: this gives us an admin interface to manage database entries
admin = Admin()

#initialize login manager
login_manager = LoginManager()
