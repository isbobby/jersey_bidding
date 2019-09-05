from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required

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
    form = biddingForm()
    form.firstChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.secondChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.thirdChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.fourthChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]
    form.fifthChoice.choices = [(entries.number,entries.number) for entries in JerseyNumber.query.filter(JerseyNumber.isTaken == False)]

    if form.validate_on_submit():
        choice = Choice( submitDatetime="", firstChoice = form.firstChoice.data, secondChoice = form.secondChoice.data, 
        thirdChoice = form.thirdChoice.data, fourthChoice = form.fourthChoice.data, fifthChoice = form.fifthChoice.data,
        user_id = current_user.id )
        db.session.add(choice)
        db.session.commit(choice)
        flash('Your Post Has Been Created!', 'success') 
        return redirect(url_for('main.home'))
        
    return render_template('biddingPage.html', title='Bidding', form=form)