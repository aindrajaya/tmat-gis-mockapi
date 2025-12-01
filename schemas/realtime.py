from typing import Optional
from pydantic import BaseModel

class RealtimeDataResponse(BaseModel):
    """Realtime sensor data response schema"""
    id: int
    device_id_unik: str
    timestamp_data: str  # Stored as string from JSON
    tmat_value: float
    suhu_value: float
    ph_value: float
    api_key_used: Optional[str] = None
    
    class Config:
        from_attributes = True

class RealtimeDeviceResponse(BaseModel):
    """Paginated realtime device data response"""
    data: list[RealtimeDataResponse]
    total: int
    offset: int
    limit: int
    
    class Config:
        from_attributes = True
