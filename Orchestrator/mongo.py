import pymongo

client = pymongo.MongoClient("mongodb://mongo/")

FLIGHT_DATA = 'FLIGHT_DATA'
USERS = 'USERS'

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
    ns = flight_data.update_many({'status':1}, {'$set':{'status':4}})
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
    print(f'Finding user with us: {username}')
    return users.find_one({'username':username}, {'_id': False})