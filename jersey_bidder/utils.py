from jersey_bidder.models import User

def getUser(FlaskUser):
    """Returns User Model From FlaskUser"""
    return User.query.filter(User.flaskUser_id == FlaskUser.id).first()
