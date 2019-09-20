from jersey_bidder.models import *
from jersey_bidder import db
from jersey_bidder.useradmin.CustomAllocationExceptions import AllocationError
import random

def getHighestYear():
    return db.session.query(db.func.max(User.year)).scalar()

def getStatsForYearUnit(year):
    overallStats = {}

    totalUserInYear = User.query.filter(User.year == year).count()

    totalAllocatedUserInYear = User.query.filter((User.year == year) & (User.jerseyNumber_id != None)).count()

    overallStats.update({'totalUserInYear': totalUserInYear})
    overallStats.update({'totalAllocatedUserInYear': totalAllocatedUserInYear})

    return overallStats

def getStatsForYear(year):
    overallStats = {}
    overallStats.update({'totalUserInYear': 0})
    overallStats.update({'totalAllocatedUserInYear': 0})

    if year == 3:
        year = getHighestYear()

    while year > 3:
        currentYearStats = getStatsForYearUnit(year)
        currentTotalUserInYear = overallStats['totalUserInYear'] + currentYearStats['totalUserInYear']
        currentTotalAllocatedUserInYear = overallStats['totalAllocatedUserInYear'] + currentYearStats['totalAllocatedUserInYear']
        overallStats.update({'totalUserInYear': currentTotalUserInYear})
        overallStats.update({'totalAllocatedUserInYear': currentTotalAllocatedUserInYear})
        year = year - 1

    currentYearStats = getStatsForYearUnit(year)
    currentTotalUserInYear = overallStats['totalUserInYear'] + currentYearStats['totalUserInYear']
    currentTotalAllocatedUserInYear = overallStats['totalAllocatedUserInYear'] + currentYearStats['totalAllocatedUserInYear']
    overallStats.update({'totalUserInYear': currentTotalUserInYear})
    overallStats.update({'totalAllocatedUserInYear': currentTotalAllocatedUserInYear})

    return overallStats

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

def validateNumberTaken(desiredNumber, gender_id):
    """check if this jerseyNumber is taken, input gender_id 1 for male and 2 for female, returns boolean"""
    desiredJersey = JerseyNumber.query.filter((JerseyNumber.gender_id == gender_id) & (
        JerseyNumber.number == desiredNumber)).first()
    return desiredJersey.isTaken

def validateSportClashWithNumber(desiredNumber, user):
    """check whether the user has clash with any users holding the current jerseyNumber"""
    desiredJersey = JerseyNumber.query.filter((JerseyNumber.gender_id == user.gender_id) & (
        JerseyNumber.number == desiredNumber)).first()

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

def validateSportClashWithJersey(desiredJersey, user):
    """check whether the user has clash with any users holding the current jerseyNumber"""
    UsersWithDesiredNumber = desiredJersey.users

    if UserPlayMixedSport(user):
        # check clash with opposite gender users
        oppositeGenderID = getOppositeGenderID(user)
        desiredJerseyOppositeGender = JerseyNumber.query.filter(
            (JerseyNumber.gender_id == oppositeGenderID) & (JerseyNumber.number == desiredJersey.number)).first()
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

def validateChoiceAvailable(desiredNumber, user):
    # check if isTaken
    desiredJersey = JerseyNumber.query.filter((JerseyNumber.gender_id == user.gender_id) & (
        JerseyNumber.number == desiredNumber)).first()

    UsersWithDesiredNumber = desiredJersey.users

    userWantUnique = user.wantUniqueNumber
    if userWantUnique and UsersWithDesiredNumber:
        return False
    
    desiredNumberIsTaken = desiredJersey.isTaken

    if desiredNumberIsTaken:
        return False

    # check with the users of this number if there are conflicts
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
        # user did not input choice, return false
        return False

    if user.wantUniqueNumber:
        allocationMethod = allocateUniqueNumberToUser

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

def splitMaleAndFemale(userList):
    """splits the userList into male and female, male list at index 1 female index 2, return type is tuple"""
    tempMaleList = []
    tempFemaleList = []
    for user in userList:
        if user.gender_id == 1:
            tempMaleList.append(user)
        elif user.gender_id == 2:
            tempFemaleList.append(user)
        # by right should throw error here
    return tempMaleList, tempFemaleList

def allocateSamePointUsers(userList, allocationMethod, failedUserList):
    """shuffles the users randomly with the same points and allocates them accordingly"""
    random.shuffle(userList)
    for user in userList:
        result = allocateUserChoices(user, allocationMethod)
        if result == False:
            # if any of the user was not succesfully
            failedUserList.append(user)
    db.session.commit()
    return failedUserList

def setTaken():
    """scan throug all jersey's and set whichever have users to be taken"""
    jerseyWithUser = JerseyNumber.query.filter(JerseyNumber.users != None)
    for jersey in jerseyWithUser:
        jersey.isTaken = True
    db.session.commit()

def allocateYearUnit(currentYear):
    """unit of allocate, does not check seniorty"""
    # will add all users who were failed to be allocated into this list be it no choice OR conflict
    failedUserList = []

    UsersFromCurrentYear = User.query.filter((User.year == currentYear) & (User.jerseyNumber_id == None)).order_by(User.points.desc()).all()

    if not UsersFromCurrentYear:
        # no users from current year
        raise AllocationError("The current year: " + str(currentYear) + " does not contain any users in the database")

    UserIterator = iter(UsersFromCurrentYear)
    currentUser = next(UserIterator)
    currentPoint = currentUser.points
    tempUserList = [currentUser]
    for user in UserIterator:
        currentUser = user
        if (currentUser.points == currentPoint):
            tempUserList.append(currentUser)
        else:
            allocateSamePointUsers(tempUserList, allocateNonUniqueNumberToUser, failedUserList)
            currentPoint = currentUser.points
            tempUserList = [currentUser]

    if tempUserList:
        allocateSamePointUsers(tempUserList, allocateNonUniqueNumberToUser, failedUserList)

    return failedUserList

def allocateByYear(currentYear):
    """checks currentYear and applies required allocations"""
    # will add all users who were failed to be allocated into this list be it no choice OR conflict 
    failedUserList = []

    if currentYear >= 3:
        currentYear = getHighestYear()

        while currentYear > 3:
            # allocate away all the higher years first and append into currentfailedUserList
            failedUserList.extend(allocateYearUnit(currentYear))
            setTaken()
            currentYear = currentYear - 1

    UsersFromCurrentYear = User.query.filter((User.year == currentYear) & (User.jerseyNumber_id == None)).order_by(User.points.desc()).all()

    failedUserList.extend(allocateYearUnit(currentYear))

    if currentYear == 3:
        setTaken()

    return failedUserList

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

def availNumbers(user):
    """pass in a user object and return a list of jerseyNumbers available"""
    finalAvailList = []

    notTakenJerseyNumbers = JerseyNumber.query.filter((JerseyNumber.gender_id == user.gender_id) & (JerseyNumber.isTaken == False)).all()
    for jersey in notTakenJerseyNumbers:
        jerseyAvail = validateSportClashWithJersey(jersey, user)
        if (jerseyAvail):
            finalAvailList.append(jersey)
    
    return finalAvailList

