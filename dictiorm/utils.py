from pymongo import MongoClient



###############################################################################
# Generic helper functions
###############################################################################

def id_to_str(document):
    if document and '_id' in document:
        document['_id'] = str(document['_id'])
    return document



def combine(recent_data, past_data):
    result = past_data
    for key in recent_data:
        result[key] = recent_data[key]
    return result



###############################################################################
# MongoDB
###############################################################################

def database_connection(url, port, database_name, user, password):
    db_connection = MongoClient(url, port)
    db = db_connection[database_name]
    db.authenticate(user, password)
    return db



def collection_connection(url, port, database_name, user, password, collection):
    return database_connection(url, port, database_name, user, password)[collection]



