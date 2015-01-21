from app import app
from app import db

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, \
    RoleMixin

# Define models for Flask security
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Game models
class Gameroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean())
    created = db.Column(db.DateTime())
    player_one = db.Column(db.String(255))
    player_two = db.Column(db.String(255))
    winner = db.Column(db.String(255))

    def __repr__(self):
        return '<Game %r - Player 1: %s - Player 2: %s>' % (self.id, self.player_one, self.player_two)

"""
# Create the db
@app.before_first_request
def create_db():
    db.create_all()

"""

"""
# Create a user to test with
@app.before_first_request
def create_user():
    print 'Creating User: michael@rubycowgames.com'
    db.create_all()
    user_datastore.create_user(email='michael@rubycowgames.com', password='password')
    db.session.commit()
"""
