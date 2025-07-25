from PIL import Image
import numpy as np
import os
from typing import Optional, Tuple

import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve

from moviepy import VideoFileClip
import cv2
import tempfile
import shutil

try:
    from pydub import AudioSegment

    _HAS_PYDUB = True
except ImportError:
    _HAS_PYDUB = False


# ------------------------------------------------------------------
# Image LSB
# ------------------------------------------------------------------
def hide_message_in_image(
    image_path: str,
    message: bytes,
    technique: str,
    output_path: Optional[str] = None,
) -> str:
    if technique.lower() == "lsb":
        return lsb_embed_image(image_path, message, output_path)
    raise ValueError(f"Unsupported image technique: {technique}")


def extract_message_from_image(image_path: str, technique: str) -> bytes:
    if technique.lower() == "lsb":
        return lsb_extract_image(image_path)
    raise ValueError(f"Unsupported image technique: {technique}")


def lsb_embed_image(
    image_path: str,
    message: bytes,
    output_path: Optional[str] = None,
) -> str:
    img = Image.open(image_path)
    if img.mode not in {"RGB", "RGBA"}:
        img = img.convert("RGBA")  # Ensure RGBA if not already

    data = message.encode() if isinstance(message, str) else message
    binary_message = "".join(f"{byte:08b}" for byte in data)
    binary_message += "1" * 16  # 16-bit delimiter

    pixels = img.load()
    width, height = img.size
    idx = 0

    for y in range(height):
        for x in range(width):
            if idx >= len(binary_message):
                break
            r, g, b, a = pixels[x, y]  # Now includes alpha
            r = (r & ~1) | int(binary_message[idx])
            idx += 1
            if idx < len(binary_message):
                g = (g & ~1) | int(binary_message[idx])
                idx += 1
            if idx < len(binary_message):
                b = (b & ~1) | int(binary_message[idx])
                idx += 1
            if idx < len(binary_message) and img.mode == "RGBA":
                a = (a & ~1) | int(binary_message[idx])  # Use alpha if available
                idx += 1
            pixels[x, y] = (r, g, b, a) if img.mode == "RGBA" else (r, g, b)
        else:
            continue
        break

    if idx < len(binary_message):
        raise ValueError("Image too small for LSB payload")

    if output_path is None:
        output_path = "embedded_" + os.path.basename(image_path)
    img.save(output_path)  # Preserves RGBA if original was RGBA
    return output_path


def lsb_extract_image(image_path: str) -> bytes:
    img = Image.open(image_path)
    if img.mode not in {"RGB", "RGBA"}:
        img = img.convert("RGBA")

    pixels = img.load()
    width, height = img.size
    bits = []

    for y in range(height):
        for x in range(width):
            if img.mode == "RGBA":
                r, g, b, a = pixels[x, y]
                bits.extend([r & 1, g & 1, b & 1, a & 1])  # Include alpha
            else:
                r, g, b = pixels[x, y]
                bits.extend([r & 1, g & 1, b & 1])

    bit_str = "".join(map(str, bits))
    delim = bit_str.find("1" * 16)
    if delim == -1:
        return b""

    bit_str = bit_str[:delim]
    if len(bit_str) % 8:
        bit_str = bit_str[: -(len(bit_str) % 8)]

    return bytes(int(bit_str[i : i + 8], 2) for i in range(0, len(bit_str), 8))


# ------------------------------------------------------------------
# Audio Part
# ------------------------------------------------------------------


