from flask import Blueprint, render_template, url_for, redirect, request, flash, make_response
from flask_login import login_user, logout_user, login_required
from flask_user import current_user, roles_required
from datetime import datetime

# local
from jersey_bidder.models import User, Choice, JerseyNumber, FlaskUser, Role, FlaskUserRoles

from jersey_bidder.useradmin.forms import allocateForm, assignNumberForm
from jersey_bidder import db
from jersey_bidder.utils import getFlaskUser, getFlaskUserRole
from jersey_bidder.useradmin.utils import allocateByYear, generateMaleList, generateFemaleList, splitMaleAndFemale, \
        availNumbers, allocateNonUniqueNumberToUser, allocateUniqueNumberToUser, getStatsForYear
from jersey_bidder.useradmin.CustomAllocationExceptions import AllocationError
from jersey_bidder.useradmin.outputUtils import create_userpassword_csv


useradmin = Blueprint('useradmin', __name__)


@useradmin.route("/useradmin/home", methods=['GET', 'POST'])
@roles_required('Admin')
def adminHome():
    return render_template('/jersey_bidder/useradmin/adminHome.html')


@useradmin.route("/useradmin/allocate", methods=['GET', 'POST'])
@roles_required('Admin')
def adminAllocate():
    form = allocateForm()
    form.yearToAllocate.choices = [(0, 0), (1, 1), (2, 2), (3, "3+")]

    if form.validate_on_submit():
        failedAllocateUsers = []
        selectYear = form.yearToAllocate.data
        try:
            failedAllocateUsers = allocateByYear(selectYear)
        except AllocationError as err:
            errString = str(err)
            return render_template('generalErrorPage.html', errorMessage = errString)

        if failedAllocateUsers != None:

            overallStats = getStatsForYear(selectYear)

            # get failed male and female users
            maleAndFemaleTuple = splitMaleAndFemale(failedAllocateUsers)
            failedMaleList = maleAndFemaleTuple[0]
            failedFemaleList = maleAndFemaleTuple[1]

            return render_template('/jersey_bidder/useradmin/allocateFailure.html', failedMales=failedMaleList, failedFemales=failedFemaleList, overallStats=overallStats)

        successMessage = "successfully allocated year " + str(form.yearToAllocate.data) + " students"

        allUsersInYear = User.query.filter(User.year == form.yearToAllocate.data).all()
        return render_template('/jersey_bidder/useradmin/allocateSuccess.html', successMessage=successMessage, allUsersInYear=allUsersInYear)

    return render_template('/jersey_bidder/useradmin/allocatePage.html', form=form)


@useradmin.route("/useradmin/checkresult/male", methods=['GET', 'POST'])
@roles_required('Admin')
def fullResultMale():
    list = generateMaleList()
    return render_template('/jersey_bidder/useradmin/fullResultMale.html', list=list)


@useradmin.route("/useradmin/checkresult/female", methods=['GET', 'POST'])
@roles_required('Admin')
def fullResultFemale():
    list = generateFemaleList()
    return render_template('/jersey_bidder/useradmin/fullResultFemale.html', list=list)


@useradmin.route("/useradmin/checkresult/malebyyear/<int:year_id>", methods=['GET', 'POST'])
@login_required
def showMaleByYear(year_id):
    usersByYear = User.query.filter(
        (User.year == year_id) & (User.gender_id == 1)).all()
    return render_template('/jersey_bidder/useradmin/showMaleResultByYear.html', usersByYear=usersByYear, year_id=year_id)


@useradmin.route("/useradmin/checkresult/femalebyyear/<int:year_id>", methods=['GET', 'POST'])
@roles_required('Admin')
def showFemaleByYear(year_id):
    usersByYear = User.query.filter(
        (User.year == year_id) & (User.gender_id == 2)).all()
    return render_template('/jersey_bidder/useradmin/showFemaleResultByYear.html', usersByYear=usersByYear, year_id=year_id)


@useradmin.route("/useradmin/checkresult/fullmalelist", methods=['GET', 'POST'])
@roles_required('Admin')
def getAllMaleUsers():
    users = User.query.filter(User.gender_id == 1).all()
    return render_template('/jersey_bidder/useradmin/fullNameListMale.html', users=users)


@useradmin.route("/useradmin/checkresult/fullfemalelist", methods=['GET', 'POST'])
@roles_required('Admin')
def getAllFemaleUsers():
    users = User.query.filter(User.gender_id == 2).all()
    return render_template('/jersey_bidder/useradmin/fullNameListFemale.html', users=users)


