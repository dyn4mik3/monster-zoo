from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask.ext.socketio import SocketIO

# Create app
app = Flask(__name__)

# Load up config.py file
app.config.from_object('config')

# Create database connection object
db = SQLAlchemy(app)

# Create mail object
mail = Mail(app)

# Create socketio object
socketio = SocketIO(app)

from app import views, models
