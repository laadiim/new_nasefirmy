#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# nasefirmy/__init__.py

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flaskext.mysql import MySQL

app = Flask(__name__)
app.config.from_pyfile('_config.py')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# from nasefirmy.users.views import users_blueprint
# from nasefirmy.overview.views import overview_blueprint
# from project.api.views import api_blueprint
from nasefirmy import views

# register our blueprints
# app.register_blueprint(users_blueprint)
# app.register_blueprint(overview_blueprint)
# app.register_blueprint(api_blueprint)


# error handlers

# @app.errorhandler(404)
# def page_not_found(error):
#     if app.debug is not True:
#         now = datetime.datetime.now()
#         r = request.url
#         with open('error.log', 'a') as f:
#             current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
#             f.write("\n404 error at {}: {} ".format(current_timestamp, r))
#     return render_template('404.html'), 404
#
#
# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     if app.debug is not True:
#         now = datetime.datetime.now()
#         r = request.url
#         with open('error.log', 'a') as f:
#             current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
#             f.write("\n500 error at {}: {} ".format(current_timestamp, r))
#     return render_template('500.html'), 500
