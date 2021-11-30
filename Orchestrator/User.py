from sqlalchemy.orm import relationship
from .database import db
from .auth import get_crypto_context

class User(db.Model):

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and get_crypto_context().verify(password, user.password):
            return user

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    
    def jwt_payload(self):
        return {
            'username':self.username
        }
        
    def __repr__(self):
        return '<User %r>' % self.username