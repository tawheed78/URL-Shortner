from fastapi import APIRouter, HTTPException, Request, status
from ..models.models import URLStatistics, QRCode
from ..configs.db_config import db_instance
from ..services.analytics_service import url_stats, get_qr_code
from ..services.rate_limiting_service import rate_limit

router = APIRouter()

collection = db_instance.get_collection()

@router.get('/{code}/stats', response_model=URLStatistics)
@rate_limit(limit=25, time_window=60)
async def get_URL_statistics(request:Request, code:str):
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
@rate_limit(limit=5, time_window=60)
async def get_QR_code(request: Request, code:str):
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