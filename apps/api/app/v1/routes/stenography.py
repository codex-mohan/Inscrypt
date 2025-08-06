from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Request
import uuid
from fastapi.responses import FileResponse
from typing import List, Dict, Any, Optional
from app.logging_config import logger
from app.v1.core.encryption import encrypt_data, decrypt_data
from app.v1.core.stenography import (
    hide_message_in_image,
    extract_message_from_image,
    hide_message_in_audio,
    extract_message_from_audio,
    hide_message_in_video,
    extract_message_from_video,
)
from fastapi.responses import FileResponse
import mimetypes
import json
import os

from app.logging_config import setup_logging  # triggers the single setup
import logging

import base64

logger = logging.getLogger(__name__)

router = APIRouter()

SUPPORTED_ENCRYPTION_ALGORITHMS = [
    "AES",
    "DES",
    "DES3",
    "ChaCha20",
    "ChaCha20_Poly1305",
    "Blowfish",
    "ARC2",
    "ARC4",
    "Salsa20",
    "CAST",
    "PKCS1_OAEP",
    "PKCS1_v1_5",
    "XOR",
]

SUPPORTED_HASH_ALGORITHMS = [
    "keccak",
    "SHA1",
    "SHA224",
    "SHA256",
    "SHA384",
    "SHA512",
    "SHA3_224",
    "SHA3_256",
    "SHA3_384",
    "SHA3_512",
    "TupleHash128",
    "TupleHash256",
    "SHAKE128",
    "SHAKE256",
    "cSHAKE128",
    "cSHAKE256",
    "KangarooTwelve",
    "Whirlpool",
    "blake2b",
    "blake2s",
]

SUPPORTED_STEGANOGRAPHY_TECHNIQUES = {
    "image": [
        {"name": "LSB", "description": "Least Significant Bit substitution."},
        {
            "name": "DCT",
            "description": "Discrete Cosine Transform coefficient modification.",
        },
        {
            "name": "DWT",
            "description": "Discrete Wavelet Transform coefficient modification.",
        },
    ],
    "audio": [
        {
            "name": "LSB",
            "description": "Least Significant Bit substitution in audio samples.",
        },
        {
            "name": "EchoHiding",
            "description": "Hiding data in the echo of the audio signal.",
        },
        {
            "name": "PhaseCoding",
            "description": "Hiding data in the phase of the audio signal.",
        },
    ],
    "video": [
        {
            "name": "LSB",
            "description": "Least Significant Bit substitution in video frames.",
        },
        {
            "name": "MotionVector",
            "description": "Hiding data in the motion vectors of the video.",
        },
    ],
}


@router.get("/supported")
async def get_supported_methods() -> Dict[str, Any]:
    """
    Returns a list of supported encryption algorithms, hash functions, and steganography techniques.
    """
    return {
        "encryption_algorithms": SUPPORTED_ENCRYPTION_ALGORITHMS,
        "hash_algorithms": SUPPORTED_HASH_ALGORITHMS,
        "steganography_techniques": SUPPORTED_STEGANOGRAPHY_TECHNIQUES,
    }


