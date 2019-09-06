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
        mixed = Gender(genderName = "Mixed")
        db.session.add(male)
        db.session.add(female)
        db.session.add(mixed)

        # Add sports
        frisbee = Sport(sportName = "Frisbee_Mixed", gender=mixed)
        Softball = Sport(sportName = "Softball_Mixed", gender=mixed)
        Takraw_Male  = Sport(sportName = "Takraw_Male", gender=male)
        Netball_Female = Sport(sportName = "Netball_Female", gender=female)
        Tennis_Male = Sport(sportName = "Tennis_Male", gender=male)
        Tennis_Female = Sport(sportName = "Tennis_Female", gender=female)
        Floorball_Male = Sport(sportName = "Floorball_Male", gender=male)
        Floorball_Female = Sport(sportName = "Floorball_Female", gender=female)
        Squash_Male = Sport(sportName = "Squash_Male", gender=male)
        Squash_Female = Sport(sportName = "Squash_Female", gender=female)
        Badminton_Male = Sport(sportName = "Badminton_Male", gender=male)
        Badminton_Female = Sport(sportName = "Badminton_Female", gender=female)
        Soccer_Male = Sport(sportName = "Soccer_Male", gender=male)
        Soccer_Female = Sport(sportName = "Soccer_Female", gender=female)
        TableTennis_Male = Sport(sportName = "TableTennis_Male", gender=male)
        TableTennis_Female = Sport(sportName = "TableTennis_Female", gender=female)
        Handball_Male = Sport(sportName = "Handball_Male", gender=male)
        Handball_Female = Sport(sportName = "Handball_Female", gender=female)
        RoadRelay_Male = Sport(sportName = "RoadRelay_Male", gender=male)
        RoadRelay_Female = Sport(sportName = "RoadRelay_Female", gender=female)
        Basketball_Male = Sport(sportName = "Basketball_Male", gender=male)
        Basketball_Femal = Sport(sportName = "Basketball_Female", gender=female)
        Swim_Male = Sport(sportName = "Swim_Male", gender=male)
        Swim_Female = Sport(sportName = "Swim_Female", gender=female)
        TouchRugby_Male = Sport(sportName = "TouchRugby_Male", gender=male)
        TouchRugby_Female = Sport(sportName = "TouchRugby_Female", gender=female)
        Track_Male = Sport(sportName = "Track_Male", gender=male)
        Track_Female = Sport(sportName = "Track_Female", gender=female)
        Volleyball_Male = Sport(sportName = "Volleyball_Male", gender=male)
        Volleyball_Female = Sport(sportName = "Volleyball_Female", gender=female)
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