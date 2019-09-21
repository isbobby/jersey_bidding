import json
from flask import Blueprint, request, render_template, url_for,redirect
from flask_wtf import Form
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from jersey_bidder.models import FlaskUser
main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('/jersey_bidder/main/home.html')
    
@main.route("/")
@main.route("/faqpage")
def faq():
    return render_template('/jersey_bidder/main/faq.html')

# @main.route("/")
# @main.route("/test")
# def test():
#     roles = FlaskUser.query.first().roles
#     return render_template('/jersey_bidder/main/testingPage.html', roles=roles)