@router.post("/embed")
async def embed_message(
    request: Request,
    file: UploadFile = File(...),
    message: str = Form(...),
    encryption_algos: str = Form(...),
    password: str = Form(...),
    hash_function: str = Form(...),
    stenographic_technique: str = Form(...),
):
    try:
        # Save the uploaded file temporarily with a unique name
        temp_dir = "/tmp"
        os.makedirs(temp_dir, exist_ok=True)
        unique_filename = f"temp_{uuid.uuid4().hex}_{file.filename}"
        temp_file_path = os.path.join(temp_dir, unique_filename)
        with open(temp_file_path, "wb") as f:
            f.write(file.file.read())

        encryption_layers = [algo.strip() for algo in encryption_algos.split(",")]

        print(encryption_layers)

        unsupported_algos = [
            algo
            for algo in encryption_layers
            if algo.upper() not in SUPPORTED_ENCRYPTION_ALGORITHMS
        ]

        print(f"unsupported algorithms: {unsupported_algos}")

        if unsupported_algos:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported encryption algorithm(s): {', '.join(unsupported_algos)}",
            )

        encrypted_result = encrypt_data(
            data=message.encode("utf-8"),
            password=password,
            encryption_layers=encryption_layers,
            hash_name=hash_function,
        )

        logger.debug(f"Raw encrypted data: {encrypted_result!r}")

        output_file_name = (
            f"/tmp/output_{uuid.uuid4().hex}.{file.filename.split('.')[-1]}"
        )
        
        # Serialize codebook and combine with encrypted data
        codebook_json = json.dumps(encrypted_result["codebook"])
        encrypted_data_b64 = encrypted_result["encrypted_data"]

        # Use a unique, unlikely delimiter
        delimiter = b"||CODEBOOK_DELIMITER||"

        combined_payload = (
            codebook_json.encode("utf-8")
            + delimiter
            + encrypted_data_b64.encode("utf-8")
        )
        
        logger.debug(f"Combined payload length: {len(combined_payload)}")

        if file.content_type.startswith("image/"):
            output_path = hide_message_in_image(
                temp_file_path,
                combined_payload,
                stenographic_technique,
                output_path=output_file_name,
            )
        elif file.content_type.startswith("audio/"):
            output_path = hide_message_in_audio(
                temp_file_path,
                combined_payload,
                stenographic_technique,
            )
        elif file.content_type.startswith("video/"):
            output_path = hide_message_in_video(
                temp_file_path,
                combined_payload,
                stenographic_technique,
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        os.remove(temp_file_path)

        return {
            "output_path": os.path.basename(output_path),
        }
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract")
async def extract_message(
    file: UploadFile = File(...),
    password: str = Form(...),
    stenographic_technique: str = Form(...),
):
    try:
        logger.info(f"Received extract request for file: {file.filename}")

        # 1. save uploaded file
        temp_dir = "/tmp"
        os.makedirs(temp_dir, exist_ok=True)
        unique_filename = f"temp_{uuid.uuid4().hex}_{file.filename}"
        temp_file_path = os.path.join(temp_dir, unique_filename)
        with open(temp_file_path, "wb") as f:
            f.write(file.file.read())

        # 2. read steganographically hidden payload
        if file.content_type.startswith("image/"):
            combined_payload = extract_message_from_image(
                temp_file_path, stenographic_technique
            )
        elif file.content_type.startswith("audio/"):
            combined_payload = extract_message_from_audio(
                temp_file_path, stenographic_technique
            )
        elif file.content_type.startswith("video/"):
            combined_payload = extract_message_from_video(
                temp_file_path, stenographic_technique
            )
        else:
            logger.error(f"Unsupported file type: {file.content_type}")
            raise HTTPException(status_code=400, detail="Unsupported file type")

        logger.info("Payload extracted successfully.")
        os.remove(temp_file_path)

        # 3. Separate codebook and encrypted data
        delimiter = b"||CODEBOOK_DELIMITER||"
        if delimiter not in combined_payload:
            logger.error(f"Delimiter not found in payload. Payload length: {len(combined_payload)}")
            logger.debug(f"Payload (first 100 bytes): {combined_payload[:100]!r}")
            raise HTTPException(
                status_code=400, detail="Invalid payload format: delimiter not found."
            )

        codebook_json_bytes, encrypted_data_b64_bytes = combined_payload.split(
            delimiter, 1
        )
        codebook_json = codebook_json_bytes.decode('utf-8')
        
        try:
            codebook = json.loads(codebook_json)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid codebook format.")

        # 4. decrypt
        decrypted_message = decrypt_data(
            encrypted_data=base64.b64decode(encrypted_data_b64_bytes),
            password=password,
            codebook=codebook,
        )

        logger.info("Decryption successful.")
        return {"message": decrypted_message.decode()}
    except Exception as e:
        logger.error("An error occurred during extraction", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = f"/tmp/{file_name}"
    print(f"Downloading file: {file_path}")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    media_type, _ = mimetypes.guess_type(file_path)
    return FileResponse(
        file_path,
        filename=file_name,
        media_type=media_type or "application/octet-stream",
    )
