"""
File handling utilities
"""

import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import FileProcessingException, FileTooLargeException


class FileHandler:
    """Utility class for handling file operations"""
    
    @staticmethod
    async def save_upload_file(
        file: UploadFile,
        directory: str = settings.UPLOAD_DIR,
        max_size: Optional[int] = None
    ) -> str:
        """
        Save an uploaded file to the specified directory
        
        Args:
            file: The uploaded file
            directory: Directory to save the file to
            max_size: Maximum file size in bytes (optional)
            
        Returns:
            str: Path to the saved file
            
        Raises:
            FileTooLargeException: If file exceeds max_size
            FileProcessingException: If file processing fails
        """
        try:
            # Check file size if max_size is specified
            if max_size and file.size and file.size > max_size:
                raise FileTooLargeException(max_size)
            
            # Create directory if it doesn't exist
            Path(directory).mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            file_extension = Path(file.filename).suffix if file.filename else ""
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(directory, unique_filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            return file_path
        except FileTooLargeException:
            raise
        except Exception as e:
            raise FileProcessingException(f"Failed to save uploaded file: {str(e)}")
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete a file
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            bool: True if file was deleted, False if file didn't exist
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            raise FileProcessingException(f"Failed to delete file: {str(e)}")
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get the size of a file in bytes
        
        Args:
            file_path: Path to the file
            
        Returns:
            int: File size in bytes
            
        Raises:
            FileProcessingException: If file doesn't exist or can't be accessed
        """
        try:
            if not os.path.exists(file_path):
                raise FileProcessingException(f"File not found: {file_path}")
            return os.path.getsize(file_path)
        except Exception as e:
            raise FileProcessingException(f"Failed to get file size: {str(e)}")
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """
        Get the extension of a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: File extension (including the dot)
        """
        return Path(file_path).suffix
    
    @staticmethod
    def is_valid_file_type(file_path: str, allowed_extensions: list) -> bool:
        """
        Check if a file has a valid extension
        
        Args:
            file_path: Path to the file
            allowed_extensions: List of allowed extensions (e.g., ['.jpg', '.png'])
            
        Returns:
            bool: True if file has a valid extension, False otherwise
        """
        extension = FileHandler.get_file_extension(file_path).lower()
        return extension in [ext.lower() for ext in allowed_extensions]