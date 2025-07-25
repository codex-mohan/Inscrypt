"""
Custom exceptions for the Inscrypt application
"""

from typing import Optional


class InscryptException(Exception):
    """Base exception for Inscrypt application"""
    
    def __init__(
        self,
        detail: str,
        status_code: int = 400,
        error_code: Optional[str] = None
    ):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.detail)


class EncryptionException(InscryptException):
    """Exception raised for encryption-related errors"""
    pass


class DecryptionException(InscryptException):
    """Exception raised for decryption-related errors"""
    pass


class SteganographyException(InscryptException):
    """Exception raised for steganography-related errors"""
    pass


class FileProcessingException(InscryptException):
    """Exception raised for file processing errors"""
    pass


class ValidationException(InscryptException):
    """Exception raised for validation errors"""
    pass


class KeyGenerationException(InscryptException):
    """Exception raised for key generation errors"""
    pass


class HashingException(InscryptException):
    """Exception raised for hashing errors"""
    pass


class UnsupportedAlgorithmException(InscryptException):
    """Exception raised when an unsupported algorithm is requested"""
    def __init__(self, algorithm: str):
        super().__init__(
            detail=f"Unsupported algorithm: {algorithm}",
            status_code=400,
            error_code="UNSUPPORTED_ALGORITHM"
        )


class InvalidKeyException(InscryptException):
    """Exception raised for invalid encryption keys"""
    def __init__(self, detail: str = "Invalid encryption key"):
        super().__init__(
            detail=detail,
            status_code=400,
            error_code="INVALID_KEY"
        )


class FileTooLargeException(InscryptException):
    """Exception raised when file size exceeds limit"""
    def __init__(self, max_size: int):
        super().__init__(
            detail=f"File too large. Maximum size: {max_size} bytes",
            status_code=413,
            error_code="FILE_TOO_LARGE"
        )


class UnsupportedFileTypeException(InscryptException):
    """Exception raised for unsupported file types"""
    def __init__(self, file_type: str):
        super().__init__(
            detail=f"Unsupported file type: {file_type}",
            status_code=415,
            error_code="UNSUPPORTED_FILE_TYPE"
        )