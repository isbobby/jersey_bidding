from jersey_bidder import create_app, db
from jersey_bidder.models import *

def setUp(app):
    with app.app_context():
        # drop all tables first
        Choice.__table__.drop(db.engine)
        UserSports.__table__.drop(db.engine)
        Sport.__table__.drop(db.engine)
        User.__table__.drop(db.engine)
        JerseyNumber.__table__.drop(db.engine)
        Gender.__table__.drop(db.engine)
        db.create_all() 

        #add Gender
        male = Gender(genderName = "Male")
        female = Gender(genderName = "Female")
        mixed = Gender(genderName = "Mixed")
        db.session.add(male)
        db.session.add(female)
        db.session.add(mixed)

        # Add sports
        frisbee = Sport(sportName = "Frisbee_Mixed", Gender=mixed)
        Softball = Sport(sportName = "Softball_Mixed", Gender=mixed)
        Takraw_Male  = Sport(sportName = "Takraw_Male", Gender=male)
        Netball_Female = Sport(sportName = "Netball_Female", Gender=female)
        Tennis_Male = Sport(sportName = "Tennis_Male", Gender=male)
        Tennis_Female = Sport(sportName = "Tennis_Female", Gender=female)
        Floorball_Male = Sport(sportName = "Floorball_Male", Gender=male)
        Floorball_Female = Sport(sportName = "Floorball_Female", Gender=female)
        Squash_Male = Sport(sportName = "Squash_Male", Gender=male)
        Squash_Female = Sport(sportName = "Squash_Female", Gender=female)
        Badminton_Male = Sport(sportName = "Badminton_Male", Gender=male)
        Badminton_Female = Sport(sportName = "Badminton_Female", Gender=female)
        Soccer_Male = Sport(sportName = "Soccer_Male", Gender=male)
        Soccer_Female = Sport(sportName = "Soccer_Female", Gender=female)
        TableTennis_Male = Sport(sportName = "TableTennis_Male", Gender=male)
        TableTennis_Female = Sport(sportName = "TableTennis_Female", Gender=female)
        Handball_Male = Sport(sportName = "Handball_Male", Gender=male)
        Handball_Female = Sport(sportName = "Handball_Female", Gender=female)
        RoadRelay_Male = Sport(sportName = "RoadRelay_Male", Gender=male)
        RoadRelay_Female = Sport(sportName = "RoadRelay_Female", Gender=female)
        Basketball_Male = Sport(sportName = "Basketball_Male", Gender=male)
        Basketball_Femal = Sport(sportName = "Basketball_Female", Gender=female)
        Swim_Male = Sport(sportName = "Swim_Male", Gender=male)
        Swim_Female = Sport(sportName = "Swim_Female", Gender=female)
        TouchRugby_Male = Sport(sportName = "TouchRugby_Male", Gender=male)
        TouchRugby_Female = Sport(sportName = "TouchRugby_Female", Gender=female)
        Track_Male = Sport(sportName = "Track_Male", Gender=male)
        Track_Female = Sport(sportName = "Track_Female", Gender=female)
        Volleyball_Male = Sport(sportName = "Volleyball_Male", Gender=male)
        Volleyball_Female = Sport(sportName = "Volleyball_Female", Gender=female)
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