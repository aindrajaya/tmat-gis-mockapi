from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class DeviceResponse(BaseModel):
    """Device response schema"""
    id: int
    device_id_unik: str
    id_perusahaan: int
    id_site: int
    tipe_alat: str
    alamat: Optional[str] = None
    provinsi: str
    kabupaten: str
    kota: str
    latitude: float
    longitude: float
    status: str
    last_online: str  # Stored as string from JSON
    created_at: str  # Stored as string from JSON
    kode_titik: str
    kode_blok: str
    
    class Config:
        from_attributes = True
