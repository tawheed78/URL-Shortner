import os
from motor.motor_asyncio import AsyncIOMotorClient

CONNECTION_STRING = "mongodb://localhost:27017/"
client = AsyncIOMotorClient(CONNECTION_STRING)
db = client["url_shortner_service_database"]