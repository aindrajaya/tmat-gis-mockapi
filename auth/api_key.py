from fastapi import Header, HTTPException, Query, status
from typing import Optional

async def verify_api_key(
    x_api_key: Optional[str] = Header(None),
    api_key: Optional[str] = Query(None)
) -> str:
    """
    Verify API key from either:
    1. X-API-KEY header (recommended for secure requests)
    2. api_key query parameter (for testing/simple requests)
    
    For demo: allows any non-empty key
    """
    # Priority: Header > Query Parameter
    key = x_api_key or api_key
    
    if not key or key.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing. Provide via X-API-KEY header or api_key query parameter"
        )
    
    return key
