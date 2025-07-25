"""
Models for video steganography service
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel


class VideoSteganographyAlgorithm(str, Enum):
    """Supported video steganography algorithms"""
    LSB = "LSB"
    # Add other video steganography algorithms here


class VideoSteganographyResult(BaseModel):
    """Result of video steganography operation"""
    output_file_path: str
    algorithm: str
    hidden_data_size: int
    metadata: Optional[dict] = None


class VideoExtractionResult(BaseModel):
    """Result of video data extraction operation"""
    extracted_data: bytes
    algorithm: str
    metadata: Optional[dict] = None