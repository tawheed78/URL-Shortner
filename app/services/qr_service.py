"""
Service for generating QR codes for URLs.
"""

import base64
from io import BytesIO
import qrcode

def generate_qr_code(short_url: str) -> str:
    """
    Generates a QR code for the given URL.
    
    Parameters:
    - short_url (str): The shortened URL to generate a QR code for.
    
    Returns:
    - str: A base64-encoded string representing the QR code image.
    """
    code = qrcode.QRCode(
        version=1, 
        box_size=10,
        border=4
    )
    code.add_data(short_url)
    code.make(fit=True)
    img = code.make_image(fill_color='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")    
    qr_code = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
    return qr_code
