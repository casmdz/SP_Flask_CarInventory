from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length


from models import User

# class UserLoginForm(FlaskForm):
#     email = StringField('Email', validators = [DataRequired(), Email()])
#     password = PasswordField('Password', validators = [DataRequired()])
#     submit_button = SubmitField()
    
# jinja2.exceptions.UndefinedError: 'forms.UserRegistrationForm object' has no attribute 'username_or_email'
# 127.0.0.1 - - [02/Sep/2023 17:44:55] "GET /signup HTTP/1.1" 500 -
    
class UserLoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Log In')

    def validate_username_or_email(self, username_or_email):
        #user = logged_user (thats the way the Phonebook had it)
        logged_user = User.query.filter_by(username=username_or_email.data).first() or User.query.filter_by(email=username_or_email.data).first()
        if not logged_user:
            raise ValidationError('User does not exist. Please check your username or email.')
        
        #INFO
        #https://betterprogramming.pub/a-detailed-guide-to-user-registration-login-and-logout-in-flask-e86535665c07
        # https://wtforms.readthedocs.io/en/3.0.x/
        
class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit_button = SubmitField('Sign Up')
# forms --> app\templates\forms.html