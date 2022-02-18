

import logging
logging.basicConfig(level=logging.INFO)
import requests
from dotenv import load_dotenv
load_dotenv()
from os import environ
from Orchestrator.app import app
from waitress import serve
from Orchestrator.docker_helper import setup_docker
import pytest

# before all tests
@pytest.fixture(scope='session')
def docker_setup():
    setup_docker(environ['DOCKER_USER'], environ['DOCKER_EMAIL'], environ['DOCKER_PAT'], environ['DOCKER_REGISTRY'])
    serve(app, host='0.0.0.0', port=5000)
    return f'localhost:5000'

def test_login(orchestrator_addr):
    r = requests.post(f'{orchestrator_addr}/login', json={
        'username':'admin',
        'password':'test'
    })
    assert r.status_code == 200
    assert 'token' in r.json()
    return r.json()['token']