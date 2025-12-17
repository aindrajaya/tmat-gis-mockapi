from typing import List
from pydantic import BaseModel
from .device import DeviceResponse

class PerusahaanResponse(BaseModel):
    """Company response schema"""
    id: int
    nama_perusahaan: str
    pic_kontak: str
    email_kontak: str
    telepon: str
    alamat: str
    status: str
    created_at: str  # Stored as string from JSON
    kode_perusahaan: str
    jenis_perusahaan: str
    
    class Config:
        from_attributes = True

class PerusahaanWithDevicesResponse(BaseModel):
    """Company with attached device list"""
    perusahaan: PerusahaanResponse
    devices: List[DeviceResponse]
    
    class Config:
        from_attributes = True
