from .auth import get_crypto_context
from .mongo import retrieve_user

class User():

    @staticmethod
    def authenticate(database, username, password):
        user = retrieve_user(database, username)
        if user and get_crypto_context().verify(password, user['password']):
            return user
    
    def jwt_payload(self):
        return {
            'username':self.username
        }
        
    def __repr__(self):
        return '<User %r>' % self.username