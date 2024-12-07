import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')

client = AsyncIOMotorClient(CONNECTION_STRING)
db = client["url_shortner_service_database"]
try:
    client.admin.command("ping")
    print('ping')
except Exception as e:
    print(e)



    