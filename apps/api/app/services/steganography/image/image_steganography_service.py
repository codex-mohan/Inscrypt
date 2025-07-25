"""
Image steganography service using LSB (Least Significant Bit) technique
"""

from PIL import Image
import numpy as np
from io import BytesIO
from typing import Optional

from app.core.exceptions import SteganographyException, FileProcessingException
from app.core.config import settings
from .models import SteganographyAlgorithm, SteganographyResult, ExtractionResult


class ImageSteganographyService:
    """Service for embedding and extracting data in images using LSB"""

    def __init__(self):
        self.supported_algorithms = {
            SteganographyAlgorithm.LSB: self._lsb_steganography,
        }
        self.supported_extraction_algorithms = {
            SteganographyAlgorithm.LSB: self._lsb_extraction,
        }

    def embed_data(
        self,
        image_path: str,
        data_to_hide: bytes,
        algorithm: SteganographyAlgorithm = SteganographyAlgorithm.LSB,
        output_path: Optional[str] = None,
    ) -> SteganographyResult:
        """Embed data into an image using the specified algorithm."""
        if algorithm not in self.supported_algorithms:
            raise SteganographyException(f"Unsupported steganography algorithm: {algorithm.value}")

        try:
            return self.supported_algorithms[algorithm](image_path, data_to_hide, output_path)
        except Exception as e:
            raise SteganographyException(f"Failed to embed data: {str(e)}")

    def extract_data(
        self,
        image_path: str,
        algorithm: SteganographyAlgorithm = SteganographyAlgorithm.LSB,
        data_length: Optional[int] = None,
    ) -> ExtractionResult:
        """Extract hidden data from an image using the specified algorithm."""
        if algorithm not in self.supported_extraction_algorithms:
            raise SteganographyException(f"Unsupported steganography algorithm for extraction: {algorithm.value}")

        try:
            return self.supported_extraction_algorithms[algorithm](image_path, data_length)
        except Exception as e:
            raise SteganographyException(f"Failed to extract data: {str(e)}")

    def _lsb_steganography(
        self, image_path: str, data: bytes, output_path: Optional[str]
    ) -> SteganographyResult:
        """Embed data into an image using the LSB technique."""
        try:
            img = Image.open(image_path).convert("RGBA")
            width, height = img.size
            pixels = np.array(img)

            # Convert data to binary string
            binary_data = ''.join(format(byte, '08b') for byte in data)
            data_len = len(binary_data)

            if data_len + 32 > width * height * 4:  # 32 bits for data length
                raise SteganographyException("Data is too large to hide in the image.")

            # Prepend data length to binary data
            binary_data = format(data_len, '032b') + binary_data

            data_idx = 0
            for r in range(height):
                for c in range(width):
                    for channel in range(4):  # R, G, B, A channels
                        if data_idx < len(binary_data):
                            current_bit = int(binary_data[data_idx])
                            pixels[r, c, channel] = (pixels[r, c, channel] & 0xFE) | current_bit
                            data_idx += 1
                        else:
                            break
                    if data_idx >= len(binary_data):
                        break
                if data_idx >= len(binary_data):
                    break

            stego_img = Image.fromarray(pixels, 'RGBA')
            
            if not output_path:
                output_path = f"{settings.OUTPUT_DIR}/stego_image.png"
            
            stego_img.save(output_path)

            return SteganographyResult(
                output_file_path=output_path,
                algorithm=SteganographyAlgorithm.LSB.value,
                hidden_data_size=len(data),
            )
        except Exception as e:
            raise FileProcessingException(f"Error processing image for LSB embedding: {str(e)}")

    def _lsb_extraction(
        self, image_path: str, data_length: Optional[int]
    ) -> ExtractionResult:
        """Extract hidden data from an image using the LSB technique."""
        try:
            img = Image.open(image_path).convert("RGBA")
            width, height = img.size
            pixels = np.array(img)

            binary_data_bits = []
            
            # First, extract the length of the hidden data (32 bits)
            extracted_len_bits = []
            for r in range(height):
                for c in range(width):
                    for channel in range(4):
                        extracted_len_bits.append(str(pixels[r, c, channel] & 1))
                        if len(extracted_len_bits) == 32:
                            break
                    if len(extracted_len_bits) == 32:
                        break
                if len(extracted_len_bits) == 32:
                    break
            
            if len(extracted_len_bits) < 32:
                raise SteganographyException("Could not extract data length from image.")
            
            actual_data_length = int("".join(extracted_len_bits), 2)
            
            if data_length and data_length != actual_data_length:
                raise SteganographyException(
                    f"Provided data length ({data_length}) does not match extracted length ({actual_data_length})."
                )
            
            # Now extract the actual hidden data
            data_idx = 32 # Start after the length bits
            for r in range(height):
                for c in range(width):
                    for channel in range(4):
                        if data_idx > 31 and len(binary_data_bits) < actual_data_length:
                            binary_data_bits.append(str(pixels[r, c, channel] & 1))
                        data_idx += 1
                        if len(binary_data_bits) == actual_data_length:
                            break
                    if len(binary_data_bits) == actual_data_length:
                        break
                if len(binary_data_bits) == actual_data_length:
                    break

            if len(binary_data_bits) < actual_data_length:
                raise SteganographyException("Incomplete data extracted from image.")

            # Convert binary string to bytes
            extracted_bytes = bytearray()
            for i in range(0, len(binary_data_bits), 8):
                byte = int("".join(binary_data_bits[i:i+8]), 2)
                extracted_bytes.append(byte)

            return ExtractionResult(
                extracted_data=bytes(extracted_bytes),
                algorithm=SteganographyAlgorithm.LSB.value,
                metadata={"original_data_length": actual_data_length}
            )
        except Exception as e:
            raise FileProcessingException(f"Error processing image for LSB extraction: {str(e)}")