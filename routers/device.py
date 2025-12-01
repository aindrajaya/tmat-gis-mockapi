from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from schemas.device import DeviceResponse
from services import database
from auth.api_key import verify_api_key

router = APIRouter(
    prefix="/device",
    tags=["Device"]
)

@router.get("", response_model=List[DeviceResponse])
async def get_device(
    device_id: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Get device(s)
    - If device_id is provided, return specific device
    - Otherwise, return all devices
    """
    if device_id is not None:
        device = database.get_device_by_device_id(device_id)
        if device is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device with id {device_id} not found"
            )
        return [device]
    
    return database.get_all_devices()
