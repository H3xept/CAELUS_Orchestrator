from flask import Flask, render_template
from .auth import setup_auth
from flask_compress import Compress

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'owefj()/94hr0p+àùòè3ru9)=Yoikjf3fj'
app.config['JWT_TOKEN_LOCATION'] = ["headers", "cookies"]

from .User import User
setup_auth(app)
from .router import router

Compress(app)

@app.route('/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')

app.register_blueprint(router, url_prefix='/')
