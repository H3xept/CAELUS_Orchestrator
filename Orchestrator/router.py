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

@router.route("/home")
@jwt_required()
def home():
    return render_template('home.html', processes=router.ps.processes_info())

@router.post('/new_process')
def new_process():
    ps:ProcessManager = router.ps
    ps.schedule_process('test','test_mission')
    return redirect('/home')

@jwt.unauthorized_loader
def unauthorised(_):
    redirect('/')

@router.route("/")
def login_get():
    return render_template('login.html')

@router.post("/login")
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
            local_res = make_response(redirect('/home'))
            local_res.set_cookie('access_token_cookie', token, expires=datetime.datetime.utcnow() + datetime.timedelta(hours=24))
        else:
            local_res = redirect('/')
            return local_res
        return local_res
    except Exception as e:
        print(e)
        return redirect('/')
    

