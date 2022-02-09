from typing import Union
from flask import request
from .account import Account
import requests
import logging

class Orchestrator():
    __base_url = None

    def __init__(self, base_url: str, base_account = None):
        self.__logger = logging.getLogger()
        if base_url is None:
            self.__logger.error('Orchestrator API cannot work without a base_url!')
        Orchestrator.__base_url = base_url
        self.__base_account: Account = base_account
    
    def __bearer_header(self, account: Account = None):
        return {'Authorization':f'{account.get_jwt()}'}

    register_user_endpoint = f'{__base_url}/register'
    def register(self, username, password, admin_account: Account = None) -> bool:
        
        if admin_account is None:
            admin_account = self.__base_account
        
        if admin_account.get_username() != 'admin':
            self.__logger.warn('Cannot register a new account if not logged in as admin.')
            return False

        response = requests.post(Orchestrator.register_user_endpoint, {
            'username':username,
            'password':password
        }, headers=self.__bearer_header(admin_account))
        if response.status_code == 200:
            return True
        
        self.__logger.warn(f'Registration failed for user {username}')
        return False


    authenticate_user_endpoint = f'{__base_url}/login'
    def authenticate(self, username, password) -> Union[Account, None]:
        response = requests.post(Orchestrator.authenticate_user_endpoint, {
            'username':username,
            'password':password
        })
        if response.status_code == 200:
            data = response.json()
            return Account(username, data.access_token)
        self.__logger.warn(f'Authentication failed for user {username}')

    get_pending_jobs_endpoint = f'{__base_url}/pending_jobs'
    def get_pending_jobs(self,account: Account =None):
        if account is None:
            account = self.__base_account
        return requests.get(Orchestrator.get_pending_jobs_endpoint, headers=self.__bearer_header(account)).json()
        