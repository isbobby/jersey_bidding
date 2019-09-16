from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from flask_user import roles_required, current_user

# local
from jersey_bidder.models import User, Choice, JerseyNumber
from jersey_bidder.numbers.forms import biddingForm, chopeNumberForm, allocateForm
from jersey_bidder import db
from jersey_bidder.utils import getUser

numbers = Blueprint('numbers', __name__)


@numbers.route("/preference", methods=['GET', 'POST'])
@roles_required('Bidder')
def showNumber():
    currentUser = getUser(current_user)
    numbers = JerseyNumber.query.filter(
        JerseyNumber.gender_id == currentUser.gender_id)
    return render_template('prefViewAll.html', title='Preference Page', numbers=numbers)


@numbers.route("/preference/<int:jerseyNumber_id>", methods=['GET', 'POST'])
@roles_required('Bidder')
def showSingleNumber(jerseyNumber_id):
    number = JerseyNumber.query.get_or_404(jerseyNumber_id)
    interestedUsers = User.query.filter(
        User.preference_id == number.id and User.gender_id == number.gender_id).all()
    return render_template('prefViewSingleNumber.html', title='Preference Page', number=number, interestedUsers=interestedUsers)


@numbers.route("/preference/chope/<int:jerseyNumber_id>", methods=['GET', 'POST'])
@roles_required('Bidder')
def chopeSingleNumber(jerseyNumber_id):
    number = JerseyNumber.query.get_or_404(jerseyNumber_id)
    newNumber = number = JerseyNumber.query.get_or_404(jerseyNumber_id)
    currentUser = getUser(current_user)
    currentUser.preference_id = newNumber.id
    db.session.commit()

    return render_template('prefChopeNumber.html', title='Chope', newNumber=newNumber)


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

    # if current user has submitted a choice, redirect to editing page
    if currentUser.choice:
        return redirect(url_for('numbers.editNumber'))

    if form.validate_on_submit():
        submitDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        choice = Choice(submitDatetime=submitDate, firstChoice=form.firstChoice.data, secondChoice=form.secondChoice.data,
                        thirdChoice=form.thirdChoice.data, fourthChoice=form.fourthChoice.data, fifthChoice=form.fifthChoice.data,
                        user_id=currentUser.id)

        db.session.add(choice)
        db.session.commit()

        successMessage = "Your submission has been registered."
        return render_template('biddingSuccess.html', successMessage=successMessage)

    return render_template('biddingPage.html', title='Bidding', form=form)


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

    # fetch current users' previous choice to display on the site
    currentChoice = Choice.query.filter(
        Choice.user_id == currentUser.id).first()

    if form.validate_on_submit():
        submitDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        newChoice = Choice(submitDatetime=submitDate, firstChoice=form.firstChoice.data, secondChoice=form.secondChoice.data,
                           thirdChoice=form.thirdChoice.data, fourthChoice=form.fourthChoice.data, fifthChoice=form.fifthChoice.data,
                           user_id=currentUser.id)

        # remove the previous submission and commit the latest one
        db.session.delete(currentChoice)
        db.session.add(newChoice)
        db.session.commit()

        successMessage = "Your previous submission has been updated"
        return render_template('biddingSuccess.html', successMessage=successMessage)

    return render_template('biddingEdit.html', title='Bidding', form=form, currentChoice=currentChoice)



