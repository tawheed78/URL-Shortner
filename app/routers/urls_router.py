from ..configs.db_config import MongoDbDatabase
from ..models.models import URLCreation, URLDetails, URLResponse, URLStatistics
from ..services.urls_service import create_short_url
from ..services.qr_service import generateQRCode
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

db = MongoDbDatabase(databaseName="url_shortner_service_database", collectionName="urls_collection")

@router.post('/shorten', response_model=URLResponse)
async def shorten_url(payload: URLCreation):
    if not payload.longUrl:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The long URL is required."
        )
    try:
        result = await create_short_url(payload.longUrl, payload.customAlias)
        return URLResponse(shortUrl=result['shortUrl'], qrCode=result['qrCode'], created=result['created'])
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
