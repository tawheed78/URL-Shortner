from typing import List, Union
from fastapi.responses import JSONResponse, RedirectResponse
from ..models.models import URLCreation, URLDetails, URLResponse, BulkURLCreation
from ..services.urls_service import shorten_URL, fetch_all_urls, fetch_URL_details, remove_url, process_short_url_click
from fastapi import APIRouter, HTTPException, Request, status


router = APIRouter()
redirect_router = APIRouter()

@router.post('/', response_model=Union[URLResponse, List[URLResponse]])
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
async def list_URLs():
    try:
        urls = await fetch_all_urls()
        return urls
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    
@router.get('/{code}', response_model= URLDetails)
async def get_URL_details(code):
    try:
        url = await fetch_URL_details(code)
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