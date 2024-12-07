from fastapi import HTTPException, status
from datetime import datetime
from ..utils.utils import generate_unique_short_code
from ..configs.db_config import MongoDbDatabase
from pymongo.errors import PyMongoError
from ..services.qr_service import generateQRCode

_instance = MongoDbDatabase(databaseName="url_shortner_database", collectionName="url_collection")
collection = _instance.get_collection()

async def custom_alias_exists(customAlias):
    try:
        res = await collection.find_one({"_id": customAlias})
        return res is not None
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def create_short_url(longUrl, customAlias):
    if customAlias:
        if await custom_alias_exists(customAlias):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Custom alias '{customAlias}' is already in use."
            )
    shortCode = customAlias if customAlias else generate_unique_short_code(1,3)
    shortUrl = f"mylink.ly/{shortCode}"
    created = datetime.now()
    qrCode = generateQRCode(shortUrl)
    try:
        collection.insert_one({
            "_id": shortCode,
            "shortUrl": shortUrl,
            "longUrl": longUrl,
            "clicks": 0,
            "lastAccessed": None,
            "qrCode": qrCode,
            "created": created
        })
        return {"shortUrl":shortUrl, "qrCode":qrCode, "created":created}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error creating URL: {str(e)}")