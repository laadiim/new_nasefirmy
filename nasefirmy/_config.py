#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# nasefirmy/_config.py


import os


# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'nasefirmy.db'
CSRF_ENABLED = True
SECRET_KEY = '\x03z\xf2\xf3}?BYc\x15Y\x87u\x90\xdf\x8a\x7fx\xf3$\xb9\x8e\x9fM'
# WTF_CSRF_SECRET_KEY = '\x03z\xf2\xf3}?BYc\x15Y\x87u\x90\xdf\x8a\x7fx\xf3$\xb9\x8e\x9fM'
DEBUG = True

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/' + DATABASE_PATH
