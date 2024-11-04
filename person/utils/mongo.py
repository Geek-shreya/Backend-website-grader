from django.conf import settings
from db_connection import MONGO_DB

def get_email_collection():
    # MONGO_DB already refers to the database, so we can directly access the collection
    return MONGO_DB['emails']
