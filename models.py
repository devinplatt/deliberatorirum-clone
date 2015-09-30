from database import db

class Argmap(db.Model):
  __tablename__ = 'argmap'

  title = db.Column(db.String(120),primary_key=True)
  data = db.Column(db.Text(), index=True, unique=False)

  def GetMapname(self):
    try:
      return unicode(self.title)  # python 2
    except NameError:
      return str(self.title)  # python 3

  def GetData(self):
    try:
      return unicode(self.data)  # python 2
    except NameError:
      return str(self.data)  # python 3

  def SetData(self, data):
    self.data = data
    db.session.commit()

  def __repr__(self):
    return '<Title %r>' % (self.title)  

class User(db.Model):
  __tablename__ = 'user'  # necessary?

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
