from datetime import datetime
from pydantic import BaseModel

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
