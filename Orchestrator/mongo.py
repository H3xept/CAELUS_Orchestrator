import pymongo
from os import environ

mongo_uri = 'mongodb://mongo/' if 'IN_DOCKER' in environ else 'mongodb://localhost/'
print(f'Trying to connect to {mongo_uri}...')
client = pymongo.MongoClient(mongo_uri)
client.admin.command('ping')
print(f'Connected!')

FLIGHT_DATA = 'FLIGHT_DATA'
USERS = 'USERS'
SIM_OUT = 'SIM_OUT'

def store_new_process(database, process):
    flight_data = database[FLIGHT_DATA]
    flight_data.insert_one(process.to_dict())

def update_process_status(database, process):
    flight_data = database[FLIGHT_DATA]
    query = {'$set':{'status':process.get_status(), 'status_str':process.get_status_string()}}
    flight_data.update_one({'id':process.get_id()}, query)

def get_processes_for_user(database, user_id):
    flight_data = database[FLIGHT_DATA]
    return flight_data.find({'issuer_id':user_id}, {'_id': False})

def cleanup_dangling_processes(database):
    # Set all running to halted
    flight_data = database[FLIGHT_DATA]
    ns = flight_data.update_many({'status':1}, {'$set':{'status':4, 'status_str':"HALTED"}})
    if ns.modified_count > 0:
        print(f'Cleaned up {ns.modified_count} dangling processes')

def store_new_user(database, username, password):
    users = database[USERS]
    if users.find_one({'username':username}):
        return False
    users.insert_one({'username':username, 'password':password})
    return True

def retrieve_user(database, username):
    users = database[USERS]
    return users.find_one({'username':username}, {'_id': False})

def retrieve_process(database, pid):
    flight_data = database[FLIGHT_DATA]
    return flight_data.find_one({'id':pid}, {'_id': False})

def user_owns_operation(database, user_id, operation_id):
    flight_data = database[FLIGHT_DATA]
    res = flight_data.find_one({'mission_payload.operation_id':operation_id, 'issuer_id':user_id})
    return True if res is not None else False

def get_simulation_data(database, operation_id):
    sim_data = database[SIM_OUT]
    return sim_data.find_one({'operation_id':operation_id}, {'_id': False})

def get_operation_id_for_job_id(database, job_id):
    flight_data = database[FLIGHT_DATA]
    res = flight_data.find_one({'id':job_id}, {'_id': False, 'mission_payload.operation_id':True})
    if res is not None:
        return res['mission_payload']['operation_id']