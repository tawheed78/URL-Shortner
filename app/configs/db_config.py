import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')

class MongoDbDatabase:
    def __init__(self, databaseName, collectionName, connectionString=CONNECTION_STRING):
        self.connectionString = connectionString
        self.client = AsyncIOMotorClient(connectionString)
        self.databaseName = databaseName
        self.db = self.client[self.databaseName]
        self.collection = self.db[collectionName]
        # self.create_index = self.create_ttl_index()
    def get_db(self):
        return self.db
    
    def get_collection(self):
        return self.collection
    
    # def create_ttl_index(self):
    #     try:
    #         self.collection.create_index(
    #             [("expireAfter", 1)],
    #             expireAfterSeconds=1
    #         )
            
    #         print("TTL index created successfully.")
    #     except Exception as e:
    #         print(f"Error creating TTL index: {e}")
    
db_instance = MongoDbDatabase(databaseName="url_shortner_database", collectionName="url_collection")

    