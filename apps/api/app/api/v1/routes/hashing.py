"""
Hashing API routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import base64

from app.services.hashing import HashingService
from app.services.hashing.models import HashAlgorithm, SupportedHash

router = APIRouter()

# Initialize hashing service
hashing_service = HashingService()


class HashRequest(BaseModel):
    data: str
    algorithm: HashAlgorithm
    key: Optional[str] = None
    output_length: Optional[int] = None
    custom: Optional[str] = None


class HashResponse(BaseModel):
    hash_value: str
    algorithm: str
    length: int
    hex_digest: str


class VerifyRequest(BaseModel):
    data: str
    expected_hash: str
    algorithm: HashAlgorithm
    key: Optional[str] = None
    output_length: Optional[int] = None
    custom: Optional[str] = None


class VerifyResponse(BaseModel):
    is_valid: bool
    algorithm: str


@router.get("/algorithms", response_model=list)
async def get_supported_algorithms():
    """Get list of supported hashing algorithms"""
    return [algo.value for algo in HashAlgorithm]


@router.get("/supported", response_model=list[SupportedHash])
async def get_supported_hashes():
    """Get list of supported hashing algorithms and their settings"""
    return hashing_service.get_supported_hashes()