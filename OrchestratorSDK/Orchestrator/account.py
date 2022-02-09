
class Account():

    def __init__(self, username, jwt):
        self.__username = username
        self.__jwt = jwt
    
    def get_username(self):
        return self.__username

    def get_jwt(self):
        return self.__jwt
