import git
import os

def user_dir(username = 'default_user', mapname = 'map1'):
  return os.path.join('./tempMaps', username, mapname)

def change_user(local_dir, name='joeblow', email='joe@mail.com'):
  # want to edit just the local config, like in:
  # http://www.thebuzzmedia.com/git-tip-git-config-user-name-and-user-email-for-local-not-global-config/
  # see: https://home.regit.org/2014/05/playing-with-python-git/
  rep = git.Repo(local_dir)
  cw = rep.config_writer()
  cw.set_value("user", "email", email)
  cw.set_value("user", "name", name)
  cw.release()

def createRepo(username = 'default_user', mapname = 'map1'):
  repo = mapname
  origin_dir = os.path.join('./maps', mapname)
  #temp_dir = os.path.join('./tempMaps', mapname)
  temp_dir = user_dir(username, mapname)

  # not checking if the repo already exists, but this is a safe
  # operation in any case
  g1 = git.Repo.init(origin_dir, bare=True)

  # did not check if repo already exists, so have to handle both
  # cases
  origin = None
  try:
    origin = g1.remote()
  except ValueError:
    origin = g1.create_remote('origin', origin_dir)

  temp = None
  if os.path.isdir(temp_dir):
    temp = git.Repo(temp_dir)
  else:
    temp = git.Repo.clone_from(origin_dir, temp_dir)

  return [g1, origin, temp]

def push_change(local_dir, msg = "generic commit msg", to_add = ['data.json']):
  print('push sequence')
  rep = git.Repo(local_dir)
  origin = rep.remote()
  info = origin.pull()
  print(info)
  rep.index.add(to_add)
  rep.index.commit(msg)
  print('pushing')
  pushinfo = origin.push(rep.head)[0]
  print(pushinfo.summary)

import shutil
def CreateDefault(username = 'default_user', mapname = 'map1', temppath = 'tempMaps/map1'):
  g1, origin, temp = createRepo(username, mapname)
  src = 'static/data.json'
  dst = os.path.join(temppath, 'data.json') 
  #dst = 'tempMaps/map1/data.json'
  #if not os.path.exists(temppath):
  #  os.makedirs(temppath)
  shutil.copyfile(src, dst)
  return temp

def createDefaultAndPush(username = 'default_user', mapname ='map1', temppath = 'tempMaps/map1'):
  temp = CreateDefault(username, mapname, temppath)
  push_change(temppath, 'pushing the default map')
  return temp

def LoadOrCreate(username = 'default_user', mapname='map1'):
  origin_dir = './maps'
  temp_dir = './tempMaps'
  msg = ''
  originpath = os.path.join(origin_dir, mapname)
  #temppath = os.path.join(temp_dir, mapname)
  temppath = user_dir(username, mapname)
  temp = None
  if os.path.isdir( originpath ):
    if os.path.isdir( temppath ):
      shutil.rmtree(temppath)
    temp = git.Repo.clone_from(originpath, temppath)
    msg = 'repo loaded'
  else:
    temp = createDefaultAndPush(username, mapname, temppath)
    msg = 'repo created'
  change_user(temppath, username, 'joe@mail.com')

  return msg

