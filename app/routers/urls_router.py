from datetime import datetime
import json
from typing import List, Union
from fastapi.responses import JSONResponse, RedirectResponse
import redis
from ..models.models import URLCreation, URLDetails, URLResponse, BulkURLCreation
from ..services.urls_service import shorten_URL, fetch_all_urls, fetch_URL_details, remove_url, process_short_url_click
from ..services.rate_limiting_service import rate_limit
from ..configs.redis_config import get_redis_client
from fastapi import APIRouter, Depends, HTTPException, Request, status
import redis.asyncio as aioredis


router = APIRouter()
redirect_router = APIRouter()

@router.post('/', response_model=Union[URLResponse, List[URLResponse]])
@rate_limit(limit=10, time_window=60)
async def create_short_URL(payload: Union[URLCreation, BulkURLCreation]):
    try:
        if isinstance(payload, URLCreation):
            result = await shorten_URL(payload.longUrl, payload.customAlias)
            return URLResponse(shortUrl=result['shortUrl'], qrCode=result['qrCode'], created=result['created'])
        elif isinstance(payload, BulkURLCreation):
            urls_list = []
            for url_data in payload.urls:
                result = await shorten_URL(url_data.longUrl, url_data.customAlias)
                urls_list.append(URLResponse(shortUrl=result['shortUrl'], qrCode=result['qrCode'], created=result['created']))
            return urls_list
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

    
@redirect_router.get('/{code}')
async def redirect_shortURL(code, request: Request):
    if not code:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The long URL is required."
            )
    try:
        user_agent = request.headers.get('User-Agent')
        response = await process_short_url_click(code, user_agent)
        if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= "No such URL exists."                    
            )
        else:
            return RedirectResponse(url=response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

 
@router.get('/', response_model=List[URLDetails])
@rate_limit(limit=20, time_window=60) 
async def list_URLs(request: Request, redis: aioredis.Redis = Depends(get_redis_client)):
    try:
        cached_urls_list = await redis.get('shortURLs')
        if cached_urls_list:
            return [URLDetails(**url) for url in json.loads(cached_urls_list)]
        urls = await fetch_all_urls()
        urls_data = []
        for url in urls:
            url['created'] = str(url['created'])
            urls_data.append(url)
        await redis.set('shortURLs',json.dumps(urls_data),ex=3600)
        return urls
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get('/{code}', response_model= URLDetails)
@rate_limit(limit=20, time_window=60)
async def get_URL_details(request: Request, code:str, redis: aioredis.Redis = Depends(get_redis_client)):
    try:
        cached_url = await redis.get(code)
        if cached_url:
            cached_url = json.loads(cached_url)

            if 'created' in cached_url:
                cached_url["created"] = datetime.fromisoformat(cached_url["created"])
            return URLDetails(**cached_url)

        url = await fetch_URL_details(code)
        if not url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= "URL not found."                    
            )
        response = URLDetails(**url)
        url_data = response.model_dump()

        if isinstance(url_data['created'], datetime):
            url_data['created'] = url_data['created'].isoformat()

        await redis.set(code, json.dumps(url_data), ex=3600)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

   
@router.delete('/{code}')
@rate_limit(limit=30, time_window=60) 
async def delete_URL(code):
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