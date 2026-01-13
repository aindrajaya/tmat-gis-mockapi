from typing import List, Optional
from fastapi import APIRouter, Depends, Query

from auth.api_key import verify_api_key
from schemas.site import (
    SiteResponse,
    KecamatanResponse,
    KelurahanResponse,
    KabupatenResponse,
    ProvinsiResponse,
)
from services.database import (
    get_all_sites,
    get_sites_by_kecamatan,
    get_sites_by_kelurahan,
    get_all_kecamatan,
    get_all_kelurahan,
    get_all_kabupaten,
    get_all_provinsi,
    get_kecamatan_by_kabupaten,
    get_kelurahan_by_kecamatan,
)

router = APIRouter(prefix="/site", tags=["site"])


@router.get("", response_model=List[SiteResponse])
async def get_site(
    id_kecamatan: Optional[int] = Query(None, description="Filter by kecamatan/district ID"),
    id_kelurahan: Optional[int] = Query(None, description="Filter by kelurahan/village ID"),
    id_perusahaan: Optional[int] = Query(None, description="Filter by company ID"),
    api_key: str = Depends(verify_api_key),
):
    """
    Get sites with optional filtering by location or company.
    
    Parameters:
    - id_kecamatan: Filter sites by kecamatan/district ID
    - id_kelurahan: Filter sites by kelurahan/village ID
    - id_perusahaan: Filter sites by company ID
    """
    sites = get_all_sites()
    
    # Apply filters
    if id_kecamatan:
        sites = get_sites_by_kecamatan(id_kecamatan)
    elif id_kelurahan:
        sites = get_sites_by_kelurahan(id_kelurahan)
    
    # Additional filter by company
    if id_perusahaan:
        sites = [s for s in sites if s["id_perusahaan"] == id_perusahaan]
    
    return sites


@router.get("/kecamatan", response_model=List[KecamatanResponse])
async def get_kecamatan(
    id_kabupaten: Optional[int] = Query(None, description="Filter by kabupaten/regency ID"),
    api_key: str = Depends(verify_api_key),
):
    """
    Get all kecamatan (districts) or filter by kabupaten.
    
    Parameters:
    - id_kabupaten: Filter kecamatan by parent kabupaten/regency ID
    """
    if id_kabupaten:
        return get_kecamatan_by_kabupaten(id_kabupaten)
    return get_all_kecamatan()


@router.get("/kelurahan", response_model=List[KelurahanResponse])
async def get_kelurahan(
    id_kecamatan: Optional[int] = Query(None, description="Filter by kecamatan/district ID"),
    api_key: str = Depends(verify_api_key),
):
    """
    Get all kelurahan (villages) or filter by kecamatan.
    
    Parameters:
    - id_kecamatan: Filter kelurahan by parent kecamatan/district ID
    """
    if id_kecamatan:
        return get_kelurahan_by_kecamatan(id_kecamatan)
    return get_all_kelurahan()


@router.get("/kabupaten", response_model=List[KabupatenResponse])
async def get_kabupaten(
    id_provinsi: Optional[int] = Query(None, description="Filter by provinsi/province ID"),
    api_key: str = Depends(verify_api_key),
):
    """
    Get all kabupaten (regencies) or filter by provinsi.
    
    Parameters:
    - id_provinsi: Filter kabupaten by parent provinsi/province ID
    """
    if id_provinsi:
        kabupaten = get_all_kabupaten()
        return [k for k in kabupaten if k["id_provinsi"] == id_provinsi]
    return get_all_kabupaten()


@router.get("/provinsi", response_model=List[ProvinsiResponse])
async def get_provinsi(
    api_key: str = Depends(verify_api_key),
):
    """Get all provinces (provinsi)"""
    return get_all_provinsi()
