from flask import Flask
from .auth import setup_auth
from .database import setup_db
from flask_jwt import jwt_required

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'owefj()/94hr0p+àùòè3ru9)=Yoikjf3fj'
app.config['JWT_TOKEN_LOCATION'] = ["headers", "cookies"]

setup_db(app)

from .User import User
setup_auth(app)
from .router import router

app.register_blueprint(router, url_prefix='/')
