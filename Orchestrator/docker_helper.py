import sys
import docker
import logging

class Docker():

    DT_IMAGE = '/h3xept/caelus_dt:latest'

    def __init__(self, user, email, access_token, registry_base_uri):
        self.__creds = {
            'username':user,
            'email':email,
            'password':access_token,
            'serveraddress':registry_base_uri
        }
        
        self.client = docker.DockerClient()
        self.__logger = logging.getLogger()

        self.docker_auth()
        self.pull_latest_dt()

    def docker_auth(self):
        self.client.login(
            self.__creds['username'],
            self.__creds['password'],
            self.__creds['email'],
            self.__creds['serveraddress']
        )

    def pull_latest_dt(self):
        if 'unittest' not in sys.modules.keys():
            try:
                self.__logger.info('Checking local DT image...')
                self.client.images.get(f'{self.__creds["serveraddress"]}{Docker.DT_IMAGE}')
            except:
                self.__logger.info('Image not present!')
                self.__logger.info(f'Pulling latest of {Docker.DT_IMAGE} from {self.__creds["serveraddress"]}')
                self.client.images.pull(f'{self.__creds["serveraddress"]}{Docker.DT_IMAGE}', auth_config=self.__creds)
                self.__logger.info('Image pulled successfully.')


docker_singleton = None
def setup_docker(user, email, access_token, registry_base_uri):
    global docker_singleton
    docker_singleton = Docker(user, email, access_token, registry_base_uri)
    return docker_singleton

def get_docker():
    return docker_singleton