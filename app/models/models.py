from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class URLCreation(BaseModel):
    longUrl : str
    customAlias : Optional[str] = None

class URLResponse(BaseModel):
    shortUrl : str
    qrCode : str
    created : datetime

class URLDetails(BaseModel):
    longUrl: str
    shortUrl: str
    created: datetime
    clicks: int

class URLStatistics(BaseModel):
    longUrl: str
    shortUrl: str
    clicks: int
    created: datetime
    lastAccessed: Optional[datetime]