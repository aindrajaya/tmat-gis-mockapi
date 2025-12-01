from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from services import database
from routers import perusahaan, device, realtime

# Startup event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    database.load_database()
    print("✓ Database loaded into memory")
    yield
    # Shutdown
    print("✓ Application shutdown")

# Initialize FastAPI app
app = FastAPI(
    title="API Monitoring TMAT - Portal V1",
    description="Mock backend API for plantation monitoring system",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(perusahaan.router, prefix=settings.API_PREFIX)
app.include_router(device.router, prefix=settings.API_PREFIX)
app.include_router(realtime.router, prefix=settings.API_PREFIX)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }

@app.get("/")
async def root():
    """Welcome message"""
    return {
        "message": "API Monitoring TMAT - Portal V1",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True if settings.ENVIRONMENT == "development" else False
    )