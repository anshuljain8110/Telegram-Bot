#importing pymongo
from pymongo import MongoClient
#importing env
import os
from dotenv import load_dotenv
load_dotenv()
DBTOKEN = os.environ.get('DBTOKEN')

#creating and connecting to db collections
client = MongoClient(DBTOKEN)
db = client.money_manager
lend = db.lenders