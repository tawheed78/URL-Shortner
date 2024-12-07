from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class URLCreation(BaseModel):
    longUrl : str
    customAlias : Optional[str] = None

class URLResponse(BaseModel):
    shortUrl : str
    qrCode : str
    created : datetime

class URLDetails(BaseModel):
    shortUrl: str
    longUrl: str
    qrCode: str
    created: datetime
    
class URLAnalytics(BaseModel):
    device_clicks: Dict[str, int]
    browser_clicks: Dict[str, int]
    lastAccessed: Optional[datetime]

class URLStatistics(BaseModel):
    longUrl: str
    shortUrl: str
    clicks: int
    created: datetime
    analytics: URLAnalytics

class QRCode(BaseModel):
    shortUrl:str
    longUrl:str
    qrCode:str