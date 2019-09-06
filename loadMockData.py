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
            currentRoomNumber = integerToBlock(i % 5) + str(i)
            currentYear = (i % 4) + 1
            currentPoints = i
            currentEmail = "dummyEmail" + str(i) + "@gmail.com"
            currentPassword = "dummyPassword" + str(i)
            currentGender_id = i % 2 + 1
            currentPreference_id = 0
            if currentGender_id  == 1:
                # is a male
<<<<<<< HEAD
                currentPreference_id = random.radint(0, 99)
            else :
                currentPreference_id = random.radint(100, 199)
=======
                currentPreference_id = random.randint(1, 100)
            else :
                currentPreference_id = random.randint(101, 200)
>>>>>>> 0433895f4e9915fb2b1f6157a9461774fbce6267

            currentUser = User(roomNumber = currentRoomNumber, year = currentYear, points = currentPoints, 
                    email = currentEmail, password = currentPassword, gender_id = currentGender_id, preference_id=currentPreference_id)
            db.session.add(currentUser)

            # create sports
            maleSport_id = [entries.id for entries in Sport.query.filter(Sport.gender_id == 1 or Sport.gender_id == 3)]
            femaleSport_id = [entries.id for entries in Sport.query.filter(Sport.gender_id == 2 or Sport.gender_id == 3)]
        
        #mock their choices

        db.session.commit()

# setup database with base data
setUp(currentApp)
# load mock data
loadMockData(currentApp)