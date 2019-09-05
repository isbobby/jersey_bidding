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
        user = User.query.filter_by(email=form.roomNumber.data).first()
        #if user and bcrypt.check_password_hash(user.password, form.password.data):
        if form.password.data == user.password:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful, Please Check Roomnumber and Password', 'danger')
    return render_template('login.html', title='Login', form=form)

@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

#User
#login 

#main
#static faq page

#Jersey
#submit preference 
#view

#faq -> login -> view -> submit (validate) -> view -> logout -> view

#csv
#excel work book

#scripts
#generate pw -> send email

#load to DB

#website
#####separate login windows and limit login

#publish result

#scan db for jersey bidding 