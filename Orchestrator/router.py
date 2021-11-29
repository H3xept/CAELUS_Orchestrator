from flask import Blueprint, render_template, request, redirect
from flask.helpers import make_response, url_for
from flask.json import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from .process_manager import ProcessManager
import requests
import datetime
from .User import User
from .auth import jwt

router = Blueprint('router', __name__, template_folder='./templates')
router.ps = ProcessManager(max_concurrent_processes=10)

HOME_GET = '/home'
LOGIN_GET = '/'

NEW_PROCESS_POST = '/new_process'
TERMINATE_PROCESS_POST = '/terminate/<pid>'
LOGIN_POST = '/login'

@router.route(HOME_GET)
@jwt_required()
def home():
    return render_template('home.html', processes=router.ps.processes_info())

@router.post(NEW_PROCESS_POST)
def new_process():
    ps:ProcessManager = router.ps
    ps.schedule_process('test','test_mission')
    return redirect(HOME_GET)

@router.post(TERMINATE_PROCESS_POST)
def stop_process(pid):
    ps:ProcessManager = router.ps
    ps.halt_process(pid)
    return redirect(HOME_GET)

@jwt.unauthorized_loader
def unauthorised(_):
    redirect(LOGIN_GET)

@router.route(LOGIN_GET)
def login_get():
    return render_template('login.html')

@router.post(LOGIN_POST)
def login_post():
    try:
        data = {
            'username':request.form.get('username'),
            'password':request.form.get('password')
        }

        user = User.authenticate(data['username'], data['password'])
        if user is not None:
            print(f'Login successful for user {data["username"]}')
            token = create_access_token(user.jwt_payload())
            local_res = make_response(redirect(HOME_GET))
            local_res.set_cookie('access_token_cookie', token, expires=datetime.datetime.utcnow() + datetime.timedelta(hours=24))
        else:
            local_res = redirect(LOGIN_GET)
            return local_res
        return local_res
    except Exception as e:
        print(e)
        return redirect(LOGIN_GET)
    

