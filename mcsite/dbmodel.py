from mcsite import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User (db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.String(50), unique=True, nullable=False)
  username = db.Column(db.String(100), unique=True, nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  admin = db.Column(db.Boolean)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"



class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  note = db.Column(db.String(200))
  user_id = db.Column(db.String(50))

class citta(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  citta = db.Column(db.String(200))

  