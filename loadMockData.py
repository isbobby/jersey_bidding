from jersey_bidder import create_app, db, models
from jersey_bidder.models import *
from setUpSQL import setUp
import random

currentApp = create_app()

def integerToBlock(x):
    if (x == 0):
        return "A"
    elif (x == 1): 
        return "B"
    elif (x == 2):
        return "C"
    elif (x == 3):
        return "D"
    else:
        return "E"

def loadMockData(app):
    with app.app_context():
        # MOCK DATA FOR TESTING

        #mock 400 eusoffians
        for i in range(400):
            # create dummy user
            currentName = "dummyUser_" + str(i)
            currentRoomNumber = integerToBlock(i % 5) + str(i)
            currentYear = (i % 4) + 1
            currentPoints = i
            currentEmail = "dummyEmail" + str(i) + "@gmail.com"
            currentPassword = "dummyPassword" + str(i)
            currentGender_id = i % 2 + 1
            currentPreference_id = 0
            if currentGender_id  == 1:
                # is a male
                currentPreference_id = random.randint(1, 100)
            else :
                currentPreference_id = random.randint(101, 200)

            currentUser = User(name = currentName, roomNumber = currentRoomNumber, year = currentYear, points = currentPoints, 
                    email = currentEmail, password = currentPassword, gender_id = currentGender_id, preference_id=currentPreference_id)

            # create sports
            maleSports = Sport.query.filter((Sport.gender_id == 1) | (Sport.gender_id == 3)).all()
            femaleSports = Sport.query.filter((Sport.gender_id == 2) or (Sport.gender_id == 3))
            dummySportsToAdd = []
            if currentUser.gender_id == 1:
                dummySportsToAdd = random.sample(list(maleSports), k=2)
            if currentUser.gender_id == 2:
                dummySportsToAdd = random.sample(list(femaleSports), k=2)
            for dummySport in dummySportsToAdd:
                currentUser.sports.append(dummySport)

            db.session.add(currentUser)

        db.session.commit()

# setup database with base data
setUp(currentApp)
# load mock data
loadMockData(currentApp)