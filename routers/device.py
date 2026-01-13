from fastapi import APIRouter, Depends, HTTPException, Query, status
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
    device_id: Optional[str] = Query(None, description="Filter by device ID"),
    id_provinsi: Optional[int] = Query(None, description="Filter by provinsi/province ID"),
    id_kabupaten: Optional[int] = Query(None, description="Filter by kabupaten/regency/city ID"),
    id_kecamatan: Optional[int] = Query(None, description="Filter by kecamatan/district ID"),
    id_kelurahan: Optional[int] = Query(None, description="Filter by kelurahan/village ID"),
    id_perusahaan: Optional[int] = Query(None, description="Filter by company ID"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get device(s) with optional filtering by location hierarchy or company
    
    Parameters:
    - device_id: Filter by specific device ID
    - id_provinsi: Filter by province
    - id_kabupaten: Filter by regency/city (kabupaten/kota)
    - id_kecamatan: Filter by district (kecamatan)
    - id_kelurahan: Filter by village (kelurahan/desa)
    - id_perusahaan: Filter by company
    
    Filter Priority (highest to lowest specificity):
    device_id > id_kelurahan > id_kecamatan > id_kabupaten > id_provinsi > id_perusahaan > all devices
    """
    # Priority 1: Get specific device by ID
    if device_id is not None:
        device = database.get_device_by_device_id(device_id)
        if device is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device with id {device_id} not found"
            )
        return [device]
    
    # Priority 2: Filter by kelurahan (village - highest location specificity)
    if id_kelurahan is not None:
        return database.get_devices_by_kelurahan(id_kelurahan)
    
    # Priority 3: Filter by kecamatan (district)
    if id_kecamatan is not None:
        return database.get_devices_by_kecamatan(id_kecamatan)
    
    # Priority 4: Filter by kabupaten (regency/city)
    if id_kabupaten is not None:
        return database.get_devices_by_kabupaten(id_kabupaten)
    
    # Priority 5: Filter by provinsi (province)
    if id_provinsi is not None:
        return database.get_devices_by_provinsi(id_provinsi)
    
    # Priority 6: Filter by company
    if id_perusahaan is not None:
        return database.get_devices_by_perusahaan(id_perusahaan)
    
    # Otherwise return all devices
    return database.get_all_devices()
