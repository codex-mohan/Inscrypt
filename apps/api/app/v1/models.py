from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class EmbedRequest(BaseModel):
    message: str = Field(..., description="The secret message to embed in the file.")
    encryption_algos: List[str] = Field(..., description="A list of encryption algorithms to apply.")
    password: str = Field(..., description="The password for deriving the encryption keys.")
    hash_function: str = Field(..., description="The hash function to use for key derivation.")
    stenographic_technique: str = Field(..., description="The steganography technique to use for hiding the message.")

class ExtractRequest(BaseModel):
    password: str = Field(..., description="The password used during the embedding process.")
    stenographic_technique: str = Field(..., description="The steganography technique used during embedding.")
    codebook: Optional[Dict[str, Any]] = Field(None, description="The codebook generated during embedding. Contains metadata for decryption.")
    encryption_algos: Optional[List[str]] = Field(None, description="A list of encryption algorithms used. Required if codebook is not provided.")
    hash_function: Optional[str] = Field(None, description="The hash function used. Required if codebook is not provided.")