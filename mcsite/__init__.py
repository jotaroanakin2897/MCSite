from flask import Flask, url_for
from flask_login import LoginManager
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
from flask_migrate import Migrate

migrate = Migrate()


from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mcdata.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY']='8d332d0af2408ec1e0b21f24f6dadb5b'

login_manager = LoginManager(app)

app.config["MONGO_URI"]="mongodb://localhost:27017/MCData"
mongo = PyMongo(app)


from mcsite import routes, apis, apimongo