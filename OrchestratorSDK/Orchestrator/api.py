from typing import Union
from .account import Account
import requests
import logging
import json

class OrchestratorAPI():

    def __init__(self, base_url: str, base_account = None):
        self.__logger = logging.getLogger()
        if base_url is None:
            self.__logger.error('OrchestratorAPI cannot work without a base_url!')
            exit(0)

        self.__base_url = base_url
        self.register_user_endpoint = f'{self.__base_url}/register'
        self.authenticate_user_endpoint = f'{self.__base_url}/login'
        self.get_pending_jobs_endpoint = f'{self.__base_url}/pending_jobs'
        self.get_activated_jobs_endpoint = f'{self.__base_url}/jobs'
        self.get_simulation_data_endpoint = f'{self.__base_url}/simulation_data'
        self.schedule_new_mission_endpoint = f'{self.__base_url}/new_mission'
        self.halt_mission_endpoint = f'{self.__base_url}/halt'

        self.__base_account: Account = base_account
    
    def __bearer_header(self, account: Account = None):
        return {'Authorization':f'Bearer {account.get_jwt()}'}

    def register(self, username, password, admin_account: Account = None) -> bool:
        
        if admin_account is None:
            admin_account = self.__base_account
        if admin_account is None:
            self.__logger.error('OrchestratorAPI cannot register without an admin account!')
            return False

        if admin_account.get_username() != 'admin':
            self.__logger.warning('Cannot register a new account if not logged in as admin.')
            return False
        
        response = requests.post(self.register_user_endpoint, json={
            'username':username,
            'password':password
        }, headers=self.__bearer_header(admin_account))

        if response.status_code == 200:
            return True
        
        self.__logger.warning(f'Registration failed for user {username}')
        return False


    def authenticate(self, username, password) -> Union[Account, None]:
        response = requests.post(self.authenticate_user_endpoint, json={
            'username':username,
            'password':password
        })
        if response.status_code == 200:
            data = response.json()
            return Account(username, data['access_token'])
        self.__logger.warning(f'Authentication failed for user {username}')

    def get_pending_jobs(self,account: Account = None):
        if account is None:
            account = self.__base_account
        return requests.get(self.get_pending_jobs_endpoint, headers=self.__bearer_header(account))
    
    def get_activated_jobs(self,account: Account = None):
        if account is None:
            account = self.__base_account
        return requests.get(self.get_activated_jobs_endpoint, headers=self.__bearer_header(account))

    def get_simulation_data(self, job_id, account: Account = None):
        if account is None:
            account = self.__base_account
        return requests.get(f'{self.get_simulation_data_endpoint}/{job_id}', headers=self.__bearer_header(account))

    def schedule_new_mission(self, json_body, docker_img = 'ghcr.io/h3xept/caelus_dt:latest', account: Account = None):
        if account is None:
            account = self.__base_account
        complete_body = {
            'docker_img': docker_img,
            'mission': json_body
        }
        return requests.post(self.schedule_new_mission_endpoint, json=complete_body, headers=self.__bearer_header(account))

    def halt_mission(self, job_id, account: Account = None):
        if account is None:
            account = self.__base_account
        return requests.post(f'{self.halt_mission_endpoint}/{job_id}', headers=self.__bearer_header(account))