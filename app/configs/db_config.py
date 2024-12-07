import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')

# client = AsyncIOMotorClient(CONNECTION_STRING)
# db = client["url_shortner_service_database"]
# try:
#     client.admin.command("ping")
#     print('ping')
# except Exception as e:
#     print(e)

class MongoDbDatabase:
    def __init__(self, databaseName, collectionName, connectionString=CONNECTION_STRING):
        self.connectionString = connectionString
        self.client = AsyncIOMotorClient(connectionString)
        self.databaseName = databaseName
        self.db = self.client[self.databaseName]
        self.collection = self.db[collectionName]
    
    def get_db(self):
        return self.db
    
    def get_collection(self):
        return self.collection
        
    