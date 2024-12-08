import re
from pydantic import BaseModel, HttpUrl, ValidationInfo, ValidationError, field_validator
from typing import Dict, List, Optional
from datetime import datetime

class URLCreation(BaseModel):
    longUrl : HttpUrl
    customAlias : Optional[str] = None

    @field_validator("customAlias") 
    def validate_custom_alias(cls, v: str, info: ValidationInfo) -> str:
        if v and not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("CustomAlias must only include alphabets, numbers and hyphen.")
        return v
class BulkURLCreation(BaseModel):
    urls: List[URLCreation] 

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