@useradmin.route("/useradmin/checkresult/conflict/male", methods=['GET', 'POST'])
@roles_required('Admin')
def getConflictMale():
    conflictUsers = User.query.filter(
        (User.gender_id == 1) & (User.jerseyNumber_id == None)).all()

    return render_template('/jersey_bidder/useradmin/maleConflictUser.html', conflictUsers=conflictUsers)


@useradmin.route("/useradmin/checkresult/conflict/female", methods=['GET', 'POST'])
@roles_required('Admin')
def getConflictFemale():
    conflictUsers = User.query.filter(
        (User.gender_id == 2) & (User.jerseyNumber_id == None)).all()

    return render_template('/jersey_bidder/useradmin/femaleConflictUser.html', conflictUsers=conflictUsers)


@useradmin.route("/useradmin/adminassign/<int:user_id>", methods=['GET', 'POST'])
@roles_required('Admin')
def adminAssign(user_id):
    user = User.query.filter(User.id == user_id).first()
    listOfAvailNumbers = availNumbers(user)

    form = assignNumberForm()
    form.assign.choices = [(entries.number, entries.number)
                           for entries in listOfAvailNumbers]
    number = form.assign.data

    if form.validate_on_submit():
        if user.year == 1 or user.year == 2:
            allocateNonUniqueNumberToUser(number, user)
        else:
            allocateUniqueNumberToUser(number, user)

        db.session.commit()
        return render_template('/jersey_bidder/useradmin/adminAssignSuccess.html', user=user, number=number)

    return render_template('/jersey_bidder/useradmin/allocateSingleUser.html', user=user, listOfAvailNumbers=listOfAvailNumbers, form=form)

@useradmin.route("/jersey_bidder//useradmin/deactivate/<int:year>", methods=['GET', 'POST'])
def deactivateByYear(year):
    #deactivate users by year
    rawUsers = User.query.filter(User.year==year).all()
    userlist = []
    bidderRole = Role.query.filter(Role.name == "Bidder").first()

    for user in rawUsers:
        flaskUser = getFlaskUser(user)
        userlist.append(flaskUser)
    for flaskUser in userlist:
        print(flaskUser.id)
        print(flaskUser.roles)
        if bidderRole in flaskUser.roles:
            flaskUser.roles.remove(bidderRole)

    db.session.commit()
    
    successMessage = "All year " + str(year) + " users have been deactivated. They can no longer submit bidding requests and edit their previous submissions." 
    return render_template('/jersey_bidder/useradmin/adminChangeAuthByYear.html', rawUsers=rawUsers, userlist=userlist, successMessage=successMessage)

@useradmin.route("/useradmin/activate/<int:year>", methods=['GET', 'POST'])
def activateByYear(year):
    #deactivate users by year
    rawUsers = User.query.filter(User.year==year).all()
    userlist = []
    bidderRole = Role.query.filter(Role.name == "Bidder").first()

    for user in rawUsers:
        flaskUser = getFlaskUser(user)
        if bidderRole not in flaskUser.roles:
            flaskUser.roles.append(bidderRole)
        userlist.append(flaskUser)

    db.session.commit() 

    successMessage = "All year " + str(year) + " users have been activated. They can now submit bidding requests and edit their previous submissions." 
    return render_template('/jersey_bidder/useradmin/adminChangeAuthByYear.html', rawUsers=rawUsers, userlist=userlist, successMessage=successMessage)

@useradmin.route("/useradmin/showactive/all", methods=['GET'])
@roles_required('Admin')
def checkActiveUsers():
    users = User.query.all()
    activeUsers = []
    bidderRole = Role.query.filter(Role.name == "Bidder").first()
    for user in users:
        flaskuser = getFlaskUser(user)
        if bidderRole in flaskuser.roles:
            activeUsers.append(user)
    
    return render_template('/jersey_bidder/useradmin/adminShowActiveUsers.html', activeUsers=activeUsers)


@useradmin.route("/useradmin/generatePasswordCSV", methods=['GET'])
@roles_required('Admin')
def getUserPassWordList():
    data = User.query.order_by(User.roomNumber).all()
    (file_basename, server_path, file_size) = create_userpassword_csv(data)
    return 
    # return_file = open(server_path+file_basename, 'r')
    # response = make_response(return_file,200)
    # response.headers['Content-Description'] = 'File Transfer'
    # response.headers['Cache-Control'] = 'no-cache'
    # response.headers['Content-Type'] = 'text/csv'
    # response.headers['Content-Disposition'] = 'attachment; filename=%s' % file_basename
    # response.headers['Content-Length'] = file_size
    # return response