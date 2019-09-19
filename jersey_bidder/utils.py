from jersey_bidder.models import User, FlaskUser

def getUser(FlaskUser):
    """Returns User Model From FlaskUser"""
    return User.query.filter(User.flaskUser_id == FlaskUser.id).first()

def getFlaskUser(User):
    return FlaskUser.query.filter(FlaskUser.id==User.flaskUser_id).first()