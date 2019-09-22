from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, login_required
from flask_user import current_user

#local
from jersey_bidder.models import  User, Choice, FlaskUser
from jersey_bidder.user.forms import LoginForm
from jersey_bidder.utils import getUser


user = Blueprint('users', __name__)

@user.route("/login", methods=['GET','POST']) 
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attemptedFlaskUser = FlaskUser.query.filter_by(username=form.userName.data).first()
        #if user and bcrypt.check_password_hash(user.password, form.password.data):
        if attemptedFlaskUser and form.password.data == attemptedFlaskUser.password:
            login_user(attemptedFlaskUser)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful, Please Check room number and password', 'danger')
    return render_template('/jersey_bidder/user/login.html', title='Login', form=form)

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

""" @user.route("/checkresult")
@login_required
def checkresult():
    user = getUser(current_user)
    return render_template("/jersey_bidder/user/checkResult.html", user=user) """