    # config.py
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'database': 'dating_app'
}

MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'dating_app'
}


from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['dating_app']
collection = db['test_collection']
collection.insert_one({"name": "John", "age": 30})
result = collection.find_one({"name": "John"})
print("MongoDB document:", result)
