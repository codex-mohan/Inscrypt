"""
Models for hashing service
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel


class HashAlgorithm(str, Enum):
    """Supported hashing algorithms"""
    SHA1 = "sha1"
    SHA224 = "sha224"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"
    SHA3_224 = "sha3_224"
    SHA3_256 = "sha3_256"
    SHA3_384 = "sha3_384"
    SHA3_512 = "sha3_512"
    SHAKE128 = "shake128"
    SHAKE256 = "shake256"
    CSHAKE128 = "cshake128"
    CSHAKE256 = "cshake256"
    TUPLEHASH128 = "tuplehash128"
    TUPLEHASH256 = "tuplehash256"
    KANGAROOTWELVE = "kangarootwelve"
    WHIRLPOOL = "whirlpool"
    BLAKE2B = "blake2b"
    BLAKE2S = "blake2s"
    KECCAK = "keccak"


class HashSettings(BaseModel):
    """Settings for hashing operations"""
    algorithm: HashAlgorithm
    key: Optional[str] = None
    output_length: Optional[int] = None
    custom: Optional[str] = None


class HashResult(BaseModel):
    """Result of hashing operation"""
    hash_value: bytes
    algorithm: str
    length: int
    hex_digest: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.hash_value is not None and self.hex_digest is None:
            self.hex_digest = self.hash_value.hex()

class SupportedHash(BaseModel):
    """Model for supported hash algorithm and its settings"""
    name: str
    output_lengths: Optional[list[int]] = None
    key_required: bool = False
    custom_required: bool = False