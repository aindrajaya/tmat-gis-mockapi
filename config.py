import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application configuration settings"""
    API_KEY_DEMO: str = os.getenv("API_KEY_DEMO", "demo-key-123")
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    API_PREFIX: str = "/api/portal_v1"
    
    # CORS settings for frontend access
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://27.50.21.155:9001"
    ]

settings = Settings()
