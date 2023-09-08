from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from wtforms.validators  import DataRequired, Email, ValidationError
# from wtforms import DataRequired, Email, ValidationError

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Imports for Login Manager
from flask_login import UserMixin

# Import for Flask Login
from flask_login import LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow


#variables for class instantiation
login_manager = LoginManager() 
# doesnt work ^

ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    #ADDED USERNAME 
    username = db.Column(db.String(20), nullable=False, unique=True) 
    email = db.Column(db.String(150), nullable=False, unique=True) 
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

# added username 
    def __init__(self, email, username, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.username = username
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

# The set_id method creates a unique id number that we'll use as a primary key
    def set_id(self):
        return str(uuid.uuid4())
    
# set_password generates a hash that makes it impossible for the database owner to see the actual password. 
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

# the __repr__ method prints out at the end - this will show up in our terminal/CLI eventually. 
    def __repr__(self):
        return f'Something just happened to {self.username}...'
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
  
user_schema = UserSchema()
users_schema = UserSchema(many=True)
  
  
class Car(db.Model):
    id = db.Column(db.String, primary_key=True)
    make = db.Column(db.String(150), nullable = False, default = '')
    model = db.Column(db.String(150), nullable = False, default = '')
    year = db.Column(db.String(20), default = '')
    color = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, make='', model='', year='', color=None, user_token='', id=''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.user_token = user_token
        
    def __repr__(self):
        return f'This car {self.id} has been added to the collection.'
    
    def set_id(self):
        return (secrets.token_urlsafe())
    #its Base64 encoded
    
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make', 'model', 'year', 'color']
  
car_schema = CarSchema()
cars_schema = CarSchema(many=True)
