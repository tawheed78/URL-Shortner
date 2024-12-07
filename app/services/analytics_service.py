from fastapi import HTTPException
from ..configs.db_config import db_instance
from pymongo.errors import PyMongoError

collection = db_instance.get_collection()

async def url_stats(code):
    try:
        result = collection.find_one({"_id": code})
        return result
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching URL Stats: {str(e)}")
    
async def get_qr_code(code):
    try:
        result = collection.find_one({"_id": code})
        return result
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching QR code: {str(e)}")