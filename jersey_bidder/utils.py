from jersey_bidder.models import User, FlaskUser

def getUser(FlaskUser):
    """Returns User Model From FlaskUser"""
    return User.query.filter(User.flaskUser_id == FlaskUser.id).first()
<<<<<<< HEAD

def getFlaskUser(User):
    return FlaskUser.query.filter(FlaskUser.id==User.flaskUser_id).first()
=======
>>>>>>> 6a9e72c94cefa160f4245c68aa2e27201f0e5440
