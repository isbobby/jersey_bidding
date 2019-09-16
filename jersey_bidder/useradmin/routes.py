from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, login_required
from flask_user import current_user, roles_required
from datetime import datetime

# local
from jersey_bidder.models import User, Choice, JerseyNumber
from jersey_bidder.useradmin.forms import allocateForm, assignNumberForm
from jersey_bidder import db
from jersey_bidder.useradmin.utils import allocateByYear, generateMaleList, generateFemaleList, splitMaleAndFemale, \
        availNumbers, allocateNonUniqueNumberToUser, allocateUniqueNumberToUser, getStatsForYear
from jersey_bidder.useradmin.CustomAllocationExceptions import AllocationError


useradmin = Blueprint('useradmin', __name__)


@useradmin.route("/useradmin/home", methods=['GET', 'POST'])
@roles_required('Admin')
def adminHome():
    return render_template('adminHome.html')


@useradmin.route("/useradmin/allocate", methods=['GET', 'POST'])
@roles_required('Admin')
def adminAllocate():
    form = allocateForm()
    form.yearToAllocate.choices = [(1, 1), (2, 2), (3, 3), (4, 4)]

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

            return render_template('allocateFailure.html', failedMales=failedMaleList, failedFemales=failedFemaleList, overallStats=overallStats)

        successMessage = "successfully allocated year " + str(form.yearToAllocate.data) + " students"

        allUsersInYear = User.query.filter(User.year == form.yearToAllocate.data).all()
        return render_template('allocateSuccess.html', successMessage=successMessage, allUsersInYear=allUsersInYear)

    return render_template('allocatePage.html', form=form)


@useradmin.route("/useradmin/checkresult/male", methods=['GET', 'POST'])
@roles_required('Admin')
def fullResultMale():
    list = generateMaleList()
    return render_template('fullResultMale.html', list=list)


@useradmin.route("/useradmin/checkresult/female", methods=['GET', 'POST'])
@roles_required('Admin')
def fullResultFemale():
    list = generateFemaleList()
    return render_template('fullResultFemale.html', list=list)


@useradmin.route("/useradmin/checkresult/malebyyear/<int:year_id>", methods=['GET', 'POST'])
@login_required
def showMaleByYear(year_id):
    usersByYear = User.query.filter(
        (User.year == year_id) & (User.gender_id == 1)).all()
    return render_template('showMaleResultByYear.html', usersByYear=usersByYear, year_id=year_id)


@useradmin.route("/useradmin/checkresult/femalebyyear/<int:year_id>", methods=['GET', 'POST'])
@roles_required('Admin')
def showFemaleByYear(year_id):
    usersByYear = User.query.filter(
        (User.year == year_id) & (User.gender_id == 2)).all()
    return render_template('showFemaleResultByYear.html', usersByYear=usersByYear, year_id=year_id)


@useradmin.route("/useradmin/checkresult/fullmalelist", methods=['GET', 'POST'])
@roles_required('Admin')
def getAllMaleUsers():
    users = User.query.filter(User.gender_id == 1).all()
    return render_template('fullNameListMale.html', users=users)


@useradmin.route("/useradmin/checkresult/fullfemalelist", methods=['GET', 'POST'])
@roles_required('Admin')
def getAllFemaleUsers():
    users = User.query.filter(User.gender_id == 2).all()
    return render_template('fullNameListFemale.html', users=users)


@useradmin.route("/useradmin/checkresult/conflict/male", methods=['GET', 'POST'])
@roles_required('Admin')
def getConflictMale():
    conflictUsers = User.query.filter(
        (User.gender_id == 1) & (User.jerseyNumber_id == None)).all()

    return render_template('maleConflictUser.html', conflictUsers=conflictUsers)


@useradmin.route("/useradmin/checkresult/conflict/female", methods=['GET', 'POST'])
@roles_required('Admin')
def getConflictFemale():
    conflictUsers = User.query.filter(
        (User.gender_id == 2) & (User.jerseyNumber_id == None)).all()

    return render_template('femaleConflictUser.html', conflictUsers=conflictUsers)


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
        return render_template('adminAssignSuccess.html', user=user, number=number)

    return render_template('allocateSingleUser.html', user=user, listOfAvailNumbers=listOfAvailNumbers, form=form)
