from json import load
from flask import Flask, render_template
from .auth import setup_auth
from flask_compress import Compress
import os
from dotenv import load_dotenv
from .db_helper import setup_default_account

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['APP_SECRET']
app.config['JWT_TOKEN_LOCATION'] = ["headers", "cookies"]

from .User import User
setup_auth(app)
from .router import router

# Create an admin account in the DB
setup_default_account()

Compress(app)

@app.route('/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')

app.register_blueprint(router, url_prefix='/')
