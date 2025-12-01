#!/usr/bin/env python
"""Simple API test script"""
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"
HEADERS = {"X-API-KEY": "demo-key-123"}

def test_root():
    """Test root endpoint"""
    print("\n📌 Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/", headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_health():
    """Test health check"""
    print("\n📌 Testing health check...")
    response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_all_perusahaan():
    """Test get all companies"""
    print("\n📌 Testing GET /api/portal_v1/perusahaan...")
    response = requests.get(f"{BASE_URL}/api/portal_v1/perusahaan", headers=HEADERS)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total companies: {len(data)}")
    if data:
        print(f"First company: {json.dumps(data[0], indent=2)}")

def test_get_perusahaan_by_id():
    """Test get company by ID"""
    print("\n📌 Testing GET /api/portal_v1/perusahaan?id=19...")
    response = requests.get(f"{BASE_URL}/api/portal_v1/perusahaan?id=19", headers=HEADERS)
    print(f"Status: {response.status_code}")
    data = response.json()
    if data:
        print(f"Company: {json.dumps(data[0], indent=2)}")

def test_get_all_devices():
    """Test get all devices"""
    print("\n📌 Testing GET /api/portal_v1/device...")
    response = requests.get(f"{BASE_URL}/api/portal_v1/device", headers=HEADERS)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total devices: {len(data)}")
    if data:
        print(f"First device: {json.dumps(data[0], indent=2)}")

def test_get_device_by_id():
    """Test get device by ID"""
    print("\n📌 Testing GET /api/portal_v1/device?device_id=DEV-TI-001...")
    response = requests.get(f"{BASE_URL}/api/portal_v1/device?device_id=DEV-TI-001", headers=HEADERS)
    print(f"Status: {response.status_code}")
    data = response.json()
    if data:
        print(f"Device: {json.dumps(data[0], indent=2)}")

def test_realtime_all():
    """Test get realtime all"""
    print("\n📌 Testing GET /api/portal_v1/realtime_all...")
    response = requests.get(f"{BASE_URL}/api/portal_v1/realtime_all", headers=HEADERS)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total realtime records: {len(data)}")
    if data:
        print(f"First record: {json.dumps(data[0], indent=2)}")

def test_realtime_device():
    """Test get realtime by device with pagination"""
    print("\n📌 Testing GET /api/portal_v1/realtime_device...")
    response = requests.get(
        f"{BASE_URL}/api/portal_v1/realtime_device",
        headers=HEADERS,
        params={
            "device_id": "DEV-TI-001",
            "start_date": "2025-11-01",
            "end_date": "2025-11-30",
            "limit": 10,
            "offset": 0
        }
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")

def test_no_api_key():
    """Test missing API key"""
    print("\n📌 Testing request without API key...")
    response = requests.get(f"{BASE_URL}/api/portal_v1/perusahaan")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("=" * 60)
    print("API Testing - TMAT Monitoring Portal")
    print("=" * 60)
    
    try:
        test_root()
        test_health()
        test_get_all_perusahaan()
        test_get_perusahaan_by_id()
        test_get_all_devices()
        test_get_device_by_id()
        test_realtime_all()
        test_realtime_device()
        test_no_api_key()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
