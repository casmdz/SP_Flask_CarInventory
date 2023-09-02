from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from forms import UserRegistrationForm, UserLoginForm
from models import User

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')



@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = UserRegistrationForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            #Y
            password = form.password.data
            print(username, email, password)
            
            #instantiate user class 
            #inside the user class, take the password X and set it to that variable Y 
            #(x,y)
            user = User(username, email, password = password)

            db.session.add(user)
            db.session.commit()
            
            flash(f'You have successfully created a user account {username}', 'User-created')
            return redirect(url_for('site.home'))
        
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_up.html', form=form)
# ERROR CAME FROM TYPO.... SIGN_IN -> SIGN_UP!!
# title='Register'


# @auth.route('/signin', methods = ['GET', 'POST'])
# def signin():
#     form = UserLoginForm()
    
#     try:
#         if request.method == 'POST' and form.validate_on_submit():
            
#             username = form.username.data
#             email = form.email.data
#             password = form.password.data
#             print(username,email,password)
  
#             logged_user = User.query.filter_by(username=form.username_or_email.data).first() or User.query.filter_by(email=form.username_or_email.data).first()
#             # unused  code 
#             # if logged_user and user.check_password(form.password.data):
#             # old code 
#             #logged_user = User.query.filter(User.email == email).first()
#             if logged_user and check_password_hash(logged_user.password, password):
#                 login_user(logged_user)
                
#                 flash('successfully signed in to see the car inventory site', 'auth-sucess')
#                 return redirect(url_for('site.profile'))
#             else:
#                 flash('You have failed in your attempt to access this content.', 'auth-failed')
#                 return redirect(url_for('auth.signin'))
#     except:
#         raise Exception('Invalid Form Data: Please Check your Form')
#     return render_template('sign_in.html', form=form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            logged_user = User.query.filter_by(username=form.username_or_email.data).first() or User.query.filter_by(email=form.username_or_email.data).first()
            # unused  code 
            # if logged_user and user.check_password(form.password.data):
            # old code 
            #logged_user = User.query.filter(User.email == email).first()   
            password = form.password.data
            print(logged_user,password)
            
            if logged_user: 
                if check_password_hash(logged_user.password, password):
                    login_user(logged_user)
                    flash('successfully signed in to see the car inventory site', 'auth-sucess')
                    return redirect(url_for('site.profile'))
                else:
                    flash('Incorrect password. Please try again.', 'auth-failed')
            else:
                flash('User doesnt exist.', 'auth-failed')
                return redirect(url_for('auth.signin'))
            return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_in.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))