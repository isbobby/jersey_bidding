import os

from flask import Flask

from flask_login import LoginManager
from jersey_bidder.config import Config
from flask_bootstrap import Bootstrap

from jersey_bidder.extensions import mongo

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    #db.init_app(app)
    #from jersey_bidder.models import CombinedList
    #admin.add_view(ModelView(CombinedList, db.session))

    from jersey_bidder.main.routes import main
    app.register_blueprint(main)

    return app