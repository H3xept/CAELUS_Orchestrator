import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

def store_new_process(database, process):
    user_root = database[process.get_issuer()]
    user_root.insert_one(process.to_dict())

def update_process_status(database, process):
    user_root = database[process.get_issuer()]
    query = {'$set':{'status':process.get_status(), 'status_str':process.get_status_string()}}
    user_root.update_one({'id':process.get_id()}, query)

def get_processes_for_user(database, user_id):
    user_root = database[user_id]
    return user_root.find({}, {'_id': False})

def cleanup_dangling_processes(database):
    # Set all running to halted
    for c in database.list_collection_names():
        database[c].update_many({'status':1}, {'$set':{'status':4}})
