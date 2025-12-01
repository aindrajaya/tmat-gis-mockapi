from fastapi import Header, HTTPException, status
from typing import Optional

async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Verify API key from X-API-KEY header
    For demo: allows any non-empty key
    """
    if not x_api_key or x_api_key.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-KEY header is missing or empty"
        )
    
    return x_api_key
