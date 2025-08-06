import numpy as np
import os
from PIL import Image
from typing import Optional, Tuple
import cv2
from moviepy import ImageSequenceClip, VideoFileClip
import soundfile as sf
from scipy.signal import fftconvolve

try:
    from pydub import AudioSegment

    # Check for FFMPEG_PATH environment variable
    if "FFMPEG_PATH" in os.environ:
        AudioSegment.converter = os.environ["FFMPEG_PATH"]
    _HAS_PYDUB = True
except ImportError:
    _HAS_PYDUB = False


# Magic number to identify our steganographic data
STEGO_MAGIC = b"INSCRYPT_STEGO"


# Image LSB
def hide_message_in_image(
    image_path: str, message: bytes, technique: str, output_path: Optional[str] = None
) -> str:
    if technique.lower() == "lsb":
        return lsb_embed_image(image_path, message, output_path)
    raise ValueError(f"Unsupported image technique: {technique}")


def extract_message_from_image(image_path: str, technique: str) -> bytes:
    if technique.lower() == "lsb":
        return lsb_extract_image(image_path)
    raise ValueError(f"Unsupported image technique: {technique}")


def lsb_embed_image(
    image_path: str, message: bytes, output_path: Optional[str] = None
) -> str:
    img = Image.open(image_path)
    if img.mode not in {"RGB", "RGBA"}:
        img = img.convert("RGBA")

    message_to_embed = STEGO_MAGIC + message
    # Prepend message length to the message
    message_len_bytes = len(message_to_embed).to_bytes(4, "big")
    binary_message = "".join(
        f"{byte:08b}" for byte in message_len_bytes + message_to_embed
    )

    pixels = img.load()
    width, height = img.size
    idx = 0

    for y in range(height):
        for x in range(width):
            if idx >= len(binary_message):
                break
            if img.mode == "RGBA":
                r, g, b, a = pixels[x, y]
            else:
                r, g, b = pixels[x, y]

            if idx < len(binary_message):
                r = (r & ~1) | int(binary_message[idx])
                idx += 1
            if idx < len(binary_message):
                g = (g & ~1) | int(binary_message[idx])
                idx += 1
            if idx < len(binary_message):
                b = (b & ~1) | int(binary_message[idx])
                idx += 1
            if idx < len(binary_message) and img.mode == "RGBA":
                a = (a & ~1) | int(binary_message[idx])
                idx += 1

            pixels[x, y] = (r, g, b, a) if img.mode == "RGBA" else (r, g, b)
        else:
            continue
        break

    if idx < len(binary_message):
        raise ValueError("Image too small for LSB payload")

    if output_path is None:
        output_path = "embedded_" + os.path.basename(image_path)
    # Ensure output is PNG to prevent lossy compression issues
    base, _ = os.path.splitext(output_path)
    output_path = base + ".png"

    img.save(output_path, "PNG")
    return output_path


def lsb_extract_image(image_path: str) -> bytes:
    img = Image.open(image_path)
    if img.mode not in {"RGB", "RGBA"}:
        img = img.convert("RGBA")

    pixels = img.load()
    width, height = img.size

    bit_iterator = iter(
        (pixel_val & 1)
        for y in range(height)
        for x in range(width)
        for pixel_val in pixels[x, y]
    )

    def read_bits(n):
        # Helper to read n bits from the iterator
        return "".join(str(next(bit_iterator)) for _ in range(n))

    try:
        # Read the 32-bit length prefix
        len_bits = read_bits(32)
        message_len = int(len_bits, 2)

        # Sanity check the message length
        max_len = (width * height * len(img.getbands()) - 32) // 8
        if not (0 < message_len <= max_len):
            return b""  # Invalid length, not a stego image

        # Read the message itself
        message_bits = read_bits(message_len * 8)

        # Convert bit string to bytes
        extracted_bytes = bytes(
            int(message_bits[i : i + 8], 2) for i in range(0, len(message_bits), 8)
        )

        # Check for magic number
        if extracted_bytes.startswith(STEGO_MAGIC):
            return extracted_bytes[len(STEGO_MAGIC) :]
        else:
            return b""  # Not a valid stego file

    except (StopIteration, ValueError):
        # If image ends prematurely or bits are not valid int
        return b""


