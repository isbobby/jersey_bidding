from jersey_bidder.models import *
from jersey_bidder import db
import random


def UserPlayMixedSport(user):
    mixedSports = Sport.query.filter(Sport.gender_id == 3).all()
    mixedSportsSet = set(mixedSports)
    userSportsSet = set(user.sports)
    return bool(userSportsSet.intersection(mixedSportsSet))


def UserSportClash(user1, user2):
    """check user1 and user2 have any sports that are the same, returns true if they have a clash"""
    user1Sports = User.query.get(user1.id).sports
    user2Sports = User.query.get(user2.id).sports
    user1SportsSet = set(user1Sports)
    user2SportsSet = set(user2Sports)
    return bool(user1SportsSet.intersection(user2SportsSet))


def getOppositeGenderID(user):
    userGenderID = user.gender_id
    if userGenderID == 1:
        return 2
    elif userGenderID == 2:
        return 1


def validateChoiceAvailable(desiredNumber, user):
    # check if isTaken
    desiredJersey = JerseyNumber.query.filter((JerseyNumber.gender_id == user.gender_id) & (
        JerseyNumber.number == desiredNumber)).first()
    desiredNumberIsTaken = desiredJersey.isTaken

    if desiredNumberIsTaken:
        return False

    # check with the users of this number if there are conflicts
    UsersWithDesiredNumber = desiredJersey.users

    if UserPlayMixedSport(user):
        # check clash with opposite gender users
        oppositeGenderID = getOppositeGenderID(user)
        desiredJerseyOppositeGender = JerseyNumber.query.filter(
            (JerseyNumber.gender_id == oppositeGenderID) & (JerseyNumber.number == desiredNumber)).first()
        for otherUser in desiredJerseyOppositeGender.users:
            hasClashingSport = UserSportClash(user, otherUser)
            if hasClashingSport:
                return False

    for otherUser in UsersWithDesiredNumber:
        hasClashingSport = UserSportClash(user, otherUser)
        if hasClashingSport:
            return False

    # desired number not taken AND no conflicts
    return True


def allocateUserChoices(user, allocationMethod):
    userChoice = Choice.query.filter(Choice.user_id == user.id).first()

    if userChoice == None:
        # user did not input any choice, just return True and skip
        return True

    firstChoice = userChoice.firstChoice
    secondChoice = userChoice.secondChoice
    thirdChoice = userChoice.thirdChoice
    fourthChoice = userChoice.fourthChoice
    fifthChoice = userChoice.fifthChoice

    if validateChoiceAvailable(firstChoice, user):
        allocationMethod(firstChoice, user)
        return True
    elif validateChoiceAvailable(secondChoice, user):
        allocationMethod(secondChoice, user)
        return True
    elif validateChoiceAvailable(secondChoice, user):
        allocationMethod(secondChoice, user)
    elif validateChoiceAvailable(thirdChoice, user):
        allocationMethod(thirdChoice, user)
        return True
    elif validateChoiceAvailable(fourthChoice, user):
        allocationMethod(fourthChoice, user)
        return True
    elif validateChoiceAvailable(fifthChoice, user):
        allocationMethod(fifthChoice, user)
        return True
    else:
        return False


def allocateSamePointUsers(userList, allocationMethod):
    """shuffles the users randomly with the same points and allocates them accordingly"""
    random.shuffle(userList)
    for user in userList:
        result = allocateUserChoices(user, allocationMethod)
        if result == False:
            # if any of the user was not succesfully
            db.session.rollback()
            return result
    db.session.commit()
    return True


def allocateUniqueNumberToUser(number, user):
    desiredJerseyNumber = JerseyNumber.query.filter(
        (JerseyNumber.gender == user.gender) & (JerseyNumber.number == number)).first()
    desiredJerseyNumber.users.append(user)
    desiredJerseyNumber.isTaken = True
    user.jerseyNumber = desiredJerseyNumber


def allocateNonUniqueNumberToUser(number, user):
    desiredJerseyNumber = JerseyNumber.query.filter(
        (JerseyNumber.gender == user.gender) & (JerseyNumber.number == number)).first()
    desiredJerseyNumber.users.append(user)
    user.jerseyNumber = desiredJerseyNumber

# only freshie and year 2 will not have unique number


def allocateByYear(currentYear):
    """allocates users by year, and returns list of users with conflict is any"""
    allocationMethod = allocateUniqueNumberToUser
    if (currentYear == 1 or currentYear == 2):
        allocationMethod = allocateNonUniqueNumberToUser

    UsersFromCurrentYear = User.query.filter(
        User.year == currentYear).order_by(User.points.desc()).all()

    UserIterator = iter(UsersFromCurrentYear)
    currentUser = next(UserIterator)
    currentPoint = currentUser.points
    tempUserList = [currentUser]
    for user in UserIterator:
        currentUser = user
        if (currentUser.points == currentPoint):
            tempUserList.append(currentUser)
        else:
            allocationResult = allocateSamePointUsers(
                tempUserList, allocationMethod)
            if allocationResult == False:
                return tempUserList
            currentPoint = currentUser.points
            tempUserList = [currentUser]

    if tempUserList:
        # tempUserList is not empty, allocate them
        allocationResult = allocateSamePointUsers(
            tempUserList, allocationMethod)
        if allocationResult == False:
            return tempUserList

#right now the way to access who got the final number is to get number -> query in user using this number -> return this user
def generateMaleList(): 
    maleNumbers = JerseyNumber.query.filter(JerseyNumber.gender_id==1).all()
    modifiedDict = {}
    
    for number in maleNumbers:
        user = User.query.filter(User.jerseyNumber_id == number.id and User.gender_id == 1).first()
        if user:
            print(user)
            entry = {}
            entry['name'] = user.name
            entry['roomNumber'] = user.roomNumber
            entry['year'] = user.year
            modifiedDict[number.number] = entry
        else:   
            entry = {}
            entry['name'] = '-'
            entry['year'] = '-'
            entry['roomNumber'] = '-'
            modifiedDict[number.number] = entry
    return(modifiedDict)


def generateFemaleList():
    femaleNumbers = JerseyNumber.query.filter(JerseyNumber.gender_id==2).all()
    modifiedDict = {}
    
    for number in femaleNumbers:
        user = User.query.filter(User.jerseyNumber_id == number.id and User.gender_id == 2).first()
        if user:
            print(user)
            entry = {}
            entry['name'] = user.name
            entry['roomNumber'] = user.roomNumber
            entry['year'] = user.year
            modifiedDict[number.number] = entry
        else:   
            entry = {}
            entry['name'] = '-'
            entry['year'] = '-'
            entry['roomNumber'] = '-'
            modifiedDict[number.number] = entry
    return(modifiedDict)
