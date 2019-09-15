PEOPLE_CSV = 'allocation/normalisation_output.csv'

import pandas as pd;
from utils import randomStringDigits;
from jersey_bidder import create_app, db, models
from jersey_bidder.models import *
from sqlalchemy import or_

mapping_headers = {
    "year": "Year of Study",
    "name": "Full Name",
    "room_number": "Room Number",
    "gender": "Gender",
    "is_captain": "Are you Captain of a Sport",
    "representing_sports_ivp": "Have you represented NUS (SUNIG/IVP) in the following sports:",
    "sports_currently_in": "Sports you are currently in (after latest cut)",
    "total_points": "total_points",
    "email": "Email Address"
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
            if (currentGenderName == "male"):
                currentGender_id = 1
            elif (currentGenderName == "female"):
                currentGender_id = 2
            currentEmail = entry[str(mapping_headers["email"])]
            currentPassword = randomStringDigits()
            currentUser = User(name = currentName, roomNumber = currentRoomNumber, year = currentYear, points = currentPoints, 
                        email = currentEmail, password = currentPassword, gender_id = currentGender_id)
            
            # add user sports
            currentUserSportList = []
            currentUserSports = entry[str(mapping_headers["sports_currently_in"])].split(';')
            for currentUser_SportName in currentUserSports:
                currentUser_SportName = currentUser_SportName.strip()
                sport_ToAdd = Sport.query.filter((Sport.gender_id == 3) | (Sport.gender_id == currentGender_id)) \
                        .filter(Sport.sportName == currentUser_SportName).first()
                currentUser.sports.append(sport_ToAdd)

            db.session.add(currentUser)

        db.session.commit()

        #alter below code to your own testing for choices
        for i in range(6):
            currentDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            currentChoice = Choice(submitDatetime = currentDatetime, firstChoice = 1, secondChoice = 2, thirdChoice = 3, fourthChoice = 4, fifthChoice = 5,
                user_id = i + 1)
            db.session.add(currentChoice)
        db.session.commit()

if __name__ == "__main__":
    loadRealData(create_app())