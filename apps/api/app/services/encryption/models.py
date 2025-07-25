"""
Encryption models and enums
"""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.services.hashing.models import HashSettings


class EncryptionAlgorithm(str, Enum):
    """Supported encryption algorithms"""
    AES = "AES"
    DES = "DES"
    DES3 = "DES3"
    CHACHA20 = "ChaCha20"
    CHACHA20_POLY1305 = "ChaCha20_Poly1305"
    BLOWFISH = "Blowfish"
    ARC2 = "ARC2"
    ARC4 = "ARC4"
    SALSA20 = "Salsa20"
    CAST = "CAST"
    PKCS1_OAEP = "PKCS1_OAEP"
    PKCS1_V1_5 = "PKCS1_v1_5"
    XOR = "XOR"


class EncryptionMode(str, Enum):
    """Supported encryption modes"""
    CBC = "CBC"
    CFB = "CFB"
    OFB = "OFB"
    CTR = "CTR"
    ECB = "ECB"
    GCM = "GCM"


class EncryptionResult(BaseModel):
    """Result of encryption operation"""
    encrypted_data: bytes
    key: bytes
    iv: Optional[bytes] = None
    nonce: Optional[bytes] = None
    tag: Optional[bytes] = None
    algorithm: str
    mode: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DecryptionResult(BaseModel):
    """Result of decryption operation"""
    decrypted_data: bytes
    algorithm: str
    mode: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class EncryptionRequest(BaseModel):
    """Request model for encryption operations"""
    data: bytes
    algorithms: list[EncryptionAlgorithm]
    key: Optional[bytes] = None
    mode: Optional[EncryptionMode] = None
    key_size: Optional[int] = None
    hash: Optional[HashSettings] = None


class DecryptionRequest(BaseModel):
    """Request model for decryption operations"""
    encrypted_data: bytes
    key: bytes
    algorithms: list[EncryptionAlgorithm]
    mode: Optional[EncryptionMode] = None
    iv: Optional[bytes] = None
    nonce: Optional[bytes] = None
    tag: Optional[bytes] = None