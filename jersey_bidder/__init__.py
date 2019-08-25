import os

from flask import Flask
from jersey_bidder.config import Config
from jersey_bidder.extensions import db, Bootstrap, admin, ModelView

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    #pass our web app to the extension packages
    db.init_app(app)
    admin.init_app(app)
    bootstrap = Bootstrap(app)

    #import the routes as classes and register these blueprints into the flask app
    from jersey_bidder.main.routes import main
    app.register_blueprint(main)

    #import all DB models
    from jersey_bidder.models import combinedUser

    #initialize admin view pages so we can view things in the admin interface
    admin.add_view(ModelView(combinedUser, db.session))

    return app