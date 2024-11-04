from pymongo import MongoClient  

url = 'mongodb://localhost:27017'
MONGO_CLIENT = MongoClient(url)

MONGO_DB = MONGO_CLIENT['emails'] 
