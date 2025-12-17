from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from schemas.perusahaan import PerusahaanResponse, PerusahaanWithDevicesResponse
from services import database
from auth.api_key import verify_api_key

router = APIRouter(
    prefix="/perusahaan",
    tags=["Perusahaan"]
)

@router.get("", response_model=List[PerusahaanResponse])
async def get_perusahaan(
    id: Optional[int] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Get company/companies
    - If id is provided, return single company
    - Otherwise, return all companies
    """
    if id is not None:
        perusahaan = database.get_perusahaan_by_id(id)
        if perusahaan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Perusahaan with id {id} not found"
            )
        return [perusahaan]
    
    return database.get_all_perusahaan()

@router.get("/devices", response_model=List[PerusahaanWithDevicesResponse])
async def get_perusahaan_devices(
    id: Optional[int] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Get perusahaan with their devices
    - If id is provided, return that company and its devices
    - Otherwise, return all companies with their devices
    """
    if id is not None:
        perusahaan_with_devices = database.get_perusahaan_with_devices(id)
        if perusahaan_with_devices is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Perusahaan with id {id} not found"
            )
        return [perusahaan_with_devices]
    
    return database.get_all_perusahaan_with_devices()
