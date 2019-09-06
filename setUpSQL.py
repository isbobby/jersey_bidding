from jersey_bidder import create_app, db
from jersey_bidder.models import *

def setUp(app):
    with app.app_context():
        # drop all tables first
        db.drop_all()
        db.create_all() 

        #add Gender
        male = Gender(genderName = "Male")
        female = Gender(genderName = "Female")
        db.session.add(male)
        db.session.add(female)

        # Add sports
        frisbee = Sport(sportName = "Frisbee_Mixed")
        Softball = Sport(sportName = "Softball_Mixed")
        Takraw_Male  = Sport(sportName = "Takraw_Male")
        Netball_Female = Sport(sportName = "Netball_Female")
        Tennis_Male = Sport(sportName = "Tennis_Male")
        Tennis_Female = Sport(sportName = "Tennis_Female")
        Floorball_Male = Sport(sportName = "Floorball_Male")
        Floorball_Female = Sport(sportName = "Floorball_Female")
        Squash_Male = Sport(sportName = "Squash_Male")
        Squash_Female = Sport(sportName = "Squash_Female")
        Badminton_Male = Sport(sportName = "Badminton_Male")
        Badminton_Female = Sport(sportName = "Badminton_Female")
        Soccer_Male = Sport(sportName = "Soccer_Male")
        Soccer_Female = Sport(sportName = "Soccer_Female")
        TableTennis_Male = Sport(sportName = "TableTennis_Male")
        TableTennis_Female = Sport(sportName = "TableTennis_Female")
        Handball_Male = Sport(sportName = "Handball_Male")
        Handball_Female = Sport(sportName = "Handball_Female")
        RoadRelay_Male = Sport(sportName = "RoadRelay_Male")
        RoadRelay_Female = Sport(sportName = "RoadRelay_Female")
        Basketball_Male = Sport(sportName = "Basketball_Male")
        Basketball_Femal = Sport(sportName = "Basketball_Femal")
        Swim_Male = Sport(sportName = "Swim_Male")
        Swim_Female = Sport(sportName = "Swim_Female")
        TouchRugby_Male = Sport(sportName = "TouchRugby_Male")
        TouchRugby_Female = Sport(sportName = "TouchRugby_Female")
        Track_Male = Sport(sportName = "Track_Male")
        Track_Female = Sport(sportName = "Track_Female")
        Volleyball_Male = Sport(sportName = "Volleyball_Male")
        Volleyball_Female = Sport(sportName = "Volleyball_Female")
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
            if i > 99:
                currentGender = female
            currentJersey = JerseyNumber(number = i, isTaken = False, gender = currentGender) 
            db.session.add(currentJersey)

        db.session.commit()