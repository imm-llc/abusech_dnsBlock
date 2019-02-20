from pymongo import MongoClient
from config import *
from app_logger import *

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]

def loader(json_record):
    try:
        db[MONGO_COLLECTION].insert_one(json_record)
        logger.info("Inserted record into Mongo")
        return True
    except Exception as e:
        logger.error(str(e))
        return False



