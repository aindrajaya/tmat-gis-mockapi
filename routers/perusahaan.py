from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from schemas.perusahaan import PerusahaanResponse
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
