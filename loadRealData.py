PEOPLE_CSV = 'allocation/normalisation_output.csv'

import pandas as pd;
from utils import randomStringDigits;
from jersey_bidder import create_app, db, models
from jersey_bidder.models import *
import random

mapping_headers = {
    "year": "Years of IHG",
    "name": "Full Name",
    "room_number": "Room Number",
    "gender": "Gender",
    "is_captain": "Are you Captain of a Sport",
    "representing_sports_ivp": "Have you represented NUS (SUNIG/IVP) in the following sports:",
    "sports_currently_in": "Sports you are currently in (after latest cut, separate by ;)",
    "total_points": "total_points",
    "email": "Email Address",
    "password": "Password",
    "username": "Username",
}

def loadRealData(app):
    """loads user data to database from normalisation_output.csv """
    with app.app_context():
        df = pd.read_csv(PEOPLE_CSV, dtype=str).fillna('')
        for index, entry in df.iterrows():
            # add current user
            currentName = entry[str(mapping_headers["name"])]
            currentRoomNumber = entry[str(mapping_headers["room_number"])]
            currentYear = int(entry[str(mapping_headers["year"])])
            currentPoints = int(entry[str(mapping_headers["total_points"])])
            currentGender_id = 0
            currentGenderName = entry[str(mapping_headers["gender"])].strip().lower()
            if (currentGenderName == "m"):
                currentGender_id = 1
            elif (currentGenderName == "f"):
                currentGender_id = 2

            currentWantUniqueNumber = False
            if currentYear >= 2:
                currentWantUniqueNumber = True

            currentUsername = entry[str(mapping_headers["username"])]
            currentPassword = entry[str(mapping_headers["password"])]

            # create flaskUser First with Bidder Role
            currentFlaskUser = FlaskUser(username=currentUsername, password=currentPassword)

            currentUser = User(name = currentName, roomNumber = currentRoomNumber, year = currentYear, 
                    points = currentPoints, gender_id = currentGender_id, flaskUser=currentFlaskUser, wantUniqueNumber=currentWantUniqueNumber)
            
            # add user sports
            currentUserSportList = []
            currentUserSports = entry[str(mapping_headers["sports_currently_in"])].split(';')
            for currentUser_SportName in currentUserSports:
                currentUser_SportName = currentUser_SportName.strip()
                sport_ToAdd = Sport.query.filter((Sport.gender_id == 3) | (Sport.gender_id == currentGender_id)) \
                        .filter(Sport.sportName == currentUser_SportName).first()
                if sport_ToAdd:
                    currentUser.sports.append(sport_ToAdd)

            db.session.add(currentUser)

        db.session.commit()

        #alter below code to your own testing for choices
        for i in range(502):
            currentDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            currentFirstChoice = random.randint(1, 99)
            currentSecondChoice = random.randint(1, 99)
            currentThirdChoice = random.randint(1, 99)
            currentFourthChoice = random.randint(1, 99)
            currentFifthChoice = random.randint(1, 99)
            currentChoice = Choice(submitDatetime = currentDatetime, firstChoice = currentFirstChoice, 
                secondChoice = currentSecondChoice, thirdChoice = currentThirdChoice, fourthChoice = currentFourthChoice, fifthChoice = currentFifthChoice,
                user_id = i + 1)
            db.session.add(currentChoice)
        db.session.commit()

if __name__ == "__main__":
    loadRealData(create_app())