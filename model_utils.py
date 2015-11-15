from models import Argmap, Revision, Content
from database import db

from flask import current_app
import logging

def GetRevisions(mapname):
  revisions = Revision.query.filter_by(title=mapname)
  revision_ids = [str(revision.revision_id) for revision in revisions]
  parent_ids = [str(revision.parent_revision_id) for revision in revisions]
  return revision_ids, parent_ids

def CreateMap(mapname, json_text):
  content = Content(data=json_text)
  db.session.add(content)
  db.session.flush()

  current_app.logger.info('content id: {0}'.format(content.content_id))
  revision = Revision(title=mapname,
                      parent_revision_id=None,
                      content_id=content.content_id)
  db.session.add(revision)
  db.session.flush()
  current_app.logger.info('revision id: {0}'.format(revision.revision_id))

  argmap = Argmap(title=mapname,
                  latest_revision_id = revision.revision_id)
  db.session.add(argmap)

  db.session.commit()

def CreateIfNotFound(username = 'default_user', mapname='map1'):
  argmap = Argmap.query.get(mapname)
  if argmap:
    msg = 'found requested map: {}'.format(mapname)
  else:
    msg = 'could not find requested map: {}'.format(mapname)
    src = 'static/data.json'
    CreateMap(mapname=mapname,
              json_text=open(src).read())
  return msg

def GetArgmapContent(mapname, revision_id = None):
  argmap = Argmap.query.get(mapname)
  if revision_id is None:
    argmap = Argmap.query.get(mapname)
    revision_id = argmap.latest_revision_id
  revision = Revision.query.get(revision_id)
  content = Content.query.get(revision.content_id)
  data = content.GetData()
  return data

def loadMap(mapname, revision_id = None):
  #argmap = Argmap.query.get(mapname)
  #return argmap.GetData()
  return GetArgmapContent(mapname, revision_id)


def SaveMap(mapname, json_text):
  # update argmap table, revision table, content table 
  argmap = Argmap.query.get(mapname)
  # argmap.SetData(json_text)
  old_revision_id = argmap.latest_revision_id
  content = Content(data=json_text)
  db.session.add(content)
  db.session.flush()

  revision = Revision(title=argmap.title,
                      parent_revision_id=old_revision_id,
                      content_id=content.content_id)
  db.session.add(revision)
  db.session.flush()

  argmap.latest_revision_id = revision.revision_id
  db.session.add(argmap)
  
  db.session.commit()

def GetMapnames():
  mapnames = []
  try:
    mapnames = [x.GetMapname() for x in Argmap.query.all()]
  except:
    raise
  return mapnames
