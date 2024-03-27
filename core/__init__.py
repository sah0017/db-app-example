# an object of WSGI application 
from flask import Flask	 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv

load_dotenv()
my_password = str(os.environ.get('PASSWORD'))

app = Flask(__name__, template_folder="../templates") # Flask constructor 
db_cred = { 
    'user': 'root',         # DATABASE USER 
    'pass': my_password,    # DATABASE PASSWORD 
    'host': '127.0.0.1:3306',    # DATABASE HOSTNAME 
    'name': 'sakila'        # DATABASE NAME 
} 
db_uri = f"mysql+pymysql://{db_cred['user']}:{db_cred['pass']}@{db_cred['host']}/{db_cred['name']}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
ma = Marshmallow(app)
