from database import db

class User(db.Model):
  __tablename__ = 'user'  # necessary?

  #id = db.Column(db.Integer, primary_key=True)
  #nickname = db.Column(db.String(64), index=True, unique=True)
  #email = db.Column(db.String(120), index=True, unique=True)
  username = db.Column(db.String(120),primary_key=True)
  password = db.Column(db.String(120), index=True, unique=False)

  def __repr__(self):
    return '<User %r>' % (self.username)

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_username(self):
    try:
      return unicode(self.username)  # python 2
    except NameError:
      return str(self.username)  # python 3

  def get_id(self):
    return self.get_username()

#  def get_id(self):
#    try:
#      return unicode(self.id)  # python 2
#    except NameError:
#      return str(self.id)  # python 3
