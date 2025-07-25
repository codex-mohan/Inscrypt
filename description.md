# Project Description: Inscrypt

## Goal
The primary goal of the Inscrypt project is to develop a comprehensive steganographic system capable of encrypting secret messages and embedding them within digital media files. It also provides secure extraction and decryption capabilities to recover the original hidden information.

## Key Features and Requirements:

### Encryption and Hiding Mechanism
- Develop methods to encrypt messages (text or image data) and embed this encrypted data within images.
- Support various encryption algorithms (e.g., AES, DES, DES3, ChaCha20, Blowfish, ARC2, ARC4, Salsa20, blockalgo, CAST, PKCS1_OAEP, PKCS1_v1_5, XOR).
- Implement diverse steganographic techniques, with LSB as a common suggestion, but encouraging exploration of others.
- Accommodate various key handling scenarios.

### Decryption and Extraction Mechanism
- Implement a robust system for decrypting previously encrypted data and extracting hidden messages from images, given the necessary keys.
- The system should hide the encryption type and steganographic method used within the image itself.

### Robustness and Undetectability
- Prioritize resilience against detection and compromise, aiming for the highest possible undetectability.

### Algorithm Versatility
- Maximize support for a wide array of encryption algorithms and steganographic techniques.
- Allow for multiple encryption layers (e.g., (AES, blowfish, AES)).
- Utilize various image, video, and audio steganographic techniques.

### Data Obfuscation
- Include several types of data that can be obfuscated, such as:
    - Volume inside video frames in video files.
    - Executables in file images, audio, and videos.
    - Secret encrypted messages.
    - Hiding hidden audio messages using Fourier transforms inside normal audio files.

### Media Format Compatibility
- Expand support for various image formats and potentially other media types (e.g., audio, video).

### Automated Key and Media Preparation
- Design the solution to minimize user input by automating key generation and media file preparation for embedding.
- Provide simple and advanced option menus for user choice.
- Include detailed information on the application's safety.

## Project Structure:
The project is a monorepo (turbo repo) featuring:
- **Backend:** A FastAPI Python server.
- **Frontend:** A Next.js based frontend.

## Frontend Technologies:
- Next.js
- ShadCN UI
- React-Icons (instead of Lucide React)
- Tailwind CSS v4
- Framer Motion (for smooth animations across UI components)

## Backend API:
- API routes should be placed in a `routes` folder with proper naming conventions.
- API versioning (e.g., `v1`, `v2`) should be followed for future endpoint management, starting with `v1`.

## Hashing Methods:
- Include the following hashing methods, properly mentioned on their respective pages:
    - `keccak, SHA1, SHA224, SHA256, SHA384, SHA512, SHA3_224, SHA3_256, SHA3_384, SHA3_512, TupleHash128, TupleHash256, SHAKE128, SHAKE256, cSHAKE128, cSHAKE256, KangarooTwelve, Whirlpool, blake`.

## Recommended Libraries:
- **Python:** `pycryptodome`, `pillow`, `numpy`, `opencv-python`, `cryptography`, `librosa`, `pydub`, `matplotlib`, `pathlib`, `scipy`, `moviepy`, `soundfile`, `fastapi`.
- **JavaScript/TypeScript:** `NextJS`, `shadcn UI`, `tailwind css`, `react-icons`, `framer-motion`.

## Dataset:
The provided dataset includes "cover" files for steganography operations:
- **Images (PNG):** 10 sample PNG images.
- **Audio (MP3):** 5 sample MP3 audio files.
- **Video (MP4):** 5 sample MP4 video files.
These files will serve as carriers for encrypted secret messages.