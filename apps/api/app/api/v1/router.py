"""
API v1 router
"""

from fastapi import APIRouter

from app.api.v1.routes import encryption, hashing, steganography

api_router = APIRouter()

# Include all routes
api_router.include_router(encryption.router, prefix="/encryption", tags=["encryption"])
api_router.include_router(hashing.router, prefix="/hashing", tags=["hashing"])
api_router.include_router(steganography.router, prefix="/steganography", tags=["steganography"])