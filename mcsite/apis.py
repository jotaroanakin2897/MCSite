#FILE API
from mcsite import app
from mcsite.dbmodel import User, Note
from mcsite import db
from flask import request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
import datetime
from functools import wraps

#DECORATOR

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token =None

    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']

    if not token:
      return jsonify({'message': 'Token missing!'}), 401
    
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
      current_user = User.query.filter_by(public_id = data['public_id']).first()
    except:
      return jsonify({'message': 'Token invalid!'}), 403
    
    return f(current_user, *args, **kwargs)

  return decorated


#API INSERT NEW USER
@app.route('/user', methods=['POST'])
def create_user():
  data = request.get_json()
  hashed_pwd = generate_password_hash(data['password'], method='sha256')

  try:
    new_user = User(public_id = str(uuid.uuid4()), username=data['username'], email=data['email'], password=hashed_pwd, admin=True)
    db.session.add(new_user)
    db.session.commit()
  except:
    return jsonify({'message': 'Insert Error!'}), 403
 
  return jsonify({'message': 'New user created!'})

#API GET ALL USER
@app.route('/user', methods=['GET'])
def get_all_user():
  users = User.query.all()
  output =[]

  for user in users:
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['password'] = user.password
    output.append(user_data)

  return jsonify({'users': output})

#API LOGIN
@app.route('/apilogin', methods=['GET'])
def apilogin():
  auth = request.authorization

  if not auth or not auth.username or not auth.password:
    return make_response('Error Authentication', 401, {'WWW-Autenticate' : 'Basic realm="Login Required"'})

  user = User.query.filter_by(username=auth.username).first()

  if not user:
    return make_response('User do not exists', 401, {'WWW-Autenticate' : 'Basic realm="Login Required"'})

  if check_password_hash(user.password, auth.password):
    token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8')})

  return make_response('Error', 401, {'WWW-Autenticate' : 'Basic realm="Login Required"'})


#API CRUD

@app.route('/apinote', methods=['GET'])
@token_required
def get_all_apinote(current_user):
  notes = Note.query.all()
  output = []

  for note in notes:
    note_data = {}
    note_data['id'] = note.id
    note_data['note'] = note.note
    note_data['user_id'] = note.user_id
    output.append(note_data)

  return jsonify({'notes':output})

@app.route('/apinote/<note_id>', methods=['GET'])
@token_required
def get_apinote(current_user, note_id):
  note = Note.query.filter_by(id=note_id).first()

  if not note:
    return jsonify({'message':'Note not found!'})

  note_data = {}
  note_data['id'] = note.id
  note_data['note'] = note.note
  note_data['user_id'] = note.user_id

  return jsonify(note_data)

@app.route('/apinote', methods=['POST'])
@token_required
def create_apinote(current_user):
  data = request.get_json()

  if not data:
    return jsonify({'message': 'Note not sent!'})
    
  try:
    new_note = Note(note=data['note'], user_id= current_user.public_id)
    db.session.add(new_note)
    db.session.commit()
  except:
    return jsonify({'message': 'Insert Error!'}), 403

  return jsonify({'message': 'Note Insert!'})

@app.route('/apinote/<note_id>', methods=['PUT'])
@token_required
def update_apinote(current_user, note_id):
  note = Note.query.filter_by(id=note_id).first()

  new_note = request.get_json()

  if not new_note:
    return jsonify({'message': 'Note not sent!'})

  if not note:
    return jsonify({'message': 'Note not exits!'})

  try:
    note.note = new_note['note']
    db.session.commit()
  except:
    return jsonify({'message': 'Update Error!'}), 403

  return jsonify({'message': 'Note Updated!'})

@app.route('/apinote/<note_id>', methods=['DELETE'])
@token_required
def delete_apinote(current_user, note_id):
  note = Note.query.filter_by(id=note_id).first()

  if not note:
    return jsonify({'message': 'Note not exits!'})

  try:
    db.session.delete(note)
    db.session.commit()
  except:
    return jsonify({'message': 'Delete Error!'}), 403

  return jsonify({'message': 'Note Deleted!'})