# Audio Part
def _load_audio_any(path: str) -> Tuple[np.ndarray, int]:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    ext = os.path.splitext(path)[1].lower()
    if ext in {".mp3", ".m4a", ".aac"}:
        if not _HAS_PYDUB:
            raise RuntimeError("pydub/ffmpeg required for MP3/M4A support")
        seg = AudioSegment.from_file(path)
        seg = seg.set_channels(1)
        samples = np.array(seg.get_array_of_samples(), dtype=np.float32) / (2**15)
        return samples, seg.frame_rate
    else:
        samples, sr = sf.read(path, dtype="float32")
        if samples.ndim == 2:
            samples = samples.mean(axis=1)
        return samples, sr


def _save_audio_any(path: str, samples: np.ndarray, sr: int) -> None:
    sf.write(path, samples, sr, subtype="PCM_16")


# Audio LSB helpers
def _lsb_embed(samples: np.ndarray, message: bytes) -> np.ndarray:
    """Embeds message into LSB of int16 samples and returns int16 samples."""
    if not np.issubdtype(samples.dtype, np.floating):
        raise TypeError("Input samples for LSB embedding must be float.")

    int16_samples = (np.clip(samples, -1.0, 1.0) * 32767).astype(np.int16)

    message_to_embed = STEGO_MAGIC + message
    message_len_bytes = len(message_to_embed).to_bytes(4, "big")
    bit_stream = "".join(f"{b:08b}" for b in message_len_bytes + message_to_embed)

    if len(bit_stream) > len(int16_samples):
        raise ValueError("Audio too short for LSB payload")

    for i, bit in enumerate(bit_stream):
        int16_samples[i] = (int16_samples[i] & ~1) | int(bit)

    return int16_samples


def _lsb_extract(samples: np.ndarray) -> bytes:
    if not np.issubdtype(samples.dtype, np.floating):
        raise TypeError("Input samples for LSB extraction must be float.")

    # Scale float samples in [-1.0, 1.0) to int16 range [-32768, 32767]
    # soundfile normalizes by 32768, so we multiply to reverse it.
    int16_samples = (samples * 32768.0).astype(np.int16)

    # Extract length (32 bits)
    if len(int16_samples) < 32:
        return b""
    len_bits = "".join(str(v & 1) for v in int16_samples[:32])
    try:
        message_len = int(len_bits, 2)
    except ValueError:
        return b""  # Not a valid binary number

    # Sanity check
    max_len = (len(int16_samples) - 32) // 8
    if not (0 < message_len <= max_len):
        return b""

    # Extract message
    total_bits_to_extract = message_len * 8
    if len(int16_samples) < 32 + total_bits_to_extract:
        return b""

    bits = "".join(str(v & 1) for v in int16_samples[32 : 32 + total_bits_to_extract])
    extracted_bytes = bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))

    if extracted_bytes.startswith(STEGO_MAGIC):
        return extracted_bytes[len(STEGO_MAGIC) :]
    else:
        return b""


# Echo-Hiding
def _echo_embed(
    samples: np.ndarray,
    sr: int,
    message: bytes,
    delay0_ms: float = 20,
    delay1_ms: float = 30,
    echo_amp: float = 0.2,
) -> np.ndarray:
    delay0 = int(sr * delay0_ms / 1000)
    delay1 = int(sr * delay1_ms / 1000)

    message_to_embed = STEGO_MAGIC + message
    message_len_bytes = len(message_to_embed).to_bytes(4, "big")
    bit_stream = "".join(f"{b:08b}" for b in message_len_bytes + message_to_embed)

    block_size = max(delay0, delay1) * 4  # Ensure block is large enough for cepstrum
    if len(bit_stream) * block_size > len(samples):
        raise ValueError("Audio too short for EchoHiding payload")

    stego = samples.copy()
    for i, bit in enumerate(bit_stream):
        start = i * block_size
        end = start + block_size
        if end > len(stego):
            break

        delay = delay1 if bit == "1" else delay0
        echo = np.zeros(block_size)
        echo[delay:] = echo_amp * stego[start : end - delay]
        stego[start:end] += echo

    return stego


