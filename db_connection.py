from pymongo import MongoClient  

url = 'mongodb+srv://root:RHVvLbi5tJgqUxzm@cluster0.lq35h.mongodb.net'
MONGO_CLIENT = MongoClient(url)

MONGO_DB = MONGO_CLIENT['grader'] 
