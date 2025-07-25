"""
Models for image steganography service
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SteganographyAlgorithm(str, Enum):
    """Supported steganography algorithms"""
    LSB = "LSB"
    # Add other image steganography algorithms here


class SteganographyResult(BaseModel):
    """Result of steganography operation"""
    output_file_path: str
    algorithm: str
    hidden_data_size: int
    metadata: Optional[dict] = None


class ExtractionResult(BaseModel):
    """Result of data extraction operation"""
    extracted_data: bytes
    algorithm: str
    metadata: Optional[dict] = None