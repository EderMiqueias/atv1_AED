import pymongo


url = "localhost"
port = 27017
cliente_db = pymongo.MongoClient(host=url, port=port)


def get_db():
    db = cliente_db.sistema_aed
    return db
