# Inscrypt 🔒

[![Build Status](https://img.shields.io/travis/yourusername/your-repo.svg?style=flat-square)](https://travis-ci.com/yourusername/your-repo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![npm version](https://img.shields.io/npm/v/inscrypt.svg?style=flat-square)](https://www.npmjs.com/package/inscrypt)

## 📝 Problem Statement

Develop a comprehensive steganographic system that encrypts secret messages and embeds them within digital media files, then provides secure extraction and decryption capabilities to recover the original hidden information.

## 🎯 Project Goal

The primary goal of the Inscrypt project is to develop a comprehensive steganographic system capable of encrypting secret messages and embedding them within digital media files. It also provides secure extraction and decryption capabilities to recover the original hidden information, prioritizing robustness, undetectability, and algorithm versatility.

## ✨ Key Features

- 🔒 **Encryption & Hiding:** Encrypt messages (text/image data) and embed within images using various algorithms and steganographic techniques (e.g., LSB). Supports multiple encryption layers.
- 🔓 **Decryption & Extraction:** Robust system to decrypt data and extract hidden messages from images, including hiding the encryption type and steganographic method used.
- 🛡️ **Robustness & Undetectability:** Prioritizes resilience against detection and compromise for maximum undetectability.
- 🎛️ **Algorithm Versatility:** Supports a wide array of encryption algorithms and steganographic techniques across image, video, and audio formats.
- 🎭 **Data Obfuscation:** Obfuscates various data types, including executables, secret messages, and hidden audio messages using techniques like Fourier transforms.
- 🖼️ **Media Compatibility:** Supports various image formats and potentially other media types (audio, video).
- ⚙️ **Automation:** Automates key generation and media file preparation, with simple/advanced option menus and safety information.

## 🚀 Technologies

### Frontend

- **Framework:** Next.js
- **UI Library:** ShadCN UI
- **Icons:** React-Icons
- **Styling:** Tailwind CSS v4
- **Animations:** Framer Motion (for smooth, creative UI animations)

### Backend

- **Framework:** FastAPI (Python)
- **API Structure:** Routes organized in a `routes` folder with versioning (e.g., `v1`).

## 🔑 Encryption & Hashing Methods

### Encryption Algorithms:

AES, DES, DES3, ChaCha20, ChaCha20_Poly1305, Blowfish, ARC2, ARC4, Salsa20, blockalgo, CAST, PKCS1_OAEP, PKCS1_v1_5, XOR

### Hashing Methods:

keccak, SHA1, SHA224, SHA256, SHA384, SHA512, SHA3_224, SHA3_256, SHA3_384, SHA3_512, TupleHash128, TupleHash256, SHAKE128, SHAKE256, cSHAKE128, cSHAKE256, KangarooTwelve, Whirlpool, blake

## 📁 Project Structure

The project is structured as a monorepo using Turbo Repo, featuring:

- **Backend:** A FastAPI Python server.
- **Frontend:** A Next.js based frontend.

## 🛠️ Setup and Running Instructions

### Prerequisites

- Node.js and npm/pnpm installed.
- Python 3.x and pip installed.

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/codex-mohan/Inscrypt.git
    cd Inscrypt
    ```
2.  Install dependencies using pnpm:
    ```bash
    pnpm install
    ```

### Running the Application

To start both the frontend and backend development servers simultaneously, use Turbo Repo:

```bash
turbo run dev
```

This command will:

- Start the FastAPI backend server (likely on `http://localhost:8000` or similar).
- Start the Next.js frontend development server (likely on `http://localhost:3000`).

### Running Backend Separately

```bash
pnpm --filter inscrypt-api dev
```

### Running Frontend Separately

```bash
pnpm --filter my-v0-project dev
```

## 🤝 Contributing

Contributions are welcome! Please refer to the contributing guidelines for more information.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🧑🏻‍🤝‍🧑🏻 Team

Group No. 32: K-Means Krew

## 👨‍💻 Author

- Mohana Krishna - ID: 23BAI10630
