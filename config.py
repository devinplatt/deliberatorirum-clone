# Modified from: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DEBUG = True  # TODO: NEVER LEAVE THIS TRUE IN PRODUCTION!!!!!

SECRET_KEY = 'development key123' # learn what this is. Change value in production.
