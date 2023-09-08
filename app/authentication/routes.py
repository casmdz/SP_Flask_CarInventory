from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from forms import UserRegistrationForm, UserLoginForm

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

# added, might  not work 
from helpers import token_required
from models import user_schema, users_schema


auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/toast')
def gettoast():
    return {'peanut butter': 'jelly time'}


@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = UserRegistrationForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            email = form.email.data
            #Y
            password = form.password.data
            print(first_name, last_name, username, email, password, ' Successfully signed up')

            user = User(email=email, username=username, first_name=first_name, last_name=last_name, password=password)

            db.session.add(user)
            db.session.commit()
            
            print(f'You have successfully created a user account {username}', 'User-created')
            return redirect(url_for('site.home'))
        
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_up.html', form=form)

# ERROR CAME FROM TYPO.... SIGN_IN -> SIGN_UP!!
# title='Register'



@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    error = None
    try:
        if request.method == 'POST' and form.validate():
            username_or_email = form.username_or_email.data
            password = form.password.data
            
            logged_user = User.query.filter((User.email == username_or_email) | (User.username == username_or_email)).first()
            
            # print(logged_user,password)
            
            if logged_user: 
                if check_password_hash(logged_user.password, password):
                    login_user(logged_user)
                    print(f'{username_or_email} signed in to see the car inventory site', 'auth-sucess')
                    # Something just happened to new-hope... signed in to see the car inventory site auth-sucess
                    return redirect(url_for('site.profile'))
                else:
                    print(logged_user, ' incorrect password')
                    # Something just happened to new-hope...  incorrect password
                    error = 'Incorrect password'
                    flash('Incorrect password. Please try again.', error)
            else:
                print('User doesnt exist.')
                error = 'Invalid credentials'
                return redirect(url_for('auth.signin'))
            return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_in.html', form=form, error=error, flash=flash)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))

@auth.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    user_list = []
    for u in users:
        user_list.append({
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'username': u.username,
            'email': u.email
        })
    return jsonify(user_list)
# works! got a list of users


# @auth.route('/users/<id>', methods=['POST','PUT'])
# @token_required
# def update_user(current_user_token,id):
#     print(f'current_user_token: {current_user_token}')
#     print(f'id: {id}')
    
#     user = User.query.get(id)
#     if user is None:
#         return jsonify({'message': 'User not found'}), 404


# Update
@auth.route('/users/<id>', methods=['POST','PUT'])
@token_required
def update_user(current_user_token,id):
    print(f'current user id: {id}')

    user = User.query.get(id)
    user.first_name = request.json['first_name']
    user.last_name = request.json['last_name']
    # if 'first_name' in request.json:
    #     user.first_name = request.json['first_name']
    # if 'last_name' in request.json:
    #     user.last_name = request.json['last_name']
    user.username = request.json['username']
    user.email = request.json['email']
    user.user_token = current_user_token.token
    
    db.session.commit()
    response = user_schema.dump(user)
    return jsonify(response)

# fixed bug 6 , working now


@auth.route('/users/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user_token,id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    response = user_schema.dump(user)
    return jsonify(response, {'message': 'User deleted successfully'})

#working code 