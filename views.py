from database import db
from flask import current_app, Blueprint
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json, jsonify, make_response
import logging
import model_utils
import os
import urllib

from flask.ext.login import login_required

bp = Blueprint('bp', __name__,
               template_folder='templates',
               static_folder='static')


def loadJson(filename = 'static/data.json'):
  return json.load(open(filename))

@bp.route('/get_maps')
def get_maps():
  maps = []
  try:
    maps = model_utils.GetMapnames()
    current_app.logger.info('maps (should not be []: {0}'.format(maps))
  except:
    maps = []
    current_app.logger.warning('GetMapnames() call failed!')
  current_app.logger.info('maps: {0}'.format(maps))
  msg = "{\n"
  for i in range(len(maps)):
    msg += "\"m" + str(i) + "\": \"" + maps[i] + "\","
  msg = msg[:-1]
  msg += "\n}"
  current_app.logger.info('msg: {0}'.format(msg))
  current_app.logger.info('maps return value: {0}'.format(msg))
  return msg

@bp.route('/create_map')
def create_map():
  mapname = request.query_string
  mapname = urllib.unquote(mapname)
  current_app.logger.info('Request: {0}'.format(request))
  current_app.logger.info('Query String: {0}'.format(mapname))
  # SANITIZE INPUT! (NO ".." ETC.)
  if mapname == 'none':
    mapname = 'map1'
  if session.get('logged_in'):
    # CHECK THAT THE FILE EXISTS
    msg = model_utils.CreateIfNotFound(session['username'], mapname)
    current_app.logger.info('Model msg: {0}'.format(msg))
  else:
    # CHECK THAT THE FILE EXISTS
    msg = model_utils.CreateIfNotFound(mapname = mapname)
    current_app.logger.info('Model msg: {0}'.format(msg))
  return get_maps()

@bp.route('/get_tree')
def get_tree():
  mapname = request.query_string
  # user = request.args.get('user')
  mapname = urllib.unquote(mapname)
  current_app.logger.info('Request: {0}'.format(request))
  current_app.logger.info('Query String: {0}'.format(mapname))
  # SANITIZE INPUT! (NO ".." ETC.)
  if mapname == 'none':
    mapname = 'map1'
  filename = None
  if session.get('logged_in'):
    # CHECK THAT THE FILE EXISTS
    msg = model_utils.CreateIfNotFound(session['username'], mapname)
    current_app.logger.info('Git msg: {0}'.format(msg))
    #filename = model_utils.user_dir(session['username'], mapname)
  else:
    # CHECK THAT THE FILE EXISTS
    msg = model_utils.CreateIfNotFound(mapname = mapname)
    current_app.logger.info('Git msg: {0}'.format(msg))
  # tree comes in as string
  tree = model_utils.loadMap(mapname)
  current_app.logger.info('tree: {0}'.format(tree))
  current_app.logger.info('tree type: {0}'.format(type(tree)))
  # convert tree to python object
  tree = json.loads(tree)
  tree["mapname"] = mapname
  msg = json.dumps(tree)
  current_app.logger.info('get_tree msg: {0}'.format(msg))
  # return tree as string again
  return jsonify(tree)

# TODO: make this only allowable for logged in users
# See: http://stackoverflow.com/questions/11839855/flask-not-getting-any-data-from-jquery-request-data
@bp.route('/set_tree', methods=['POST'])
# disabling login requirement until I make it possible to set up
# accounts
#@login_required
def set_tree():
  current_app.logger.info('Request: {0}'.format(request))
  data = (request.form).to_dict()
  keys = data.keys()
  # TODO: if keys' length is 0, return bad status
  json_text = keys[0]
  current_app.logger.info('Request data: {0}'.format(json_text))
  mydict = json.loads(json_text)
  current_app.logger.info('mydict: {0}'.format(mydict))
  mapname = mydict["mapname"]
  tree = mydict["tree"]
  current_app.logger.info('mapname: {0}'.format(mapname))
  current_app.logger.info('tree: {0}'.format(tree))
  json_text = json.dumps(tree)
  current_app.logger.info('json_text: {0}'.format(json_text))

  response = make_response("success")
  current_app.logger.info('Response: {0}'.format(response))
  # SHOULD VERIFY THE DATA SENT TO US RIGHT HERE!!!!!!! 
  # CHECK GIT STATUS AS DOING THIS
  model_utils.SaveMap(mapname, json_text)
  return response

