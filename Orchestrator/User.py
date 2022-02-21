from .auth import get_crypto_context
from .mongo import retrieve_user

class User():

    @staticmethod
    def authenticate(database, username, password):
        user = retrieve_user(database, username)
        try:
            if user and get_crypto_context().verify(password, user['password']):
                return user 
        except Exception as _:
            print(f'Failed to authenticate user {username}')
            return None
    
    def jwt_payload(self):
        return {
            'username':self.username
        }
        
    def __repr__(self):
        return '<User %r>' % self.username