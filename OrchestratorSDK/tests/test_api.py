

import logging
logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv
load_dotenv()
from os import environ
from Orchestrator.app import app
from waitress import serve
from Orchestrator.docker_helper import setup_docker
import pytest

# before all

setup_docker(environ['DOCKER_USER'], environ['DOCKER_EMAIL'], environ['DOCKER_PAT'], environ['DOCKER_REGISTRY'])
serve(app, host='0.0.0.0', port=5000)