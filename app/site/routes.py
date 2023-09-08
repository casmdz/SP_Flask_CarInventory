from flask import Blueprint, render_template
from helpers import token_required
from models import db, User, Car
from flask_login import login_required, current_user

site = Blueprint('site', __name__, template_folder='site_templates')



@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/my_cars')
@login_required
# @token_required
def my_cars():
    user_cars = Car.query.filter_by(user_token=current_user.token).all()
    return render_template('my_cars.html', user_cars=user_cars)
    
    
# @site.route('/my_cars')
# @login_required
# # @token_required
# def my_cars(current_user_token):
#         user_cars = Car.query.filter_by(user_id=current_user_token.id).all()
#         return render_template('mycars.html', user_cars=user_cars)
