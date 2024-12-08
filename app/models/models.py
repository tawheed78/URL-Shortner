import re
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, AnyHttpUrl, field_validator, ValidationInfo

"""
This module contains Pydantic models used for URL shortening,
including models for URL creation, response, details, statistics, 
analytics, and QR code generation.
"""

class URLCreation(BaseModel):
    """
    Model for creating a URL.

    Attributes:
        longUrl: The original URL to be shortened.
        customAlias: An optional custom alias for the shortened URL.
    """
    longUrl: AnyHttpUrl
    customAlias: Optional[str] = None

    @field_validator("customAlias") 
    def validate_custom_alias(cls, v: str) -> str:
        """
        Validates the custom alias to ensure it only contains
        alphanumeric characters, hyphens, or underscores.

        Args:
            v: The custom alias.

        Returns:
            str: The validated custom alias.

        Raises:
            ValueError: If the alias contains invalid characters.
        """
        if v and not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("CustomAlias must only include alphabets, numbers and hyphen.")
        return v
    
class BulkURLCreation(BaseModel):
    """
    Model for bulk creation of URLs.

    Attributes:
        urls: A list of URLCreation models.
    """
    urls: List[URLCreation] 

class URLResponse(BaseModel):
    """
    Model for the response when a URL is shortened.

    Attributes:
        shortUrl: The shortened URL.
        qrCode: The QR code for the shortened URL.
        created: The creation timestamp of the shortened URL.
    """
    shortUrl: str
    qrCode: str
    created: datetime

class URLDetails(BaseModel):
    """
    Model for details of a shortened URL.

    Attributes:
        shortUrl: The shortened URL.
        longUrl: The original long URL.
        qrCode: The QR code for the shortened URL.
        created: The creation timestamp of the shortened URL.
    """
    shortUrl: str
    longUrl: str
    qrCode: str
    created: datetime
    
class URLAnalytics(BaseModel):
    """
    Model for URL analytics.

    Attributes:
        device_clicks: A dictionary of device-based click counts.
        browser_clicks: A dictionary of browser-based click counts.
        lastAccessed: The last time the URL was accessed.
    """
    device_clicks: Dict[str, int]
    browser_clicks: Dict[str, int]
    lastAccessed: Optional[datetime]

class URLStatistics(BaseModel):
    """
    Model for URL statistics.

    Attributes:
        longUrl: The long URL.
        shortUrl: The shortened URL.
        clicks: The number of clicks.
        created: The creation timestamp.
        analytics: The analytics related to the URL.
    """
    longUrl: str
    shortUrl: str
    clicks: int
    created: datetime
    analytics: URLAnalytics

class QRCode(BaseModel):
    """
    Model for a QR code associated with a shortened URL.

    Attributes:
        shortUrl: The shortened URL.
        longUrl: The original long URL.
        qrCode: The QR code image data.
    """
    shortUrl: str
    longUrl: str
    qrCode: str
