from typing import Optional
from pydantic import BaseModel


class SiteResponse(BaseModel):
    """Schema for master_site response"""
    id: int
    id_perusahaan: int
    nama_site: str
    id_provinsi: int
    id_kabupaten: int
    id_kecamatan: int
    id_kelurahan: int
    latitude: float
    longitude: float
    keterangan: Optional[str] = None
    created_at: str


class KecamatanResponse(BaseModel):
    """Schema for district/kecamatan response"""
    id: int
    id_kecamatan: int
    id_kabupaten: int
    nama_kecamatan: str


class KelurahanResponse(BaseModel):
    """Schema for village/kelurahan response"""
    id: int
    id_kelurahan: int
    id_kecamatan: int
    nama_kelurahan: str


class KabupatenResponse(BaseModel):
    """Schema for regency/kabupaten response"""
    id: int
    id_kabupaten: int
    id_provinsi: int
    nama_kabupaten: str


class ProvinsiResponse(BaseModel):
    """Schema for province/provinsi response"""
    id: int
    id_provinsi: int
    nama_provinsi: str
