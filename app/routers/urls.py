from configs.db_config import db
from models.models import URLCreation, URLDetails, URLResponse, URLStatistics
from fastapi import APIRouter, Request,HTTPException
from pymongo.errors import PyMongoError
from pydantic import ValidationError

router = APIRouter()
collection = db['urls_database']

@router.post('/', response_model=URLResponse)
def shorten_url(payload: URLCreation):
    shortcode 