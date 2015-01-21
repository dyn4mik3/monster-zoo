# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'super-secret'
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# Flask-Mail Settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False 
MAIL_USERNAME = 'email@gmail.com'
MAIL_PASSWORD = 'email'

# Flask-Security Settings
SECURITY_REGISTERABLE = True
SECURITY_EMAIL_SUBJECT_REGISTER = 'Welcome to MonsterZoo!'
