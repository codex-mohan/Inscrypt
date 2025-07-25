"""
Models for audio steganography service
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel


class AudioSteganographyAlgorithm(str, Enum):
    """Supported audio steganography algorithms"""
    LSB = "LSB"
    FFT = "FFT"  # Fourier Transform
    # Add other audio steganography algorithms here


class AudioSteganographyResult(BaseModel):
    """Result of audio steganography operation"""
    output_file_path: str
    algorithm: str
    hidden_data_size: int
    metadata: Optional[dict] = None


class AudioExtractionResult(BaseModel):
    """Result of audio data extraction operation"""
    extracted_data: bytes
    algorithm: str
    metadata: Optional[dict] = None