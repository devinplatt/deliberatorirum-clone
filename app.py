#!/usr/bin/env python
from database import db
from models import User
from views import bp  # bp for "blueprint"

#import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json, jsonify, make_response
from contextlib import closing
import logging
import gitutils
import os
from flask.ext.bcrypt import Bcrypt

from flask.ext.login import LoginManager, login_user, logout_user, login_required
from forms import LoginForm

def create_app(config_filename = 'cf'):
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config.from_pyfile('config.py', silent=False)
    db.init_app(app)
    app.register_blueprint(bp)

    return app

app = create_app()
bcrypt = Bcrypt(app)

def connect_db():
  return None

def init_db():
  pass

@app.before_request
def before_request():
  pass

@app.teardown_request
def teardown_request(exception):
  pass

# login stuff
login_manager = LoginManager()
login_manager.init_app(app)

# login database

from flask.ext.sqlalchemy import SQLAlchemy

@login_manager.user_loader
def load_user(username):
  #return User.query.get(int(userid))
  return User.query.get(username)

# taken from:
# https://flask-login.readthedocs.org/en/latest/
# https://realpython.com/blog/python/using-flask-login-for-user-management-with-flask/
@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  form = LoginForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      # authenticate user
      user = User.query.get(form.username.data)
      if user:
        if bcrypt.check_password_hash(user.password,
                                      form.password.data):
          # login and validate the user
          login_user(user)
          session['logged_in'] = True # is there a better way?
          session['username'] = user.username # is there a better way?
          flash("Logged in successfully.")
          return redirect(url_for('bp.show_index'))
        else:
          error = "incorrect username or password (p)"
      else:
        error = "incorrect username or password (u)"
  return render_template('login.html', error=error, form = form)


@app.route('/logout')
@login_required
def logout():
  session.pop('logged_in', None)
  session.pop('username', None)
  logout_user()
  flash('You were logged out')
  return redirect(url_for('bp.show_index'))


if __name__ == '__main__':
  # see https://gist.github.com/ibeex/3257877
  # if you want to log to file
  app.run()
  #pass
