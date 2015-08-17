#!/usr/bin/env python
"""Create a new user"""
import sys

from flask import current_app
from models import User
from app import app, bcrypt, db
# from flask.ext.bcrypt import Bcrypt

def main():
  """Main entry point for script."""
  with app.app_context():
    #db.metadata.create_all(db.engine)
    if User.query.all():
      print 'A user already exists! Create another? (y/n):',
      create = raw_input()
      if create == 'n':
          return

    users = [u.username for u in User.query.all()]

    print 'Enter username: ',
    username = raw_input()

    while username in users:
      print 'User already exists. Enter new username: ',
      username = raw_input()
    
    print 'Enter password: ',
    password = raw_input()

    user = User(username=username,
                password=bcrypt.generate_password_hash(password))
    db.session.add(user)

    db.session.commit()
    print 'User added.'

    users = User.query.all()
    print(users)


if __name__ == '__main__':
    sys.exit(main())
