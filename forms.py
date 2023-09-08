from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from models import User

# class UserLoginForm(FlaskForm):
#     email = StringField('Email', validators = [DataRequired(), Email()])
#     password = PasswordField('Password', validators = [DataRequired()])
#     submit_button = SubmitField()
    
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
        # Note there is a distinction between this and DataRequired in that InputRequired looks that form-input data was provided, and DataRequired looks at the post-coercion data.
        
class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit_button = SubmitField('Sign Up')
# forms --> app\templates\forms.html
# it doesnt have the name fields!! 
# first_name = db.Column(db.String(150), nullable=True, default='')
# last_name = db.Column(db.String(150), nullable = True, default = '')