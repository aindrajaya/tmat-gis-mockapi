from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import datetime
from typing import Optional, List
from schemas.realtime import RealtimeDataResponse, RealtimeDeviceResponse
from services import database
from auth.api_key import verify_api_key

router = APIRouter(
    prefix="",
    tags=["Realtime Data"]
)

@router.get("/realtime_all", response_model=List[RealtimeDataResponse])
async def get_realtime_all(
    id_perusahaan: Optional[int] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Get realtime data summary
    - If id_perusahaan provided, filter by company
    - Otherwise return all realtime data
    """
    if id_perusahaan is not None:
        return database.get_realtime_by_perusahaan(id_perusahaan)
    
    return database.get_all_realtime()

@router.get("/realtime_device", response_model=RealtimeDeviceResponse)
async def get_realtime_device(
    device_id: str = Query(..., description="Unique device identifier"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    limit: int = Query(100, ge=1, le=1000, description="Results per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get realtime device data within date range
    - Filters by device_id and date range (full day)
    - Supports pagination with offset and limit
    - Returns paginated data with metadata
    """
    # Validate device exists
    device = database.get_device_by_device_id(device_id)
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with id {device_id} not found"
        )
    
    # Parse dates
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Dates must be in YYYY-MM-DD format"
        )
    
    if start_dt > end_dt:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="start_date must be before or equal to end_date"
        )
    
    # Get paginated data
    data, total = database.get_realtime_by_device(
        device_id=device_id,
        start_date=start_dt,
        end_date=end_dt,
        offset=offset,
        limit=limit
    )
    
    return RealtimeDeviceResponse(
        data=data,
        total=total,
        offset=offset,
        limit=limit
    )
