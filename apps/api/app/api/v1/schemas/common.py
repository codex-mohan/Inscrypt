"""
Common schemas for the API
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class APIResponse(BaseModel):
    """Base API response model"""
    success: bool
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class FileUploadResponse(BaseModel):
    """Response model for file upload operations"""
    file_id: str
    file_name: str
    file_size: int
    file_type: str
    upload_time: str


class FileDownloadResponse(BaseModel):
    """Response model for file download operations"""
    download_url: str
    file_name: str
    file_size: int
    expires_at: str