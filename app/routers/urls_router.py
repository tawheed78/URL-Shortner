from ..configs.db_config import db
from ..models.models import URLCreation, URLDetails, URLResponse, URLStatistics
from fastapi import APIRouter, Request,HTTPException
from pymongo.errors import PyMongoError
from pydantic import ValidationError
from ..utils.utils import generate_unique_short_code
from datetime import datetime
router = APIRouter()
collection = db['urls_database']

@router.post('/shorten', response_model=URLResponse)
async def shorten_url(payload: URLCreation):
    shortCode = payload.customAlias if payload.customAlias else generate_unique_short_code(1,3)
    longUrl = payload.longUrl
    shortUrl = f"mylink.ly/{shortCode}"
    created = datetime.now()
    document = {
        "shortUrl": shortUrl,
        "longUrl": longUrl,
        "created": created
    }
    result = await collection.insert_one({shortCode:document})

    return URLResponse(shortUrl=shortUrl, qrCode="example", created=created)
