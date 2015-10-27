from models import Argmap
from database import db

def CreateIfNotFound(username = 'default_user', mapname='map1'):
  argmap = Argmap.query.get(mapname)
  if argmap:
    msg = 'found requested map: {}'.format(mapname)
  else:
    msg = 'could not find requested map: {}'.format(mapname)
    src = 'static/data.json'
    argmap = Argmap(title=mapname,
                    data=open(src).read())
    db.session.add(argmap)
    db.session.commit()

  return msg


def loadMap(mapname):
  argmap = Argmap.query.get(mapname)
  return argmap.GetData()


def SaveMap(mapname, json_text):
  argmap = Argmap.query.get(mapname)
  argmap.SetData(json_text)


def GetMapnames():
  mapnames = []
  try:
    [x.GetMapname() for x in Argmap.query.all()]
  except:
    raise
  return mapnames
