import os

from flask import Flask
from jersey_bidder.config import Config
from jersey_bidder.extensions import db, Bootstrap, admin, ModelView, login_manager
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from jersey_bidder.models import User, Choice, JerseyNumber, Gender, UserSports, Sport, FlaskUser
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    #pass our web app to the extension packages
    db.init_app(app)
    admin.init_app(app)
    bootstrap = Bootstrap(app)
    user_manager = UserManager(app, db, FlaskUser)
    
    
    #import the routes as classes and register these blueprints into the flask app
    from jersey_bidder.main.routes import main
    from jersey_bidder.user.routes import user
    from jersey_bidder.numbers.routes import numbers
    from jersey_bidder.useradmin.routes import useradmin

    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(numbers)
    app.register_blueprint(useradmin)

    #initialize admin view pages so we can view things in the admin interface
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Choice, db.session))
    admin.add_view(ModelView(JerseyNumber, db.session))
    admin.add_view(ModelView(Gender, db.session))
    admin.add_view(ModelView(UserSports, db.session))
    admin.add_view(ModelView(Sport, db.session))

    return app