@bp.route('/')
def show_index():
  return redirect(url_for('bp.nav'))

@bp.route('/nav')
def nav():
  return render_template('nav.html')

@bp.route('/map/<mapid>')
def mappage(mapid):
  if mapid in model_utils.GetMapnames():
    return render_template('map.html', mapid=mapid)
  else:
    return 'Map {0} not found'.format(mapid)

@bp.route('/map/<mapid>/revision/<revid>')
def mappage_rev(mapid, revid):
  if mapid in model_utils.GetMapnames():
    return render_template('revision.html',
                           mapid=mapid, revid=revid)
  else:
    return 'Map {0} not found'.format(mapid)

@bp.route('/map/<mapid>/revisions')
def revisions(mapid):
  if mapid in model_utils.GetMapnames():
    return render_template('revisions.html', mapid=mapid)
  else:
    return 'Map {0} not found'.format(mapid)

@bp.route('/get_revisions')
def get_revisions():

  revisions = []
  try:
    mapname = request.query_string
    #mapname = request.args.get('mapname')
    mapname = urllib.unquote(mapname)
    #revision_id = request.args.get('revid')
    current_app.logger.info('Request: {0}'.format(request))
    current_app.logger.info('Query String: {0}'.format(mapname))
    #current_app.logger.info('Query String[revid]: {0}'.format(revision_id))
    revision_ids, parent_ids = model_utils.GetRevisions(mapname)
    current_app.logger.info('revisions (should not be []): {0}'.format(revision_ids))
    revisions = revision_ids
  except:
    revisions = []
    current_app.logger.warning('GetRevisions() call failed!')
  current_app.logger.info('revisions: {0}'.format(revisions))
  
  # SANITIZE INPUT! (NO ".." ETC.)

  msg = "{\n"
  for i in range(len(revisions)):
    msg += "\"r" + str(i) + "\": \"" + revisions[i] + "\","
  msg = msg[:-1]
  msg += "\n}"

  current_app.logger.info('msg: {0}'.format(msg))
  current_app.logger.info('revisions return value: {0}'.format(msg))
  return msg

@bp.route('/get_tree_revision')
def get_tree_revision():
  # mapname = request.query_string
  qs = request.query_string
  current_app.logger.info('qs: {0}'.format(qs))
  #mapname = request.args.get('mapname')
  split = qs.split('&')
  mapname = split[0].split('=')[1]
  current_app.logger.info('mapname: {0}'.format(mapname))
  mapname = urllib.unquote(mapname)  # unquote_plus() instead?
  revision_id = split[1].split('=')[1]
  #revision_id = request.form.get('revid')

  current_app.logger.info('Request: {0}'.format(request))
  current_app.logger.info('Query String[mapid]: {}'.format(mapname))
  current_app.logger.info('Query String[revid]: {}'.format(revision_id))

  # SANITIZE INPUT! (NO ".." ETC.)
  # SHOULD CHECK THAT THE MAP EXISTS

  # tree comes in as string
  tree = model_utils.loadMap(mapname, revision_id)
  current_app.logger.info('tree: {0}'.format(tree))
  current_app.logger.info('tree type: {0}'.format(type(tree)))
  # convert tree to python object
  tree = json.loads(tree)
  tree["mapname"] = mapname
  msg = json.dumps(tree)
  current_app.logger.info('get_tree msg: {0}'.format(msg))
  # return tree as string again
  return jsonify(tree)


#@bp.route('/diff')
#def diff():
#  return render_template('diff.html')

@bp.route('/map/<mapid>/diff/<revid1>/<revid2>')
def diff(mapid, revid1, revid2):
  return render_template('diff.html',
                         mapid=mapid, revid1=revid1, revid2=revid2)
