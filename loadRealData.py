PEOPLE_CSV = 'allocation/normalisation_output.csv'

import pandas as pd;
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
    "total_points": "total_points"
}

def loadRealData(app):
    with app.app_context():
        df = pd.read_csv(PEOPLE_CSV, dtype=str).fillna('')
        for index, entry in df.iterrows():

            # adding current user
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
            currentEmail = "dummyEmail" + str(index) + "@gmail.com"
            currentPassword = "dummyPassword" + str(index)
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

if __name__ == "__main__":
    loadRealData(create_app())