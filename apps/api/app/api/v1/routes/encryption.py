"""
Encryption API routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import base64

from app.services.encryption import EncryptionService
from app.services.encryption.models import (
    EncryptionAlgorithm,
    EncryptionMode,
    EncryptionRequest,
    DecryptionRequest,
)
from app.services.hashing.models import HashSettings

router = APIRouter()

# Initialize encryption service
encryption_service = EncryptionService()


class EncryptRequest(BaseModel):
    data: str
    algorithms: list[EncryptionAlgorithm]
    key: Optional[str] = None
    mode: Optional[EncryptionMode] = None
    key_size: Optional[int] = None
    hash: Optional[HashSettings] = None


class EncryptResponse(BaseModel):
    encrypted_data: str
    key: str
    iv: Optional[str] = None
    nonce: Optional[str] = None
    tag: Optional[str] = None
    algorithm: str
    mode: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DecryptRequest(BaseModel):
    encrypted_data: str
    key: str
    algorithms: list[EncryptionAlgorithm]
    mode: Optional[EncryptionMode] = None
    iv: Optional[str] = None
    nonce: Optional[str] = None
    tag: Optional[str] = None


class DecryptResponse(BaseModel):
    decrypted_data: str
    algorithm: str
    mode: Optional[str] = None


@router.post("/encrypt", response_model=EncryptResponse)
async def encrypt_data(request: EncryptRequest):
    """Encrypt data using the specified algorithm"""
    try:
        # Convert base64 data to bytes
        data_bytes = base64.b64decode(request.data)
        
        # Convert base64 key to bytes if provided
        key_bytes = base64.b64decode(request.key) if request.key else None
        
        # Perform encryption
        result = encryption_service.encrypt(
            data=data_bytes,
            algorithms=request.algorithms,
            key=key_bytes,
            mode=request.mode,
            key_size=request.key_size,
            hash_settings=request.hash
        )
        
        # Convert bytes to base64 for response
        response = EncryptResponse(
            encrypted_data=base64.b64encode(result.encrypted_data).decode(),
            key=base64.b64encode(result.key).decode(),
            algorithm=result.algorithm,
            mode=result.mode,
            metadata=result.metadata
        )
        
        if result.iv:
            response.iv = base64.b64encode(result.iv).decode()
        if result.nonce:
            response.nonce = base64.b64encode(result.nonce).decode()
        if result.tag:
            response.tag = base64.b64encode(result.tag).decode()
            
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/decrypt", response_model=DecryptResponse)
async def decrypt_data(request: DecryptRequest):
    """Decrypt data using the specified algorithm"""
    try:
        # Convert base64 data to bytes
        encrypted_data_bytes = base64.b64decode(request.encrypted_data)
        key_bytes = base64.b64decode(request.key)
        iv_bytes = base64.b64decode(request.iv) if request.iv else None
        nonce_bytes = base64.b64decode(request.nonce) if request.nonce else None
        tag_bytes = base64.b64decode(request.tag) if request.tag else None
        
        # Perform decryption
        result = encryption_service.decrypt(
            encrypted_data=encrypted_data_bytes,
            key=key_bytes,
            algorithms=request.algorithms,
            mode=request.mode,
            iv=iv_bytes,
            nonce=nonce_bytes,
            tag=tag_bytes
        )
        
        # Convert bytes to base64 for response
        return DecryptResponse(
            decrypted_data=base64.b64encode(result.decrypted_data).decode(),
            algorithm=result.algorithm,
            mode=result.mode
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/algorithms", response_model=list)
async def get_supported_algorithms():
    """Get list of supported encryption algorithms"""
    return [algo.value for algo in EncryptionAlgorithm]


@router.get("/modes", response_model=list)
async def get_supported_modes():
    """Get list of supported encryption modes"""
    return [mode.value for mode in EncryptionMode]


class GenerateKeyResponse(BaseModel):
    key: str
    algorithm: str
    key_size: int


@router.post("/generate-key", response_model=GenerateKeyResponse)
async def generate_encryption_key(
    algorithm: EncryptionAlgorithm,
    key_size: Optional[int] = None
):
    """Generate an encryption key for the specified algorithm"""
    try:
        key_bytes = encryption_service.generate_key(algorithm, key_size)
        return GenerateKeyResponse(
            key=base64.b64encode(key_bytes).decode(),
            algorithm=algorithm.value,
            key_size=len(key_bytes)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))