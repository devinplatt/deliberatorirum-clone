from database import db
from flask import current_app, Blueprint
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json, jsonify, make_response
import logging
import model_utils
import os

from flask.ext.login import login_required

bp = Blueprint('bp', __name__,
               template_folder='templates',
               static_folder='static')


def loadJson(filename = 'static/data.json'):
  return json.load(open(filename))

@bp.route('/get_maps')
def get_maps():
  maps = model_utils.GetMapnames()
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
  current_app.logger.info('Request: {0}'.format(request))
  current_app.logger.info('Query String: {0}'.format(mapname))
  # SANITIZE INPUT! (NO ".." ETC.)
  if mapname == 'none':
    mapname = 'map1'
  if session.get('logged_in'):
    # CHECK THAT THE FILE EXISTS
    msg = model_utils.CreateIfNotFound(session['username'], mapname)
    current_app.logger.info('Git msg: {0}'.format(msg))
  else:
    # CHECK THAT THE FILE EXISTS
    msg = model_utils.CreateIfNotFound(mapname = mapname)
    current_app.logger.info('Git msg: {0}'.format(msg))
  return get_maps()

@bp.route('/get_tree')
def get_tree():
  mapname = request.query_string
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
@login_required
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

@bp.route('/diff')
def diff():
  return render_template('diff.html')
