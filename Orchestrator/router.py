from flask import Blueprint, render_template, request, redirect, flash
from flask.helpers import make_response, url_for
from flask.json import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from .process_manager import ProcessManager
import datetime
from .User import User
from .auth import jwt, get_crypto_context
from .helpers import validate_payload
from .mongo import client, get_processes_for_user, store_new_user

mongo_db = client['caelus']
router = Blueprint('router', __name__, template_folder='./templates')
router.ps = ProcessManager(mongo_db, max_concurrent_processes=10)

JOBS_GET = '/jobs'
REGISTER_POST = '/register'

NEW_PROCESS_POST = '/new_mission'
TERMINATE_PROCESS_POST = '/terminate/<pid>'
LOGIN_POST = '/login'
@router.post(NEW_PROCESS_POST)

@jwt_required()
def new_process():
    payload = request.get_json()
    payload_valid = validate_payload(payload)
    if payload_valid:
        ps:ProcessManager = router.ps
        docker_img = payload['docker_img']
        mission_data = payload['mission']
        issuer_username = get_jwt_identity()['username']
        job_id = ps.schedule_process(docker_img,mission_data,issuer_username)
        return make_response(jsonify({
            'job_id':job_id
        }), 200)
    else:
        return make_response(jsonify({}), 400)

@router.post(TERMINATE_PROCESS_POST)
@jwt_required()
def stop_process(pid):
    ps:ProcessManager = router.ps
    ps.halt_process(pid)
    return make_response(jsonify({}), 200)

@router.get(JOBS_GET)
@jwt_required()
def get_jobs():
    user_id = get_jwt_identity()['username']
    return make_response(jsonify(list(get_processes_for_user(mongo_db, user_id))), 200)

@jwt.unauthorized_loader
def unauthorised(_):
    return make_response(jsonify({}), 401)

@router.post(REGISTER_POST)
def register_user():
    cc = get_crypto_context()
    data_json = request.get_json()
    if store_new_user(mongo_db, data_json['username'], cc.hash(data_json['password'])):
        return make_response(jsonify({}), 200)
    return make_response(jsonify({}), 400)

@router.post(LOGIN_POST)
def login_post():
    try:
        data_json = request.get_json()
        print(data_json)
        data = {
            'username':data_json['username'],
            'password':data_json['password']
        }
        user = User.authenticate(mongo_db, data['username'], data['password'])
        if user is not None:
            print(f'Login successful for user {data["username"]}')
            token = create_access_token(user)
            token_expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            local_res = make_response(jsonify({
                'access_token':token,
                'expires2':token_expiry
            }), 200)
            local_res.set_cookie('access_token_cookie', token, expires=token_expiry)
        else:
            local_res = make_response(jsonify({}), 401)
        return local_res
    except Exception as e:
        print(e)
        return make_response(jsonify({
                'msg': 'Something went wrong'
            }), 500)
    