def _load_audio_any(path: str) -> Tuple[np.ndarray, int]:
    """
    Return (samples, samplerate) as float32 mono array.
    Uses pydub if the file is MP3/M4A; otherwise soundfile.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    ext = os.path.splitext(path)[1].lower()
    if ext in {".mp3", ".m4a", ".aac"}:
        if not _HAS_PYDUB:
            raise RuntimeError("pydub/ffmpeg required for MP3/M4A support")
        seg = AudioSegment.from_file(path)
        seg = seg.set_channels(1)  # mono
        samples = np.array(seg.get_array_of_samples(), dtype=np.float32) / (2**15)
        return samples, seg.frame_rate
    else:
        samples, sr = sf.read(path, dtype="float32")
        if samples.ndim == 2:
            samples = samples.mean(axis=1)  # stereo → mono
        return samples, sr


def _save_audio_any(path: str, samples: np.ndarray, sr: int) -> None:
    """Write samples (float32) to WAV via soundfile."""
    sf.write(path, samples, sr, subtype="PCM_16")


# -----------------------------------------------------------
# Audio LSB helpers (16-bit mono PCM samples)
# -----------------------------------------------------------
def _lsb_embed(samples: np.ndarray, message: bytes) -> np.ndarray:
    """
    samples : float32 mono array (‐1 … 1)
    returns : float32 array with LSB-embedded message
    """
    # Convert to int16
    int16 = (np.clip(samples, -1.0, 1.0) * 32767).astype(np.int16)

    # Bit stream
    bit_stream = "".join(f"{b:08b}" for b in message) + "1" * 16  # delimiter
    if len(bit_stream) > len(int16):
        raise ValueError("Audio too short for LSB payload")

    # Embed
    for i, bit in enumerate(bit_stream):
        int16[i] = (int16[i] & ~1) | int(bit)

    # Back to float32
    return int16.astype(np.float32) / 32768.0


def _lsb_extract(samples: np.ndarray) -> bytes:
    """
    samples : float32 mono array
    returns : bytes
    """
    int16 = (np.clip(samples, -1.0, 1.0) * 32767).astype(np.int16)
    bits = "".join(str(v & 1) for v in int16)

    delim = bits.find("1" * 16)
    if delim == -1:
        return b""

    bits = bits[:delim]
    if len(bits) % 8:
        bits = bits[: -(len(bits) % 8)]

    return bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))


# ---------- Echo-Hiding -----------------------------------------
def _echo_embed(
    samples: np.ndarray,
    sr: int,
    message: bytes,
    echo_amp: float = 0.2,
    delay_ms: float = 30,
) -> np.ndarray:
    delay = int(sr * delay_ms / 1000)
    echo = np.zeros_like(samples)
    echo[delay:] = echo_amp * samples[:-delay]

    bit_stream = "".join(f"{b:08b}" for b in message) + "1" * 8
    block_size = len(samples) // len(bit_stream)
    if block_size == 0:
        raise ValueError("Audio too short for EchoHiding")

    stego = samples.copy()
    for i, bit in enumerate(bit_stream):
        start = i * block_size
        end = min((i + 1) * block_size, len(stego))
        if bit == "1":
            stego[start:end] += echo[start:end]
    return stego


def _echo_extract(
    samples: np.ndarray, sr: int, echo_amp: float = 0.2, delay_ms: float = 30
) -> bytes:
    delay = int(sr * delay_ms / 1000)
    if delay == 0:
        return b""

    # auto-correlation around the expected delay
    corr = fftconvolve(samples, samples[::-1], mode="full")
    mid = len(samples) - 1
    peak = corr[mid + delay] / corr[mid]

    # crude threshold – tune in practice
    bit = "1" if peak > 0.5 else "0"
    return bytes([int(bit, 2)])


# ---------- Phase-Coding (flip sign of middle phase bin) ----------
def _phase_embed(samples: np.ndarray, sr: int, message: bytes) -> np.ndarray:
    bit_stream = "".join(f"{b:08b}" for b in message) + "1" * 8
    block_size = 2 ** int(np.log2(len(samples) // len(bit_stream)))
    if block_size < 32:
        raise ValueError("Audio too short for PhaseCoding")

    stego = samples.copy()
    for i, bit in enumerate(bit_stream):
        start = i * block_size
        end = start + block_size
        if end > len(stego):
            break
        block = stego[start:end]
        dft = np.fft.rfft(block)
        mid = len(dft) // 2
        if bit == "1":
            dft[mid] = -dft[mid]  # flip phase
        stego[start:end] = np.fft.irfft(dft, n=block_size)
    return stego


def _phase_extract(samples: np.ndarray, sr: int) -> bytes:
    bit_stream = ""
    block_size = 2 ** int(np.log2(len(samples)))
    while len(samples) >= block_size:
        block = samples[:block_size]
        dft = np.fft.rfft(block)
        mid = len(dft) // 2
        bit_stream += "1" if np.signbit(np.real(dft[mid])) else "0"
        samples = samples[block_size:]
    delim = bit_stream.find("1" * 8)
    if delim == -1:
        return b""
    bits = bit_stream[:delim]
    return bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))


# ---------- Public wrappers --------------------------------------
def hide_message_in_audio(
    audio_path: str,
    message: bytes,
    technique: str,
    output_path: Optional[str] = None,
) -> str:
    samples, sr = _load_audio_any(audio_path)  # helper from previous answer
    if technique.lower() == "lsb":
        stego = _lsb_embed(samples, message)  # already implemented
    elif technique.lower() == "echohiding":
        stego = _echo_embed(samples, sr, message)
    elif technique.lower() == "phasecoding":
        stego = _phase_embed(samples, sr, message)
    else:
        raise NotImplementedError(f"Audio technique '{technique}' not implemented.")

    if output_path is None:
        output_path = (
            "embedded_" + os.path.splitext(os.path.basename(audio_path))[0] + ".wav"
        )
    _save_audio_any(output_path, stego, sr)
    return output_path


def extract_message_from_audio(audio_path: str, technique: str) -> bytes:
    samples, sr = _load_audio_any(audio_path)
    if technique.lower() == "lsb":
        return _lsb_extract(samples)
    elif technique.lower() == "echohiding":
        return _echo_extract(samples, sr)
    elif technique.lower() == "phasecoding":
        return _phase_extract(samples, sr)
    else:
        raise NotImplementedError(f"Audio technique '{technique}' not implemented.")


# ------------------------ Video LSB helpers ---------------------------- #
def _video_lsb_embed(
    frames: list[np.ndarray],
    message: bytes,
) -> list[np.ndarray]:
    """Embed message into the LSB of the first frame(s)."""
    data = message.encode() if isinstance(message, str) else message
    bit_str = "".join(f"{b:08b}" for b in data) + "1" * 16
    bits = [int(b) for b in bit_str]

    out_frames = []
    idx = 0
    for frm in frames:
        if idx >= len(bits):
            out_frames.append(frm)
            continue

        # flatten first channel of first frame
        flat = frm[:, :, 0].ravel()
        for i in range(min(len(bits) - idx, flat.size)):
            flat[i] = (flat[i] & ~1) | bits[idx + i]
        idx += flat.size

        # put modified pixels back
        frm[:, :, 0] = flat.reshape(frm.shape[:2])
        out_frames.append(frm)

    if idx < len(bits):
        raise ValueError("Video too short for LSB payload")
    return out_frames


def _video_lsb_extract(frames: list[np.ndarray]) -> bytes:
    """Extract LSB bits from the first sufficient frames."""
    bits = []
    for frm in frames:
        bits.extend(frm[:, :, 0].ravel() & 1)
        # stop early if we already have enough
        bit_str = "".join(map(str, bits))
        delim = bit_str.find("1" * 16)
        if delim != -1:
            break
    else:
        return b""

    bit_str = bit_str[:delim]
    if len(bit_str) % 8:
        bit_str = bit_str[: -(len(bit_str) % 8)]
    return bytes(int(bit_str[i : i + 8], 2) for i in range(0, len(bit_str), 8))


# ------------------------ Motion-Vector helpers ------------------------ #
def _video_mv_embed(
    cap: cv2.VideoCapture,
    message: bytes,
) -> list[np.ndarray]:
    """Very small demo: encode one bit per frame by flipping the sign
    of the first motion-vector’s x-component."""
    data = message.encode() if isinstance(message, str) else message
    bit_str = "".join(f"{b:08b}" for b in data) + "1" * 8
    bits = [int(b) for b in bit_str]

    frames = []
    ret, prev = cap.read()
    if not ret:
        raise ValueError("Empty video")

    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(prev)
    hsv[..., 1] = 255

    for bit in bits:
        ret, frame = cap.read()
        if not ret:
            raise ValueError("Video too short for MotionVector payload")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowPyrLK(prev_gray, gray, None, None, winSize=(15, 15))[
            0
        ]

        if flow is not None and len(flow) > 0:
            # flip sign of first vector’s x component to encode bit
            flow[0][0][0] = abs(flow[0][0][0]) * (1 if bit else -1)

        frames.append(frame)
        prev_gray = gray

    # copy remaining frames unchanged
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames


def _video_mv_extract(cap: cv2.VideoCapture) -> bytes:
    """Decode one bit per frame from the sign of the first motion-vector."""
    bits = []
    ret, prev = cap.read()
    if not ret:
        return b""

    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowPyrLK(prev_gray, gray, None, None, winSize=(15, 15))[
            0
        ]
        bit = 0
        if flow is not None and len(flow) > 0 and flow[0][0][0] >= 0:
            bit = 1
        bits.append(bit)
        prev_gray = gray

    bit_str = "".join(map(str, bits))
    delim = bit_str.find("1" * 8)
    if delim == -1:
        return b""
    return bytes(int(bit_str[:delim], 2))


# ------------------------ Public video wrappers ------------------------ #
def hide_message_in_video(
    video_path: str,
    message: bytes,
    technique: str,
    output_path: Optional[str] = None,
) -> str:
    if technique.lower() == "lsb":
        op = _video_lsb_embed
    elif technique.lower() == "motionvector":
        op = _video_mv_embed
    else:
        raise NotImplementedError(f"Video technique '{technique}' not implemented.")

    if output_path is None:
        base = os.path.splitext(os.path.basename(video_path))[0]
        output_path = f"embedded_{base}.mp4"

    # 1. load frames (moviepy)
    clip = VideoFileClip(video_path)
    frames = [cv2.cvtColor(np.array(f), cv2.COLOR_RGB2BGR) for f in clip.iter_frames()]

    # 2. embed
    if technique.lower() == "lsb":
        new_frames = op(frames, message)
    else:
        cap = cv2.VideoCapture(video_path)
        new_frames = op(cap, message)
        cap.release()

    # 3. save new video
    height, width, _ = new_frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, clip.fps, (width, height))
    for frm in new_frames:
        out.write(frm)
    out.release()

    # copy audio back (moviepy keeps it easy)
    if clip.audio:
        final = VideoFileClip(output_path).set_audio(clip.audio)
        final.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path


def extract_message_from_video(video_path: str, technique: str) -> bytes:
    if technique.lower() == "lsb":
        clip = VideoFileClip(video_path)
        frames = [
            cv2.cvtColor(np.array(f), cv2.COLOR_RGB2BGR) for f in clip.iter_frames()
        ]
        return _video_lsb_extract(frames)
    elif technique.lower() == "motionvector":
        cap = cv2.VideoCapture(video_path)
        data = _video_mv_extract(cap)
        cap.release()
        return data
    else:
        raise NotImplementedError(f"Video technique '{technique}' not implemented.")
