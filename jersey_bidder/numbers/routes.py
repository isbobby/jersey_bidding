from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

#local
from jersey_bidder.models import  User, Choice, JerseyNumber
from jersey_bidder.numbers.forms import checkNumberForm, biddingForm
from jersey_bidder import db

numbers = Blueprint('numbers', __name__)

@numbers.route("/preference", methods=['GET','POST']) 
def showNumber():
    form = checkNumberForm()
    if form.validate_on_submit():
        number = JerseyNumber.query.get(form.number)
        return redirect(url_for('numbers.chopeNumber'))

    return render_template('showNumber.html', title='Preference Page')

@numbers.route("/bidding", methods=['GET','POST'])
def bidNumber():

    #initialize form and populate choices
    form = biddingForm()
    form.firstChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.secondChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.thirdChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.fourthChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.fifthChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]

    #if current user has submitted a choice, redirect to editing page
    if current_user.choice:
        return redirect(url_for('numbers.editNumber'))

    if form.validate_on_submit():
        submitDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        choice = Choice( submitDatetime=submitDate, firstChoice = form.firstChoice.data, secondChoice = form.secondChoice.data, 
        thirdChoice = form.thirdChoice.data, fourthChoice = form.fourthChoice.data, fifthChoice = form.fifthChoice.data,
        user_id = current_user.id)

        db.session.add(choice)
        db.session.commit()

        successMessage = "Your submission has been registered."
        return render_template('biddingSuccess.html', successMessage=successMessage)
        
    return render_template('biddingPage.html', title='Bidding', form=form)

@numbers.route("/bidding/editchoice", methods=['GET','POST'])
def editNumber():

    #initialize form and populate choices
    form = biddingForm()
<<<<<<< HEAD
=======
    form.firstChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.secondChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.thirdChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.fourthChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.fifthChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
>>>>>>> parent of 4dc4dae... adjusted UI, fixed login and jersey number display

    if current_user.gender.genderName == "Male":
        form.firstChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False, JerseyNumber.gender==current_user.gender)]
        form.secondChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False, JerseyNumber.gender==current_user.gender)]
        form.thirdChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False, JerseyNumber.gender==current_user.gender)]
        form.fourthChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False, JerseyNumber.gender==current_user.gender)]
        form.fifthChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False, JerseyNumber.gender==current_user.gender)]
    
    else:
        form.firstChoice.choices = [(entries.number,entries.number  - 100) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False, JerseyNumber.gender==current_user.gender)]
        form.secondChoice.choices = [(entries.number,entries.number  - 100) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False, JerseyNumber.gender==current_user.gender)]
        form.thirdChoice.choices = [(entries.number,entries.number  - 100) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False, JerseyNumber.gender==current_user.gender)]
        form.fourthChoice.choices = [(entries.number,entries.number  - 100) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False, JerseyNumber.gender==current_user.gender)]
        form.fifthChoice.choices = [(entries.number,entries.number  - 100) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False, JerseyNumber.gender==current_user.gender)]

    #fetch current users' previous choice to display on the site
    rawChoice = Choice.query.filter(Choice.user_id==current_user.id).first()
    currentChoice= {'key':'value'}

    if current_user.gender.genderName == "Female":
        currentChoice['firstChoice'] = rawChoice.firstChoice - 100
        currentChoice['secondChoice'] = rawChoice.secondChoice - 100
        currentChoice['thirdChoice'] = rawChoice.thirdChoice - 100
        currentChoice['fourthChoice'] = rawChoice.fourthChoice - 100
        currentChoice['fifthChoice'] = rawChoice.fifthChoice - 100

    else:
        currentChoice = rawChoice
    
    if form.validate_on_submit():
        submitDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        newChoice = Choice( submitDatetime=submitDate, firstChoice = form.firstChoice.data, secondChoice = form.secondChoice.data, 
        thirdChoice = form.thirdChoice.data, fourthChoice = form.fourthChoice.data, fifthChoice = form.fifthChoice.data,
        user_id = current_user.id)

        #remove the previous submission and commit the latest one
        db.session.delete(rawChoice)
        db.session.add(newChoice)
        db.session.commit()

        successMessage = "Your previous submission has been updated"
        return render_template('biddingSuccess.html', successMessage=successMessage)
    
    return render_template('biddingEdit.html', title='Bidding', form=form, currentChoice=currentChoice)
