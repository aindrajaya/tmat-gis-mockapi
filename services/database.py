import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Module-level database cache
_db_cache: Dict[str, Any] = None

def load_database() -> Dict[str, Any]:
    """Load populate_db.json into memory on startup"""
    global _db_cache
    
    if _db_cache is not None:
        return _db_cache
    
    db_path = Path(__file__).parent.parent / "populate_db.json"
    
    with open(db_path, 'r') as f:
        _db_cache = json.load(f)
    
    return _db_cache

def get_database() -> Dict[str, Any]:
    """Get the cached database"""
    global _db_cache
    if _db_cache is None:
        load_database()
    return _db_cache

# Perusahaan queries
def get_all_perusahaan() -> List[Dict]:
    """Get all companies"""
    db = get_database()
    return db.get("master_perusahaan", [])

def get_perusahaan_by_id(id: int) -> Optional[Dict]:
    """Get company by ID"""
    perusahaan = get_all_perusahaan()
    for item in perusahaan:
        if item["id"] == id:
            return item
    return None

# Device queries
def get_all_devices() -> List[Dict]:
    """Get all devices"""
    db = get_database()
    return db.get("master_device", [])

def get_device_by_device_id(device_id: str) -> Optional[Dict]:
    """Get device by unique device_id"""
    devices = get_all_devices()
    for device in devices:
        if device["device_id_unik"] == device_id:
            return device
    return None

def get_devices_by_perusahaan(id_perusahaan: int) -> List[Dict]:
    """Get all devices for a company"""
    devices = get_all_devices()
    return [d for d in devices if d["id_perusahaan"] == id_perusahaan]

def get_perusahaan_with_devices(id_perusahaan: int) -> Optional[Dict]:
    """Get company detail with its devices"""
    perusahaan = get_perusahaan_by_id(id_perusahaan)
    if perusahaan is None:
        return None
    
    devices = get_devices_by_perusahaan(id_perusahaan)
    return {
        "perusahaan": perusahaan,
        "devices": devices
    }

def get_all_perusahaan_with_devices() -> List[Dict]:
    """Get all companies with their devices"""
    return [
        {
            "perusahaan": perusahaan,
            "devices": get_devices_by_perusahaan(perusahaan["id"])
        }
        for perusahaan in get_all_perusahaan()
    ]

# Realtime data queries
def get_all_realtime() -> List[Dict]:
    """Get all realtime measurements"""
    db = get_database()
    return db.get("data_realtime", [])

def get_realtime_by_perusahaan(id_perusahaan: int) -> List[Dict]:
    """Get realtime data summary for company"""
    realtime = get_all_realtime()
    devices = get_devices_by_perusahaan(id_perusahaan)
    device_ids = {d["device_id_unik"] for d in devices}
    
    return [r for r in realtime if r["device_id_unik"] in device_ids]

def get_realtime_by_device(
    device_id: str,
    start_date: datetime,
    end_date: datetime,
    offset: int = 0,
    limit: int = 100
) -> tuple[List[Dict], int]:
    """
    Get realtime data for device within date range with pagination
    Returns: (data, total_count)
    """
    realtime = get_all_realtime()
    
    # Convert dates to datetime objects for comparison (full day range)
    start_dt = datetime.combine(start_date.date(), datetime.min.time())
    end_dt = datetime.combine(end_date.date(), datetime.max.time())
    
    # Filter by device and date range
    filtered = []
    for entry in realtime:
        if entry["device_id_unik"] == device_id:
            try:
                entry_time = datetime.fromisoformat(entry["timestamp_data"])
                if start_dt <= entry_time <= end_dt:
                    filtered.append(entry)
            except (ValueError, KeyError):
                continue
    
    total_count = len(filtered)
    paginated = filtered[offset:offset + limit]
    
    return paginated, total_count
