from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required

#local
from jersey_bidder.models import  User, Choice
from jersey_bidder.user.forms import LoginForm


user = Blueprint('users', __name__)

@user.route("/login", methods=['GET','POST']) 
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(roomNumber=form.roomNumber.data).first()
        #if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and form.password.data == user.password:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful, Please Check room number and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@user.route("/checkresult")
def checkresult():
    return render_template("checkResult.html")