def _echo_extract(
    samples: np.ndarray, sr: int, delay0_ms: float = 20, delay1_ms: float = 30
) -> bytes:
    delay0 = int(sr * delay0_ms / 1000)
    delay1 = int(sr * delay1_ms / 1000)
    block_size = max(delay0, delay1) * 4

    bits = []
    num_blocks = len(samples) // block_size

    for i in range(num_blocks):
        start = i * block_size
        end = start + block_size
        block = samples[start:end]

        # Cepstrum to find echo
        ceps = np.fft.ifft(np.log(np.abs(np.fft.fft(block)) + 1e-9)).real

        peak0 = np.max(ceps[delay0 - 2 : delay0 + 3])
        peak1 = np.max(ceps[delay1 - 2 : delay1 + 3])

        if peak1 > peak0:
            bits.append("1")
        else:
            bits.append("0")

    bit_stream = "".join(bits)

    if len(bit_stream) < 32:
        return b""
    len_bits = bit_stream[:32]
    try:
        message_len = int(len_bits, 2)
    except ValueError:
        return b""

    max_len = (len(bit_stream) - 32) // 8
    if not (0 < message_len <= max_len):
        return b""

    total_bits_to_extract = message_len * 8
    if len(bit_stream) < 32 + total_bits_to_extract:
        return b""

    message_bits = bit_stream[32 : 32 + total_bits_to_extract]
    extracted_bytes = bytes(
        int(message_bits[i : i + 8], 2) for i in range(0, len(message_bits), 8)
    )

    if extracted_bytes.startswith(STEGO_MAGIC):
        return extracted_bytes[len(STEGO_MAGIC) :]
    else:
        return b""


def _phase_embed(samples: np.ndarray, sr: int, message: bytes) -> np.ndarray:
    message_to_embed = STEGO_MAGIC + message
    message_len_bytes = len(message_to_embed).to_bytes(4, "big")
    bit_stream = "".join(f"{b:08b}" for b in message_len_bytes + message_to_embed)

    block_size = 2048  # Fixed block size
    if len(bit_stream) * block_size > len(samples):
        raise ValueError("Audio too short for PhaseCoding payload")

    stego = samples.copy()
    for i, bit in enumerate(bit_stream):
        start = i * block_size
        end = start + block_size
        if end > len(stego):
            break

        block = stego[start:end]
        dft = np.fft.rfft(block)

        # Modify phase of a mid-range frequency component
        freq_idx_to_modify = len(dft) // 4

        if bit == "1":
            dft[freq_idx_to_modify] = np.abs(dft[freq_idx_to_modify]) * np.exp(
                1j * np.pi / 2
            )
        else:
            dft[freq_idx_to_modify] = np.abs(dft[freq_idx_to_modify]) * np.exp(
                -1j * np.pi / 2
            )

        stego[start:end] = np.fft.irfft(dft, n=block_size)

    return stego


def _phase_extract(samples: np.ndarray, sr: int) -> bytes:
    block_size = 2048
    bits = []
    num_blocks = len(samples) // block_size

    for i in range(num_blocks):
        start = i * block_size
        end = start + block_size
        block = samples[start:end]
        dft = np.fft.rfft(block)

        freq_idx_to_check = len(dft) // 4
        angle = np.angle(dft[freq_idx_to_check])

        if angle > 0:
            bits.append("1")
        else:
            bits.append("0")

    bit_stream = "".join(bits)

    if len(bit_stream) < 32:
        return b""
    len_bits = bit_stream[:32]
    try:
        message_len = int(len_bits, 2)
    except ValueError:
        return b""

    max_len = (len(bit_stream) - 32) // 8
    if not (0 < message_len <= max_len):
        return b""

    total_bits_to_extract = message_len * 8
    if len(bit_stream) < 32 + total_bits_to_extract:
        return b""

    message_bits = bit_stream[32 : 32 + total_bits_to_extract]
    extracted_bytes = bytes(
        int(message_bits[i : i + 8], 2) for i in range(0, len(message_bits), 8)
    )

    if extracted_bytes.startswith(STEGO_MAGIC):
        return extracted_bytes[len(STEGO_MAGIC) :]
    else:
        return b""


