from typing import List

from fastapi.responses import JSONResponse
from ..configs.db_config import MongoDbDatabase
from ..models.models import URLCreation, URLDetails, URLResponse, URLStatistics
from ..services.urls_service import create_short_url, list_urls, get_url_details, remove_url
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

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
    
@router.get('/', response_model=List[URLDetails])
async def fetch_urls():
    try:
        urls = await list_urls()
        return urls
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    
@router.get('/{code}', response_model= URLDetails)
async def get_url(code):
    try:
        url = await get_url_details(code)
        if not url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= "URL not found."                    
            )
        return URLDetails(**url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    
@router.delete('/{code}')
async def delete_url(code):
    try:
        result = await remove_url(code)
        if result:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'message': f"URL with code: {code} deleted successfully"}
                )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= "No such URL exists."                    
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )