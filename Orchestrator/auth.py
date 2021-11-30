from flask_jwt_extended import JWTManager
from passlib.context import CryptContext

crypto_context = None
jwt = None

def setup_auth(app):
    global crypto_context
    global jwt
    crypto_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    jwt = JWTManager(app)

def get_crypto_context():
    return crypto_context

def get_jwt():
    return jwt