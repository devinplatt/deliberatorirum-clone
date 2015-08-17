from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine(SQLALCHEMY_DATABASE_URI)
m = MetaData()
m.reflect(engine)
for table in m.tables.values():
    print(table.name)
    for column in table.c:
        print("\t{0}".format(column.name))
        # print("\t{0}".format(column))


from app import app
from database import db
from models import User

with app.app_context():
  #db.metadata.create_all(db.engine)
  #users = [u.username for u in User.query.all()]
  # Will see that passwords are hashed:
  users = [[u.username, u.password] for u in User.query.all()]
  print(users)
  #print(User.query.all())
