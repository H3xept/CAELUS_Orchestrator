from flask import Blueprint, render_template, request, redirect, flash
from flask import json
from flask.helpers import make_response, url_for
from flask.json import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import database
from .process_manager import ProcessManager
import datetime
from .User import User
from .auth import jwt, get_crypto_context
from .helpers import validate_payload
from .mongo import client, get_processes_for_user, retrieve_process, store_new_user, user_owns_operation, get_simulation_data, get_operation_id_for_job_id
import logging
from .docker_helper import get_docker
import os

MAX_CONCURRENT_PROCESSES = 'MAX_CONCURRENT_PROCESSES'

mongo_db = client['caelus']
router = Blueprint('router', __name__, template_folder='./templates')
router.ps = ProcessManager(mongo_db, max_concurrent_processes=8 if MAX_CONCURRENT_PROCESSES not in os.environ else int(os.environ[MAX_CONCURRENT_PROCESSES]), logger=logging.getLogger('waitress'))

JOBS_GET = '/jobs'
PENDING_JOBS_GET = '/pending_jobs'
REGISTER_POST = '/register'

NEW_PROCESS_POST = '/new_mission'
HALT_PROCESS_POST = '/halt/<pid>'
LOGIN_POST = '/login'
SIM_OUT_GET = '/simulation_data/<job_id>'

@router.get('/')
def index():
    return redirect('/docs')
    
@router.post(NEW_PROCESS_POST)
@jwt_required()
def new_process():
    payload = request.get_json()
    payload_valid = validate_payload(payload)
    print(payload_valid)
    if payload_valid:
        ps:ProcessManager = router.ps
        docker_img = payload['docker_img']
        mission_data = payload['mission']
        issuer_username = get_jwt_identity()['username']
        job_id = ps.schedule_process(docker_img,mission_data,issuer_username)
        if job_id is not None:
            return make_response(jsonify({
                'job_id':job_id
            }), 200)
        else:
            return make_response(jsonify({
                'msg':f'Requested image ({docker_img}) not present.',
                'imgs_available': [img.tags for img in get_docker().client.images.list() if img.tags != [] and any(['caelus' in name for name in img.tags])]
            }), 402)
    else:
        return make_response(jsonify({}), 400)

@router.post(HALT_PROCESS_POST)
@jwt_required()
def stop_process(pid):
    # Check if mission is owned by user / if user is admin
    user_id = get_jwt_identity()['username']
    is_admin = user_id == 'admin'
    mission_owned = retrieve_process(mongo_db, pid)
    if not (is_admin or mission_owned):
        return make_response(jsonify({'msg':'You do not own that mission.'}), 401)

    ps:ProcessManager = router.ps
    if ps.halt_process(pid):
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({'msg': 'Could not halt mission. (The mission might already have completed)'}), 400)

@router.get(JOBS_GET)
@jwt_required()
def get_jobs():
    user_id = get_jwt_identity()['username']
    return make_response(jsonify(list(get_processes_for_user(mongo_db, user_id))), 200)

@router.get(PENDING_JOBS_GET)
@jwt_required()
def get_pending_jobs():
    user_id = get_jwt_identity()['username']
    return make_response(jsonify(router.ps.get_process_queue_for_user(user_id)), 200)

@router.get(SIM_OUT_GET)
@jwt_required()
def get_sim_data(job_id):
    operation_id = get_operation_id_for_job_id(mongo_db, job_id)

    user_id = get_jwt_identity()['username']
    if not user_owns_operation(mongo_db, user_id, operation_id):
        return make_response(jsonify({'msg':f'You do not own operation for job {job_id}'}), 401)
    sim_data = get_simulation_data(mongo_db, operation_id)
    if sim_data is not None:
        return make_response(jsonify(sim_data), 200)
    return make_response(jsonify({'msg':'Simulation data unavailable. Try again later.'}), 404)


@jwt.unauthorized_loader
def unauthorised(_):
    return make_response(jsonify({}), 401)

@router.post(REGISTER_POST)
@jwt_required()
def register_user():
    
    is_admin = get_jwt_identity()['username'] == 'admin'
    if not is_admin:
        return make_response(jsonify({'msg':'You must be logged in as admin to register new users!'}), 401)

    cc = get_crypto_context()
    data_json = request.get_json()
    pwd_hash = cc.hash(data_json['password'])
    if store_new_user(mongo_db, data_json['username'], pwd_hash):
        return make_response(jsonify({}), 200)
    return make_response(jsonify({}), 400)

import traceback

@router.post(LOGIN_POST)
def login_post():
    try:
        data_json = request.get_json()
        data = {
            'username':data_json['username'],
            'password':data_json['password']
        }
        user = User.authenticate(mongo_db, data['username'], data['password'])
        if user is not None:
            print(f'Login successful for user {data["username"]}')
            delta = datetime.timedelta(hours=24)
            token = create_access_token(user, expires_delta=delta)
            token_expiry = datetime.datetime.utcnow() + delta
            local_res = make_response(jsonify({
                'access_token':token,
                'expires':token_expiry
            }), 200)
            local_res.set_cookie('access_token_cookie', token, expires=token_expiry)
        else:
            local_res = make_response(jsonify({}), 401)
        return local_res
    except Exception as e:
        return make_response(jsonify({
                'msg': str(traceback.format_exc())
            }), 500)
    

