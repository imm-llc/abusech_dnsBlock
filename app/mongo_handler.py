from pymongo import MongoClient
from config import *

client = MongoClient(MONGO_URL)
db = client(MONGO_DB)

def loader(json_record):
    print("hello")


