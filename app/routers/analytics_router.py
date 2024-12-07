from fastapi import APIRouter, HTTPException, status
from ..models.models import URLStatistics, QRCode
from ..configs.db_config import db_instance
from ..services.analytics_service import url_stats, get_qr_code

router = APIRouter()

collection = db_instance.get_collection()

@router.get('/{code}/stats', response_model=URLStatistics)
async def get_url_stats(code):
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide the Short code"
        )
    try:
        response = await url_stats(code)
        return URLStatistics(**response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    
@router.get('/{code}/qr', response_model=QRCode)
async def get_qr(code):
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide the Short code"
        )
    try:
        response = await get_qr_code(code)
        return QRCode(**response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )