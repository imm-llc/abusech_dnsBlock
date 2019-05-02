from pymongo import MongoClient
from config import MONGO_URL, MONGO_DB, MONGO_COLLECTION
from app_logger import logger
import json
from bson import json_util

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]

def insert_malicious_record(json_record):
    try:
        json_record = json_util.loads(json_record)
        db[MONGO_COLLECTION].insert_one(json_record)
        logger.info("Inserted record into Mongo")
        return True
    except Exception as e:
        logger.error("Error inserting record into mongo: {}".format(str(e)))
        return False



