from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, validators
from wtforms.validators import ValidationError

from mcsite.dbmodel import User


class RegistrationForm(FlaskForm):
  username = StringField('Username',[validators.DataRequired(), validators.Length(min=4, max=50)] )
  email = StringField('Email', [validators.DataRequired(), validators.Email()])
  password = PasswordField('Password', [validators.DataRequired()])
  confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password')])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username = username.data).first()
    if user:
      raise ValidationError('Username già esiste!')

  def validate_email(self, email):
    user = User.query.filter_by(email = email.data).first()
    if user:
      raise ValidationError('Email già esiste!')

class LoginForm(FlaskForm):
  username = StringField('Username',[validators.DataRequired(), validators.Length(min=4, max=50)] )
  password = PasswordField('Password', [validators.DataRequired()])
  remember = BooleanField('Remember')
  submit = SubmitField('Login')

class NoteForm(FlaskForm):
  note = TextAreaField('Note', [validators.DataRequired()])
  submit = SubmitField('Send')