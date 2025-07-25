"""
Video steganography service
"""

import os
import cv2
import numpy as np
from moviepy import VideoFileClip, AudioFileClip
from typing import Optional, Tuple

from app.core.exceptions import SteganographyException, FileProcessingException
from app.core.config import settings
from .models import (
    VideoSteganographyAlgorithm,
    VideoSteganographyResult,
    VideoExtractionResult,
)


class VideoSteganographyService:
    """Service for embedding and extracting data in video files"""

    def __init__(self):
        self.supported_algorithms = {
            VideoSteganographyAlgorithm.LSB: self._lsb_steganography,
        }
        self.supported_extraction_algorithms = {
            VideoSteganographyAlgorithm.LSB: self._lsb_extraction,
        }

    def embed_data(
        self,
        video_path: str,
        data_to_hide: bytes,
        algorithm: VideoSteganographyAlgorithm,
        output_path: Optional[str] = None,
    ) -> VideoSteganographyResult:
        """Embed data into a video file using the specified algorithm."""
        if algorithm not in self.supported_algorithms:
            raise SteganographyException(
                f"Unsupported steganography algorithm: {algorithm.value}"
            )

        try:
            return self.supported_algorithms[algorithm](
                video_path, data_to_hide, output_path
            )
        except Exception as e:
            raise SteganographyException(f"Failed to embed data: {str(e)}")

    def extract_data(
        self,
        video_path: str,
        algorithm: VideoSteganographyAlgorithm,
        data_length: Optional[int] = None,
    ) -> VideoExtractionResult:
        """Extract hidden data from a video file using the specified algorithm."""
        if algorithm not in self.supported_extraction_algorithms:
            raise SteganographyException(
                f"Unsupported steganography algorithm for extraction: {algorithm.value}"
            )

        try:
            return self.supported_extraction_algorithms[algorithm](
                video_path, data_length
            )
        except Exception as e:
            raise SteganographyException(f"Failed to extract data: {str(e)}")

    def _lsb_steganography(
        self, video_path: str, data: bytes, output_path: Optional[str]
    ) -> VideoSteganographyResult:
        """Embed data into a video file using the LSB technique."""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise FileProcessingException(
                    f"Could not open video file: {video_path}"
                )

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            if not output_path:
                output_path = f"{settings.OUTPUT_DIR}/stego_video.mp4"

            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            # Convert data to binary string
            binary_data = "".join(format(byte, "08b") for byte in data)
            data_len = len(binary_data)

            # Prepend data length to binary data
            binary_data = format(data_len, "032b") + binary_data

            data_idx = 0
            frame_count = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if data_idx < len(binary_data):
                    # Embed data into the LSB of each pixel's color channels
                    for r in range(height):
                        for c in range(width):
                            for channel in range(3):  # B, G, R channels
                                if data_idx < len(binary_data):
                                    current_bit = int(binary_data[data_idx])
                                    frame[r, c, channel] = (
                                        frame[r, c, channel] & 0xFE
                                    ) | current_bit
                                    data_idx += 1
                                else:
                                    break
                            if data_idx >= len(binary_data):
                                break
                        if data_idx >= len(binary_data):
                            break

                out.write(frame)
                frame_count += 1

            cap.release()
            out.release()
            cv2.destroyAllWindows()

            if data_idx < len(binary_data):
                raise SteganographyException(
                    "Not enough frames/pixels in video to hide all data."
                )

            return VideoSteganographyResult(
                output_file_path=output_path,
                algorithm=VideoSteganographyAlgorithm.LSB.value,
                hidden_data_size=len(data),
            )
        except Exception as e:
            raise SteganographyException(
                f"Error processing video for LSB embedding: {str(e)}"
            )

    def _lsb_extraction(
        self, video_path: str, data_length: Optional[int]
    ) -> VideoExtractionResult:
        """Extract hidden data from a video file using the LSB technique."""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise FileProcessingException(
                    f"Could not open video file: {video_path}"
                )

            binary_data_bits = []

            # First, extract the length of the hidden data (32 bits)
            extracted_len_bits = []

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                for r in range(frame.shape[0]):
                    for c in range(frame.shape[1]):
                        for channel in range(3):
                            extracted_len_bits.append(str(frame[r, c, channel] & 1))
                            if len(extracted_len_bits) == 32:
                                break
                        if len(extracted_len_bits) == 32:
                            break
                    if len(extracted_len_bits) == 32:
                        break
                if len(extracted_len_bits) == 32:
                    break

            cap.release()
            cv2.destroyAllWindows()

            if len(extracted_len_bits) < 32:
                raise SteganographyException(
                    "Could not extract data length from video."
                )

            actual_data_length = int("".join(extracted_len_bits), 2)

            if data_length and data_length != actual_data_length:
                raise SteganographyException(
                    f"Provided data length ({data_length}) does not match extracted length ({actual_data_length})."
                )

            # Re-open video to extract actual data
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise FileProcessingException(
                    f"Could not open video file: {video_path}"
                )

            data_idx = 32  # Start after the length bits

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                for r in range(frame.shape[0]):
                    for c in range(frame.shape[1]):
                        for channel in range(3):
                            if (
                                data_idx > 31
                                and len(binary_data_bits) < actual_data_length
                            ):
                                binary_data_bits.append(str(frame[r, c, channel] & 1))
                            data_idx += 1
                            if len(binary_data_bits) == actual_data_length:
                                break
                        if len(binary_data_bits) == actual_data_length:
                            break
                    if len(binary_data_bits) == actual_data_length:
                        break
                if len(binary_data_bits) == actual_data_length:
                    break

            cap.release()
            cv2.destroyAllWindows()

            if len(binary_data_bits) < actual_data_length:
                raise SteganographyException("Incomplete data extracted from video.")

            # Convert binary string to bytes
            extracted_bytes = bytearray()
            for i in range(0, len(binary_data_bits), 8):
                byte = int("".join(binary_data_bits[i : i + 8]), 2)
                extracted_bytes.append(byte)

            return VideoExtractionResult(
                extracted_data=bytes(extracted_bytes),
                algorithm=VideoSteganographyAlgorithm.LSB.value,
                metadata={"original_data_length": actual_data_length},
            )
        except Exception as e:
            raise SteganographyException(
                f"Error processing video for LSB extraction: {str(e)}"
            )
