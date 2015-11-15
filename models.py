from database import db
from sqlalchemy import ForeignKey

class Argmap(db.Model):
  __tablename__ = 'argmap'

  # TODO: use argmap_id instead of argmap title.
  # To allow argmap renames.
  title = db.Column(db.String(120),primary_key=True)
  latest_revision_id = db.Column(db.Integer, ForeignKey("revision.revision_id"), nullable=False)

  def GetMapname(self):
    try:
      return unicode(self.title)  # python 2
    except NameError:
      return str(self.title)  # python 3

  def GetLatestRevision(self):
    return self.latest_revision_id

  def SetLatestRevision(self, revision_id):
    self.latest_revision_id = revision_id
    db.session.commit()

  def __repr__(self):
    return '<Title %r>' % (self.title)  

class Revision(db.Model):
  __tablename__ = 'revision'

  revision_id = db.Column(db.Integer, primary_key=True)
  parent_revision_id = db.Column(db.Integer, ForeignKey("revision.revision_id"), nullable=True)
  title = db.Column(db.String(120))
  content_id = db.Column(db.Integer, ForeignKey("content.content_id"), nullable=False)

  def GetRevisionId(self):
      return self.revision_id

  def GetMapname(self):
    try:
      return unicode(self.title)  # python 2
    except NameError:
      return str(self.title)  # python 3

  def GetContentId(self):
      return self.content_id

  def __repr__(self):
    return '<revision_id %r>' % (self.revision_id) 


class Content(db.Model):
  __tablename__ = 'content'

  content_id = db.Column(db.Integer, primary_key=True)
  data = db.Column(db.Text(), index=True, unique=False)

  def GetContentId(self):
      return self.content_id

  def GetData(self):
    try:
      return unicode(self.data)  # python 2
    except NameError:
      return str(self.data)  # python 3

  def SetData(self, data):
    self.data = data
    db.session.commit()

  def __repr__(self):
    return '<content_id %r>' % (self.content_id) 


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
