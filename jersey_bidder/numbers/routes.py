from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from flask_user import roles_required, current_user

# local
from jersey_bidder.models import User, Choice, JerseyNumber
from jersey_bidder.numbers.forms import biddingForm, chopeNumberForm, allocateForm
from jersey_bidder.numbers.utils import typeCastFormData
from jersey_bidder import db
from jersey_bidder.utils import getUser


numbers = Blueprint('numbers', __name__)


@numbers.route("/preference", methods=['GET', 'POST'])
def showNumber():
    currentUser = getUser(current_user)
    numbers = JerseyNumber.query.filter(
        JerseyNumber.gender_id == currentUser.gender_id)
    return render_template('/jersey_bidder/numbers/prefViewAll.html', title='Preference Page', numbers=numbers)


@numbers.route("/preference/<int:jerseyNumber_id>", methods=['GET', 'POST'])
def showSingleNumber(jerseyNumber_id):
    number = JerseyNumber.query.get_or_404(jerseyNumber_id)
    interestedUsers = User.query.filter(
        User.preference_id == number.id and User.gender_id == number.gender_id).all()
    return render_template('/jersey_bidder/numbers/prefViewSingleNumber.html', title='Preference Page', number=number, interestedUsers=interestedUsers)


@numbers.route("/preference/chope/<int:jerseyNumber_id>", methods=['GET', 'POST'])
def chopeSingleNumber(jerseyNumber_id):
    number = JerseyNumber.query.get_or_404(jerseyNumber_id)
    newNumber = number = JerseyNumber.query.get_or_404(jerseyNumber_id)
    currentUser = getUser(current_user)
    currentUser.preference_id = newNumber.id
    db.session.commit()

    return render_template('/jersey_bidder/numbers/prefChopeNumber.html', title='Chope', newNumber=newNumber)


@numbers.route("/bidding", methods=['GET', 'POST'])
@roles_required('Bidder')
def bidNumber():

    # initialize form and populate choices
    form = biddingForm()
    currentUser = getUser(current_user)
    form.firstChoice.choices = [(entries.number, entries.number) for entries in JerseyNumber.query.filter(
        JerseyNumber.isTaken == False, JerseyNumber.gender_id == currentUser.gender_id)]
    form.secondChoice.choices = [(entries.number, entries.number) for entries in JerseyNumber.query.filter(
        JerseyNumber.isTaken == False, JerseyNumber.gender_id == currentUser.gender_id)]
    form.thirdChoice.choices = [(entries.number, entries.number) for entries in JerseyNumber.query.filter(
        JerseyNumber.isTaken == False, JerseyNumber.gender_id == currentUser.gender_id)]
    form.fourthChoice.choices = [(entries.number, entries.number) for entries in JerseyNumber.query.filter(
        JerseyNumber.isTaken == False, JerseyNumber.gender_id == currentUser.gender_id)]
    form.fifthChoice.choices = [(entries.number, entries.number) for entries in JerseyNumber.query.filter(
        JerseyNumber.isTaken == False, JerseyNumber.gender_id == currentUser.gender_id)]
    form.wantUniqueNumber.choices = [(1,'Yes'),(2,'No')]

    # if current user has submitted a choice, redirect to editing page
    if currentUser.choice:
        return redirect(url_for('numbers.editNumber'))

    # fetch the current user's year for further validation, only 2+ years in IHG can choose unique option
    userYear = getUser(current_user).year

    if form.validate_on_submit():
        submitDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #type cast an integer from form into bool, wantUniqueNumber is either True or False (bool)
        wantUniqueNumber = typeCastFormData(form.wantUniqueNumber.data)

        choice = Choice(submitDatetime=submitDate, firstChoice=form.firstChoice.data, secondChoice=form.secondChoice.data,
                        thirdChoice=form.thirdChoice.data, fourthChoice=form.fourthChoice.data, fifthChoice=form.fifthChoice.data,
                        user_id=currentUser.id)

        db.session.add(choice)
        db.session.commit()

        successMessage = "Your submission has been registered."
        return render_template('/jersey_bidder/numbers/biddingSuccess.html', successMessage=successMessage)

    return render_template('/jersey_bidder/numbers/biddingPage.html', title='Bidding', form=form, userYear=userYear)


@numbers.route("/bidding/editchoice", methods=['GET', 'POST'])
@roles_required('Bidder')
def editNumber():

    # get User Model from FlaskUser
    currentUser = getUser(current_user)

    # initialize form and populate choices
    form = biddingForm()
    form.firstChoice.choices = [(entries.number, entries.number) for entries in JerseyNumber.query.filter(
        JerseyNumber.isTaken == False, JerseyNumber.gender_id == currentUser.gender_id)]
    form.secondChoice.choices = [(entries.number, entries.number) for entries in JerseyNumber.query.filter(
        JerseyNumber.isTaken == False, JerseyNumber.gender_id == currentUser.gender_id)]
    form.thirdChoice.choices = [(entries.number, entries.number) for entries in JerseyNumber.query.filter(
        JerseyNumber.isTaken == False, JerseyNumber.gender_id == currentUser.gender_id)]
    form.fourthChoice.choices = [(entries.number, entries.number) for entries in JerseyNumber.query.filter(
        JerseyNumber.isTaken == False, JerseyNumber.gender_id == currentUser.gender_id)]
    form.fifthChoice.choices = [(entries.number, entries.number) for entries in JerseyNumber.query.filter(
        JerseyNumber.isTaken == False, JerseyNumber.gender_id == currentUser.gender_id)]
    form.wantUniqueNumber.choices = [(1,'Yes'),(2,'No')]

    # fetch current users' previous choice to display on the site
    currentChoice = Choice.query.filter(
        Choice.user_id == currentUser.id).first()

    # fetch the current user's year for further validation
    userYear = getUser(current_user).year

    if form.validate_on_submit():
        submitDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #type cast an integer from form into bool, wantUniqueNumber is either True or False (bool)
        wantUniqueNumber = typeCastFormData(form.wantUniqueNumber.data)

        newChoice = Choice(submitDatetime=submitDate, firstChoice=form.firstChoice.data, secondChoice=form.secondChoice.data,
                           thirdChoice=form.thirdChoice.data, fourthChoice=form.fourthChoice.data, fifthChoice=form.fifthChoice.data,
                           user_id=currentUser.id)

        # remove the previous submission and commit the latest one
        db.session.delete(currentChoice)
        db.session.add(newChoice)
        db.session.commit()

        successMessage = "Your previous submission has been updated"
        return render_template('/jersey_bidder/numbers/biddingSuccess.html', successMessage=successMessage)

    return render_template('/jersey_bidder/numbers/biddingEdit.html', title='Bidding', form=form, currentChoice=currentChoice, userYear=userYear)



