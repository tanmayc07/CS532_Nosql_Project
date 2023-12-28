import os
from pymongo import MongoClient
# from dotenv import load_dotenv
# from pathlib import Path

# dotenv_path = Path('../.env')
# load_dotenv(dotenv_path=dotenv_path)

uri = "mongodb+srv://tanmayc:" + os.getenv('CONNECTION_PASS') + "@cluster0.ls88hji.mongodb.net/?retryWrites=true&w=majority"

def get_database_connection():
    client = MongoClient(uri)
    db = client[os.getenv('DB_NAME')]
    collection = db["stats"]
    return collection
