from jersey_bidder import create_app, db
from jersey_bidder.models import *
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin

def setUp(app):
    with app.app_context():
        #drop all tables first
        UserSports.__table__.drop(db.engine)
        Sport.__table__.drop(db.engine)
        Choice.__table__.drop(db.engine)
        User.__table__.drop(db.engine)
        JerseyNumber.__table__.drop(db.engine)
        Gender.__table__.drop(db.engine) 
        Admin.__table__.drop(db.engine)
        FlaskUserRoles.__table__.drop(db.engine)
        FlaskUser.__table__.drop(db.engine)
        Role.__table__.drop(db.engine)
        db.create_all() 

        admin = Role(name='Admin')
        bidder = Role(name='Bidder')
        db.session.add(admin)
        db.session.add(bidder)

        # Create Admin Account For Hackers
        flaskUserHacker = FlaskUser(email='eusoffhacker@gmail.com', username='eusoffhacker', password='noshady')
        flaskUserHacker.roles.append(admin)
        hackerAdmin = Admin(name='The Master', flaskUser=flaskUserHacker)
        db.session.add(hackerAdmin)

        #add Gender
        male = Gender(genderName = "Male")
        female = Gender(genderName = "Female")
        mixed = Gender(genderName = "Mixed")
        db.session.add(male)
        db.session.add(female)
        db.session.add(mixed)

        # Add sports
        frisbee = Sport(sportName = "Frisbee", Gender=mixed)
        Softball = Sport(sportName = "Softball", Gender=mixed)
        Takraw_Male  = Sport(sportName = "Takraw", Gender=male)
        Netball_Female = Sport(sportName = "Netball", Gender=female)
        Tennis_Male = Sport(sportName = "Tennis", Gender=male)
        Tennis_Female = Sport(sportName = "Tennis", Gender=female)
        Floorball_Male = Sport(sportName = "Floorball", Gender=male)
        Floorball_Female = Sport(sportName = "Floorball", Gender=female)
        Squash_Male = Sport(sportName = "Squash", Gender=male)
        Squash_Female = Sport(sportName = "Squash", Gender=female)
        Badminton_Male = Sport(sportName = "Badminton", Gender=male)
        Badminton_Female = Sport(sportName = "Badminton", Gender=female)
        Soccer_Male = Sport(sportName = "Soccer", Gender=male)
        Soccer_Female = Sport(sportName = "Soccer", Gender=female)
        TableTennis_Male = Sport(sportName = "TableTennis", Gender=male)
        TableTennis_Female = Sport(sportName = "TableTennis", Gender=female)
        Handball_Male = Sport(sportName = "Handball", Gender=male)
        Handball_Female = Sport(sportName = "Handball", Gender=female)
        RoadRelay_Male = Sport(sportName = "RoadRelay", Gender=male)
        RoadRelay_Female = Sport(sportName = "RoadRelay", Gender=female)
        Basketball_Male = Sport(sportName = "Basketball", Gender=male)
        Basketball_Femal = Sport(sportName = "Basketball", Gender=female)
        Swim_Male = Sport(sportName = "Swim", Gender=male)
        Swim_Female = Sport(sportName = "Swim", Gender=female)
        TouchRugby_Male = Sport(sportName = "TouchRugby", Gender=male)
        TouchRugby_Female = Sport(sportName = "TouchRugby", Gender=female)
        Track_Male = Sport(sportName = "Track", Gender=male)
        Track_Female = Sport(sportName = "Track", Gender=female)
        Volleyball_Male = Sport(sportName = "Volleyball", Gender=male)
        Volleyball_Female = Sport(sportName = "Volleyball", Gender=female)
        db.session.add(frisbee)
        db.session.add(Softball)
        db.session.add(Takraw_Male)
        db.session.add(Netball_Female)
        db.session.add(Tennis_Male)
        db.session.add(Tennis_Female)
        db.session.add(Floorball_Male)
        db.session.add(Floorball_Female)
        db.session.add(Squash_Male)
        db.session.add(Squash_Female)
        db.session.add(Badminton_Male)
        db.session.add(Badminton_Female)
        db.session.add(Soccer_Male)
        db.session.add(Soccer_Female)
        db.session.add(TableTennis_Male)
        db.session.add(TableTennis_Female)
        db.session.add(Handball_Male)
        db.session.add(Handball_Female)
        db.session.add(RoadRelay_Male)
        db.session.add(RoadRelay_Female)
        db.session.add(Basketball_Male)
        db.session.add(Basketball_Femal)
        db.session.add(Swim_Male)
        db.session.add(Swim_Female)
        db.session.add(TouchRugby_Male)
        db.session.add(TouchRugby_Female)
        db.session.add(Track_Male)
        db.session.add(Track_Female)
        db.session.add(Volleyball_Male)
        db.session.add(Volleyball_Female)

        #add jersey numbers
        for i in range(200):
            currentGender = male
            currentNumber = i
            if i > 99:
                currentGender = female
                currentNumber = currentNumber - 100
            currentJersey = JerseyNumber(number = currentNumber, isTaken = False, gender = currentGender) 
            db.session.add(currentJersey)

        db.session.commit()

if __name__ == "__main__":
    setUp(create_app())