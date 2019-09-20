from jersey_bidder.models import User, FlaskUser, FlaskUserRoles

def getUser(FlaskUser):
    """Returns User Model From FlaskUser"""
    return User.query.filter(User.flaskUser_id == FlaskUser.id).first()

def getFlaskUser(User):
    return FlaskUser.query.filter(FlaskUser.id==User.flaskUser_id).first()

def getFlaskUserRole(FLaskUser):
    return FlaskUserRoles.query.filter(FlaskUserRoles.user_id==FlaskUser.id).first()
