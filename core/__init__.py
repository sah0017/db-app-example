import sys

# Refuse to run outside a virtual environment so the course's pinned
# libraries never get mixed with packages installed on the system Python.
# This check must come before any third-party imports.
if sys.prefix == sys.base_prefix:
    sys.exit(
        "This application must be run from inside a virtual environment.\n"
        "Follow the Setup steps in README.md, then start the app again."
    )

# an object of WSGI application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv

env_found = load_dotenv()
my_password = os.environ.get('PASSWORD')
# Not named USER: the shell already sets USER to your login name,
# and load_dotenv() doesn't override variables that already exist
db_user = os.environ.get('DB_USER', 'root')
db_name = os.environ.get('DB_NAME', 'sakila')

# Stop with a clear message instead of trying to log in with no password
if my_password is None:
    if not env_found:
        problem = "No .env file was found in the project folder."
    else:
        problem = "The .env file has no PASSWORD line."
    sys.exit(
        problem + "\n"
        "Create a file named .env in the project folder containing:\n"
        "  PASSWORD=your_mysql_password\n"
        "then start the app again. See step 5 in README.md."
    )

app = Flask(__name__, template_folder="../templates") # Flask constructor 
# Needed for flash() messages; a new random key each run is fine for local use
app.secret_key = os.urandom(24)
db_cred = { 
    'user': db_user,        # DATABASE USER 
    'pass': my_password,    # DATABASE PASSWORD 
    'host': '127.0.0.1',    # DATABASE HOSTNAME 
    'port': 3306,           # DATABASE PORT 
    'name': db_name         # DATABASE NAME 
} 
# URL.create escapes special characters (@, :, /, #, %) in the password
db_uri = URL.create(
    "mysql+pymysql",
    username=db_cred['user'],
    password=db_cred['pass'],
    host=db_cred['host'],
    port=db_cred['port'],
    database=db_cred['name'],
)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
class Base(DeclarativeBase):
    pass

# Creating an SQLAlchemy instance
db = SQLAlchemy(app, model_class=Base)
ma = Marshmallow(app)
