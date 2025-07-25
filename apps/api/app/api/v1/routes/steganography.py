"""
Steganography API routes
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import base64
import os
from pathlib import Path

from app.services.steganography.image import ImageSteganographyService
from app.services.steganography.image.models import SteganographyAlgorithm
from app.services.steganography.audio import AudioSteganographyService
from app.services.steganography.audio.models import AudioSteganographyAlgorithm
from app.services.steganography.video import VideoSteganographyService
from app.services.steganography.video.models import VideoSteganographyAlgorithm
from app.core.config import settings
from app.utils.file_handler import FileHandler

router = APIRouter()

# Initialize steganography services
image_steganography_service = ImageSteganographyService()
audio_steganography_service = AudioSteganographyService()
video_steganography_service = VideoSteganographyService()


class EmbedRequest(BaseModel):
    data_to_hide: str
    algorithm: str
    media_type: str


class ExtractRequest(BaseModel):
    algorithm: str
    media_type: str
    data_length: Optional[int] = None


class EmbedResponse(BaseModel):
    output_file_path: str
    algorithm: str
    hidden_data_size: int


class ExtractResponse(BaseModel):
    extracted_data: str
    algorithm: str


@router.post("/embed", response_model=EmbedResponse)
async def embed_data(
    file: UploadFile = File(...),
    data_to_hide: str = Form(...),
    algorithm: str = Form(...),
    media_type: str = Form(...)
):
    """Embed data into a media file using the specified algorithm"""
    try:
        # Save uploaded file using FileHandler
        file_path = await FileHandler.save_upload_file(file, settings.TEMP_DIR, settings.MAX_FILE_SIZE)
        
        # Convert base64 data to bytes
        data_bytes = base64.b64decode(data_to_hide)
        
        # Determine output path
        output_filename = f"stego_{Path(file_path).name}"
        output_path = os.path.join(settings.OUTPUT_DIR, output_filename)
        
        # Perform steganography based on media type
        if media_type == "image":
            algo_enum = SteganographyAlgorithm(algorithm)
            result = image_steganography_service.embed_data(
                image_path=file_path,
                data_to_hide=data_bytes,
                algorithm=algo_enum,
                output_path=output_path
            )
        elif media_type == "audio":
            algo_enum = AudioSteganographyAlgorithm(algorithm)
            result = audio_steganography_service.embed_data(
                audio_path=file_path,
                data_to_hide=data_bytes,
                algorithm=algo_enum,
                output_path=output_path
            )
        elif media_type == "video":
            algo_enum = VideoSteganographyAlgorithm(algorithm)
            result = video_steganography_service.embed_data(
                video_path=file_path,
                data_to_hide=data_bytes,
                algorithm=algo_enum,
                output_path=output_path
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported media type: {media_type}")
        
        # Clean up temporary file
        FileHandler.delete_file(file_path)
        
        return EmbedResponse(
            output_file_path=result.output_file_path,
            algorithm=result.algorithm,
            hidden_data_size=result.hidden_data_size
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/extract", response_model=ExtractResponse)
async def extract_data(
    file: UploadFile = File(...),
    algorithm: str = Form(...),
    media_type: str = Form(...),
    data_length: Optional[int] = Form(None)
):
    """Extract hidden data from a media file using the specified algorithm"""
    try:
        # Save uploaded file using FileHandler
        file_path = await FileHandler.save_upload_file(file, settings.TEMP_DIR, settings.MAX_FILE_SIZE)
        
        # Perform extraction based on media type
        if media_type == "image":
            algo_enum = SteganographyAlgorithm(algorithm)
            result = image_steganography_service.extract_data(
                image_path=file_path,
                algorithm=algo_enum,
                data_length=data_length
            )
        elif media_type == "audio":
            algo_enum = AudioSteganographyAlgorithm(algorithm)
            result = audio_steganography_service.extract_data(
                audio_path=file_path,
                algorithm=algo_enum,
                data_length=data_length
            )
        elif media_type == "video":
            algo_enum = VideoSteganographyAlgorithm(algorithm)
            result = video_steganography_service.extract_data(
                video_path=file_path,
                algorithm=algo_enum,
                data_length=data_length
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported media type: {media_type}")
        
        # Clean up temporary file
        FileHandler.delete_file(file_path)
        
        # Convert bytes to base64 for response
        return ExtractResponse(
            extracted_data=base64.b64encode(result.extracted_data).decode(),
            algorithm=result.algorithm
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/algorithms/image", response_model=list)
async def get_image_algorithms():
    """Get list of supported image steganography algorithms"""
    return [algo.value for algo in SteganographyAlgorithm]


@router.get("/algorithms/audio", response_model=list)
async def get_audio_algorithms():
    """Get list of supported audio steganography algorithms"""
    return [algo.value for algo in AudioSteganographyAlgorithm]


@router.get("/algorithms/video", response_model=list)
async def get_video_algorithms():
    """Get list of supported video steganography algorithms"""
    return [algo.value for algo in VideoSteganographyAlgorithm]