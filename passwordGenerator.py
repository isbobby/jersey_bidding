# generate username and password for every user
# create bogus username if no room space provided

ALL_RESIDENT_XLSX = 'ResidentList.xlsx'
DUMMY_ROOM_NUMBER = 'X/9/999-9'
import pandas as pd;
from utils import randomStringDigits;

mapping_headers = {
    "name": "Name Preferred",
    "room_number": "Room Space",
    "password": "Password",
    "username": "Username",
}

usernameList = []
passwordList = []
roomNumberList = []

def generateUsernameAndPassword():
    df = pd.read_excel(ALL_RESIDENT_XLSX)

    for index, entry in df.iterrows():
        if pd.isnull(entry[str(mapping_headers["room_number"])]):
            currentRoomNumber = DUMMY_ROOM_NUMBER
            currentUserName = entry[str(mapping_headers["name"])].lower().replace(" ", "")
        else:
            currentRoomNumber = entry[str(mapping_headers["room_number"])][3:]
            currentUserName = currentRoomNumber
        
        currentPassword = randomStringDigits()

        usernameList.insert(index, currentUserName)
        passwordList.insert(index, currentPassword)
        roomNumberList.insert(index, currentRoomNumber)

    df["Room Space"] = roomNumberList
    df["Username"] = usernameList
    df["Password"] = passwordList

    df.to_csv('ResidentPassword.csv', sep=',')
    df.to_excel('ResidentPassword.xlsx')

if __name__ == "__main__":
    generateUsernameAndPassword()


