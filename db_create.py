# Modified from: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from database import db
from app import app, bcrypt # to register app with database
import os.path
# See: http://stackoverflow.com/questions/19437883/when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w
with app.app_context():
  # Extensions like Flask-SQLAlchemy now know what the "current" app
  # is while within this block. Therefore, you can now run........
  db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
  api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
  api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
  api.version_control(SQLALCHEMY_DATABASE_URI,
                      SQLALCHEMY_MIGRATE_REPO,
                      api.version(SQLALCHEMY_MIGRATE_REPO))

# TODO: Leave out of production. Just for testing on Heroku before
# I can set up making accounts.
from models import User
with app.app_context():
  user = User(username='admin',
              password=bcrypt.generate_password_hash('password'))
  db.session.add(user)
  db.session.commit()
