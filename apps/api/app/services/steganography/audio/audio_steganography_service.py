"""
Audio steganography service using LSB and FFT techniques
"""

import numpy as np
import soundfile as sf
from scipy.fft import fft, ifft
from io import BytesIO
from typing import Optional, Tuple

from app.core.exceptions import SteganographyException, FileProcessingException
from app.core.config import settings
from .models import AudioSteganographyAlgorithm, AudioSteganographyResult, AudioExtractionResult


class AudioSteganographyService:
    """Service for embedding and extracting data in audio using LSB and FFT"""

    def __init__(self):
        self.supported_algorithms = {
            AudioSteganographyAlgorithm.LSB: self._lsb_steganography,
            AudioSteganographyAlgorithm.FFT: self._fft_steganography,
        }
        self.supported_extraction_algorithms = {
            AudioSteganographyAlgorithm.LSB: self._lsb_extraction,
            AudioSteganographyAlgorithm.FFT: self._fft_extraction,
        }

    def embed_data(
        self,
        audio_path: str,
        data_to_hide: bytes,
        algorithm: AudioSteganographyAlgorithm,
        output_path: Optional[str] = None,
    ) -> AudioSteganographyResult:
        """Embed data into an audio file using the specified algorithm."""
        if algorithm not in self.supported_algorithms:
            raise SteganographyException(f"Unsupported steganography algorithm: {algorithm.value}")

        try:
            return self.supported_algorithms[algorithm](audio_path, data_to_hide, output_path)
        except Exception as e:
            raise SteganographyException(f"Failed to embed data: {str(e)}")

    def extract_data(
        self,
        audio_path: str,
        algorithm: AudioSteganographyAlgorithm,
        data_length: Optional[int] = None,
    ) -> AudioExtractionResult:
        """Extract hidden data from an audio file using the specified algorithm."""
        if algorithm not in self.supported_extraction_algorithms:
            raise SteganographyException(f"Unsupported steganography algorithm for extraction: {algorithm.value}")

        try:
            return self.supported_extraction_algorithms[algorithm](audio_path, data_length)
        except Exception as e:
            raise SteganographyException(f"Failed to extract data: {str(e)}")

    def _read_audio_file(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """Reads an audio file and returns its data and sample rate."""
        try:
            data, samplerate = sf.read(audio_path, dtype='int16')
            return data, samplerate
        except Exception as e:
            raise FileProcessingException(f"Error reading audio file: {str(e)}")

    def _write_audio_file(self, data: np.ndarray, samplerate: int, output_path: str):
        """Writes audio data to a file."""
        try:
            sf.write(output_path, data, samplerate)
        except Exception as e:
            raise FileProcessingException(f"Error writing audio file: {str(e)}")

    def _lsb_steganography(
        self, audio_path: str, data: bytes, output_path: Optional[str]
    ) -> AudioSteganographyResult:
        """Embed data into an audio file using the LSB technique."""
        try:
            audio_data, samplerate = self._read_audio_file(audio_path)
            
            # Flatten audio data for easier LSB manipulation
            flat_audio_data = audio_data.flatten()

            # Convert data to binary string
            binary_data = ''.join(format(byte, '08b') for byte in data)
            data_len = len(binary_data)

            # Check if data fits
            # 32 bits for data length + actual data bits
            if data_len + 32 > len(flat_audio_data):
                raise SteganographyException("Data is too large to hide in the audio file.")

            # Prepend data length to binary data
            binary_data = format(data_len, '032b') + binary_data

            data_idx = 0
            for i in range(len(flat_audio_data)):
                if data_idx < len(binary_data):
                    current_bit = int(binary_data[data_idx])
                    flat_audio_data[i] = (flat_audio_data[i] & ~1) | current_bit
                    data_idx += 1
                else:
                    break
            
            # Reshape audio data back to original shape
            stego_audio_data = flat_audio_data.reshape(audio_data.shape)

            if not output_path:
                output_path = f"{settings.OUTPUT_DIR}/stego_audio.wav"
            
            self._write_audio_file(stego_audio_data, samplerate, output_path)

            return AudioSteganographyResult(
                output_file_path=output_path,
                algorithm=AudioSteganographyAlgorithm.LSB.value,
                hidden_data_size=len(data),
            )
        except Exception as e:
            raise SteganographyException(f"Error processing audio for LSB embedding: {str(e)}")

    def _lsb_extraction(
        self, audio_path: str, data_length: Optional[int]
    ) -> AudioExtractionResult:
        """Extract hidden data from an audio file using the LSB technique."""
        try:
            audio_data, _ = self._read_audio_file(audio_path)
            flat_audio_data = audio_data.flatten()

            binary_data_bits = []
            
            # First, extract the length of the hidden data (32 bits)
            extracted_len_bits = []
            for i in range(32):
                if i < len(flat_audio_data):
                    extracted_len_bits.append(str(flat_audio_data[i] & 1))
                else:
                    raise SteganographyException("Could not extract data length from audio.")
            
            actual_data_length = int("".join(extracted_len_bits), 2)
            
            if data_length and data_length != actual_data_length:
                raise SteganographyException(
                    f"Provided data length ({data_length}) does not match extracted length ({actual_data_length})."
                )
            
            # Now extract the actual hidden data
            for i in range(32, 32 + actual_data_length):
                if i < len(flat_audio_data):
                    binary_data_bits.append(str(flat_audio_data[i] & 1))
                else:
                    raise SteganographyException("Incomplete data extracted from audio.")

            # Convert binary string to bytes
            extracted_bytes = bytearray()
            for i in range(0, len(binary_data_bits), 8):
                byte = int("".join(binary_data_bits[i:i+8]), 2)
                extracted_bytes.append(byte)

            return AudioExtractionResult(
                extracted_data=bytes(extracted_bytes),
                algorithm=AudioSteganographyAlgorithm.LSB.value,
                metadata={"original_data_length": actual_data_length}
            )
        except Exception as e:
            raise SteganographyException(f"Error processing audio for LSB extraction: {str(e)}")

    def _fft_steganography(
        self, audio_path: str, data: bytes, output_path: Optional[str]
    ) -> AudioSteganographyResult:
        """Embed data into an audio file using the FFT technique."""
        try:
            audio_data, samplerate = self._read_audio_file(audio_path)
            
            # Convert data to binary string
            binary_data = ''.join(format(byte, '08b') for byte in data)
            data_len = len(binary_data)

            # Perform FFT
            fft_data = fft(audio_data, axis=0)
            
            # Check if data fits
            # 32 bits for data length + actual data bits
            if data_len + 32 > fft_data.size:
                raise SteganographyException("Data is too large to hide in the audio file using FFT.")

            # Prepend data length to binary data
            binary_data = format(data_len, '032b') + binary_data

            # Embed data into the magnitude of the FFT coefficients
            # We'll embed in the real part for simplicity, or a more robust method
            # For simplicity, let's embed in the LSB of the real part of the FFT coefficients
            flat_fft_real = fft_data.real.flatten()
            
            data_idx = 0
            for i in range(len(flat_fft_real)):
                if data_idx < len(binary_data):
                    current_bit = int(binary_data[data_idx])
                    # Manipulate the LSB of the integer part of the real component
                    flat_fft_real[i] = (int(flat_fft_real[i]) & ~1) | current_bit
                    data_idx += 1
                else:
                    break
            
            # Reconstruct FFT data
            stego_fft_data = flat_fft_real.reshape(fft_data.real.shape) + 1j * fft_data.imag
            
            # Perform inverse FFT
            stego_audio_data = ifft(stego_fft_data, axis=0).real.astype(audio_data.dtype)

            if not output_path:
                output_path = f"{settings.OUTPUT_DIR}/stego_audio_fft.wav"
            
            self._write_audio_file(stego_audio_data, samplerate, output_path)

            return AudioSteganographyResult(
                output_file_path=output_path,
                algorithm=AudioSteganographyAlgorithm.FFT.value,
                hidden_data_size=len(data),
            )
        except Exception as e:
            raise SteganographyException(f"Error processing audio for FFT embedding: {str(e)}")

    def _fft_extraction(
        self, audio_path: str, data_length: Optional[int]
    ) -> AudioExtractionResult:
        """Extract hidden data from an audio file using the FFT technique."""
        try:
            audio_data, _ = self._read_audio_file(audio_path)
            
            # Perform FFT
            fft_data = fft(audio_data, axis=0)
            flat_fft_real = fft_data.real.flatten()

            binary_data_bits = []
            
            # First, extract the length of the hidden data (32 bits)
            extracted_len_bits = []
            for i in range(32):
                if i < len(flat_fft_real):
                    extracted_len_bits.append(str(int(flat_fft_real[i]) & 1))
                else:
                    raise SteganographyException("Could not extract data length from audio.")
            
            actual_data_length = int("".join(extracted_len_bits), 2)
            
            if data_length and data_length != actual_data_length:
                raise SteganographyException(
                    f"Provided data length ({data_length}) does not match extracted length ({actual_data_length})."
                )
            
            # Now extract the actual hidden data
            for i in range(32, 32 + actual_data_length):
                if i < len(flat_fft_real):
                    binary_data_bits.append(str(int(flat_fft_real[i]) & 1))
                else:
                    raise SteganographyException("Incomplete data extracted from audio.")

            # Convert binary string to bytes
            extracted_bytes = bytearray()
            for i in range(0, len(binary_data_bits), 8):
                byte = int("".join(binary_data_bits[i:i+8]), 2)
                extracted_bytes.append(byte)

            return AudioExtractionResult(
                extracted_data=bytes(extracted_bytes),
                algorithm=AudioSteganographyAlgorithm.FFT.value,
                metadata={"original_data_length": actual_data_length}
            )
        except Exception as e:
            raise SteganographyException(f"Error processing audio for FFT extraction: {str(e)}")