# Public audio wrappers
def hide_message_in_audio(
    audio_path: str, message: bytes, technique: str, output_path: Optional[str] = None
) -> str:
    samples, sr = _load_audio_any(audio_path)
    if technique.lower() == "lsb":
        stego_int16 = _lsb_embed(samples, message)
        # Convert back to float for saving
        stego = stego_int16.astype(np.float32) / 32768.0
    elif technique.lower() == "echohiding":
        stego = _echo_embed(samples, sr, message)
    elif technique.lower() == "phasecoding":
        stego = _phase_embed(samples, sr, message)
    else:
        raise NotImplementedError(f"Audio technique '{technique}' not implemented.")

    if stego.shape[0] < samples.shape[0]:
        stego = np.pad(stego, (0, samples.shape[0] - stego.shape[0]))

    tmp_dir = "/tmp/"

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    if output_path is None:
        output_path = (
            tmp_dir
            + "embedded_"
            + os.path.splitext(os.path.basename(audio_path))[0]
            + ".wav"
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


# Video LSB helpers
def _video_lsb_embed(frames: list[np.ndarray], message: bytes) -> list[np.ndarray]:
    if not frames:
        raise ValueError("Input frame list is empty.")
    message_to_embed = STEGO_MAGIC + message
    message_len_bytes = len(message_to_embed).to_bytes(8, "big")
    bit_stream = "".join(f"{byte:08b}" for byte in message_len_bytes + message_to_embed)

    bits_to_embed = np.array([int(b) for b in bit_stream], dtype=np.uint8)
    num_bits_to_embed = len(bits_to_embed)

    total_pixels = sum(frame.size for frame in frames)
    if num_bits_to_embed > total_pixels:
        raise ValueError("Video too short for LSB payload")

    out_frames = []
    bit_idx = 0
    for frame in frames:
        if bit_idx >= num_bits_to_embed:
            out_frames.append(frame)
            continue

        frame_copy = frame.copy()
        flat_frame = frame_copy.ravel()

        embed_len = min(len(flat_frame), num_bits_to_embed - bit_idx)
        flat_frame[:embed_len] = (flat_frame[:embed_len] & 0xFE) | bits_to_embed[
            bit_idx : bit_idx + embed_len
        ]
        bit_idx += embed_len

        out_frames.append(frame_copy)

    return out_frames


def _video_lsb_extract(frames: list[np.ndarray]) -> bytes:
    if not frames:
        return b""

    # Create a generator that yields the LSB of each pixel value sequentially
    pixel_iterator = (p & 1 for frame in frames for p in frame.ravel())

    def read_bits(n):
        bits = []
        try:
            for _ in range(n):
                bits.append(str(next(pixel_iterator)))
        except StopIteration:
            return None  # Not enough bits in the video
        return "".join(bits)

    # 1. Read the 8-byte (64-bit) length prefix
    len_bits_str = read_bits(64)
    if len_bits_str is None:
        return b""

    try:
        message_len = int(len_bits_str, 2)
    except ValueError:
        return b""  # Invalid binary format for length

    # 2. Sanity-check the message length against the total available pixels
    total_pixels = sum(f.size for f in frames)
    max_len = (total_pixels - 64) // 8
    if not (0 < message_len <= max_len):
        return b""  # Length is unreasonable

    # 3. Read the message itself
    message_bits_str = read_bits(message_len * 8)
    if message_bits_str is None:
        return b""  # Video ended before the full message could be read

    # 4. Convert the bit string to bytes
    try:
        extracted_bytes = bytes(
            int(message_bits_str[i : i + 8], 2)
            for i in range(0, len(message_bits_str), 8)
        )
    except ValueError:
        return b""  # Invalid binary format for message bytes

    # 5. Check for the magic number and return the payload
    if extracted_bytes.startswith(STEGO_MAGIC):
        return extracted_bytes[len(STEGO_MAGIC) :]

    return b""




# Motion-Vector helpers
def _video_mv_embed(cap: cv2.VideoCapture, message: bytes) -> list[np.ndarray]:
    bit_str = "".join(f"{b:08b}" for b in message) + "1" * 8
    bits_to_embed = [int(b) for b in bit_str]

    frames = []
    ret, prev = cap.read()
    if not ret:
        raise ValueError("Empty video")

    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

    lk_params = dict(
        winSize=(15, 15),
        maxLevel=2,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
    )

    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

        if p0 is not None and len(p0) > 0:
            p1, st, err = cv2.calcOpticalFlowPyrLK(
                prev_gray, gray, p0, None, **lk_params
            )

            if p1 is not None and st is not None:
                good_new = p1[st == 1]
                if len(good_new) > 0 and idx < len(bits_to_embed):
                    idx += 1

        frames.append(frame)
        prev_gray = gray

    if idx < len(bits_to_embed):
        raise ValueError("Video too short for MotionVector payload")
    return frames


def _video_mv_extract(cap: cv2.VideoCapture) -> bytes:
    bits = []
    ret, prev = cap.read()
    if not ret:
        return b""

    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

    lk_params = dict(
        winSize=(15, 15),
        maxLevel=2,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

        if p0 is not None and len(p0) > 0:
            p1, st, err = cv2.calcOpticalFlowPyrLK(
                prev_gray, gray, p0, None, **lk_params
            )

            if p1 is not None and st is not None:
                good_new = p1[st == 1]
                if len(good_new) > 0:
                    if good_new[0, 0, 0] >= 0:
                        bits.append(1)
                    else:
                        bits.append(0)

        prev_gray = gray

    bit_str = "".join(map(str, bits))
    delim = bit_str.find("1" * 8)
    if delim == -1:
        return b""
    message_bits_str = bit_str[:delim]
    if len(message_bits_str) % 8:
        message_bits_str = message_bits_str[: -(len(message_bits_str) % 8)]
    return bytes(
        int(message_bits_str[i : i + 8], 2) for i in range(0, len(message_bits_str), 8)
    )


# Public video wrappers
def hide_message_in_video(
    video_path: str, message: bytes, technique: str, output_path: Optional[str] = None
) -> str:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file.")

    original_clip = None
    final_clip = None
    try:
        if technique.lower() == "lsb":
            fps = cap.get(cv2.CAP_PROP_FPS)
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if not frames:
                raise ValueError("Could not read any frames from the video.")

            new_frames = _video_lsb_embed(frames, message)

            if output_path is None:
                base = os.path.splitext(os.path.basename(video_path))[0]
                output_path = f"/tmp/embedded_{base}.mp4"

            final_clip = ImageSequenceClip(new_frames, fps=fps)

            original_clip = VideoFileClip(video_path)
            if original_clip.audio:
                final_clip.audio = original_clip.audio

            final_clip.write_videofile(
                output_path, codec="libx264", audio_codec="aac", logger=None
            )
            return output_path

        elif technique.lower() == "motionvector":
            fps = cap.get(cv2.CAP_PROP_FPS)
            new_frames_bgr = _video_mv_embed(cap, message)
            new_frames_rgb = [
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in new_frames_bgr
            ]

            if output_path is None:
                base = os.path.splitext(os.path.basename(video_path))[0]
                output_path = f"/tmp/embedded_{base}.mp4"
            final_clip = ImageSequenceClip(new_frames_rgb, fps=fps)
            original_clip = VideoFileClip(video_path)
            if original_clip.audio:
                final_clip.audio = original_clip.audio
            final_clip.write_videofile(
                output_path, codec="libx264", audio_codec="aac", logger=None
            )
            return output_path
        else:
            raise NotImplementedError(f"Video technique '{technique}' not implemented.")
    finally:
        cap.release()
        if original_clip:
            original_clip.close()
        if final_clip:
            final_clip.close()


def extract_message_from_video(video_path: str, technique: str) -> bytes:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file.")
    try:
        if technique.lower() == "lsb":
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if not frames:
                return b""
            return _video_lsb_extract(frames)
        elif technique.lower() == "motionvector":
            return _video_mv_extract(cap)
        else:
            raise NotImplementedError(f"Video technique '{technique}' not implemented.")
    finally:
        if cap.isOpened():
            cap.release()
