"""
Service layer for handling analytics operations related to URLs.
Provides methods for fetching URL stats and QR codes.
"""

from fastapi import HTTPException
from pymongo.errors import PyMongoError
from ..configs.db_config import db_instance

collection = db_instance.get_collection()

async def url_stats(code):
    """
    Fetches statistics related to a shortened URL from the database.
    
    Parameters:
    - code (str): The unique identifier (short code) for the URL.
    
    Returns:
    - dict: The URL statistics if found, or None if not.
    """
    try:
        result = await collection.find_one({"_id": code})
        return result
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching URL Stats: {str(e)}") from e

async def get_qr_code(code):
    """
    Retrieves the QR code associated with a shortened URL from the database.
    
    Parameters:
    - code (str): The unique identifier (short code) for the URL.
    
    Returns:
    - dict: The QR code data if found, or None if not.
    """
    try:
        result = await collection.find_one({"_id": code})
        return result
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching QR code: {str(e)}") from e
