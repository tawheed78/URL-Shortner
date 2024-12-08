from fastapi import HTTPException, status
from datetime import datetime, timedelta
import os
from ..utils.utils import generate_unique_short_code, get_browser_and_device
from ..configs.db_config import db_instance
from pymongo.errors import PyMongoError
from ..services.qr_service import generate_qr_code
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

collection = db_instance.get_collection()


async def custom_alias_exists(customAlias):

    try:
        res = await collection.find_one({"_id": customAlias})
        return res is not None
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def process_short_url_click(code, user_agent):
    try:
        res = await collection.find_one({"_id": code})
        if res:
            browser, device = get_browser_and_device(user_agent)

            document = {"_id": code}
            update_query = {
            "$inc": {
                "clicks": 1,
                f"analytics.device_clicks.{device}": 1,
                f"analytics.browser_clicks.{browser}": 1,
            },
            "$set": {"analytics.lastAccessed": datetime.now()}
        }
            await collection.update_one(document, update_query)
            return res['longUrl']
        else:
            return False
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def shorten_URL(longUrl, customAlias):
    if customAlias:
        if await custom_alias_exists(customAlias):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Custom alias '{customAlias}' is already in use."
            )
    shortCode = customAlias if customAlias else generate_unique_short_code(1,3)
    shortUrl = f"{BASE_URL}/{shortCode}"
    created = datetime.now()
    utc_time = created - timedelta(hours=5, minutes=30)
    qrCode = generate_qr_code(shortUrl)
    try:
        collection.insert_one({
            "_id": shortCode,
            "shortUrl": shortUrl,
            "longUrl": str(longUrl),
            "clicks": 0,
            "lastAccessed": None,
            "qrCode": qrCode,
            "created": utc_time
        })
        return {"shortUrl":shortUrl, "qrCode":qrCode, "created":created}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error creating URL: {str(e)}")

   
async def fetch_all_urls():
    try:
        cursor = collection.find({})
        urls = await cursor.to_list(length=None)
        return urls
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all the URLs: {str(e)}")
    
async def fetch_URL_details(code):
    try:
        url = await collection.find_one({"_id": code})
        return url
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching URL details: {str(e)}")
    
async def remove_url(code):
    try:
        result = await collection.delete_one({"_id": code})
        if result.deleted_count == 1:
            return True
        else:
            return False
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching URL details: {str(e)}")