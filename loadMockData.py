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

        #assume 400 eusoffians
        for i in range(400):
            # create dummy user
            currentRoomNumber = integerToBlock(i % 5) + str(i)
            currentYear = (i % 4) + 1
            currentPoints = i
            currentEmail = "dummyEmail" + str(i) + "@gmail.com"
            currentPassword = "dummyPassword" + str(i)
            currentGender_id = i % 2 + 1

            currentUser = User(roomNumber = currentRoomNumber, year = currentYear, points = currentPoints, 
                    email = currentEmail, password = currentPassword, gender_id = currentGender_id)
            db.session.add(currentUser)

        db.session.commit()

# setup database with base data
setUp(currentApp)
# load mock data
loadMockData(currentApp)