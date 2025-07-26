from __future__ import annotations

import base64
from typing import List, Dict, Any, Tuple, Optional

from Crypto.Cipher import AES, DES, DES3, ChaCha20, Blowfish, ARC2, ARC4, Salsa20, CAST
from Crypto.Random import get_random_bytes
from Crypto.Hash import (
    SHA1,
    SHA224,
    SHA256,
    SHA384,
    SHA512,
    SHA3_224,
    SHA3_256,
    SHA3_384,
    SHA3_512,
    SHAKE128,
    SHAKE256,
    TupleHash128,
    TupleHash256,
    cSHAKE128,
    cSHAKE256,
    KangarooTwelve,
    SHA512 as Whirlpool,
    keccak,
)

# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
_HASH_MAP = {
    "keccak": keccak,
    "sha1": SHA1,
    "sha224": SHA224,
    "sha256": SHA256,
    "sha384": SHA384,
    "sha512": SHA512,
    "sha3_224": SHA3_224,
    "sha3_256": SHA3_256,
    "sha3_384": SHA3_384,
    "sha3_512": SHA3_512,
    "tuplehash128": TupleHash128,
    "tuplehash256": TupleHash256,
    "shake128": SHAKE128,
    "shake256": SHAKE256,
    "cshake128": cSHAKE128,
    "cshake256": cSHAKE256,
    "kangorootwelve": KangarooTwelve,
    "whirlpool": Whirlpool,
}


def _get_hash(name: str):
    try:
        return _HASH_MAP[name.lower()]
    except KeyError:
        raise ValueError(f"Unsupported hash: {name}")


def _kdf(key_material: bytes, hash_name: str, size: int, index: int) -> bytes:
    """Deterministically derive a key for layer *index*."""
    h = _get_hash(hash_name)
    data = key_material + str(index).encode()
    if h in {
        SHAKE128,
        SHAKE256,
        cSHAKE128,
        cSHAKE256,
        KangarooTwelve,
        TupleHash128,
        TupleHash256,
    }:
        return h.new(data=data).read(size)
    return h.new(data=data).digest()[:size]


# --------------------------------------------------------------------------- #
# Per-algorithm wrappers                                                      #
# --------------------------------------------------------------------------- #
def _encrypt_layer(
    algo: str, key: bytes, plaintext: bytes
) -> Tuple[bytes, Dict[str, bytes]]:
    """Return (ciphertext, meta-dict with nonce/tag when applicable)."""
    algo = algo.lower()

    if algo == "aes":
        cipher = AES.new(key, AES.MODE_EAX)
        ct, tag = cipher.encrypt_and_digest(plaintext)
        return ct, {"nonce": cipher.nonce, "tag": tag}

    if algo == "des":
        cipher = DES.new(key, DES.MODE_EAX)
        ct, tag = cipher.encrypt_and_digest(plaintext)
        return ct, {"nonce": cipher.nonce, "tag": tag}

    if algo == "des3":
        cipher = DES3.new(key, DES3.MODE_EAX)
        ct, tag = cipher.encrypt_and_digest(plaintext)
        return ct, {"nonce": cipher.nonce, "tag": tag}

    if algo == "blowfish":
        cipher = Blowfish.new(key, Blowfish.MODE_EAX)
        ct, tag = cipher.encrypt_and_digest(plaintext)
        return ct, {"nonce": cipher.nonce, "tag": tag}

    if algo == "arc2":
        cipher = ARC2.new(key, ARC2.MODE_EAX)
        ct, tag = cipher.encrypt_and_digest(plaintext)
        return ct, {"nonce": cipher.nonce, "tag": tag}

    if algo == "cast":
        cipher = CAST.new(key, CAST.MODE_EAX)
        ct, tag = cipher.encrypt_and_digest(plaintext)
        return ct, {"nonce": cipher.nonce, "tag": tag}

    # --- stream ciphers ---------------------------------------------------- #
    if algo == "chacha20":
        cipher = ChaCha20.new(key=key)
        return cipher.encrypt(plaintext), {"nonce": cipher.nonce}

    if algo == "salsa20":
        cipher = Salsa20.new(key=key)
        return cipher.encrypt(plaintext), {"nonce": cipher.nonce}

    if algo == "arc4":
        cipher = ARC4.new(key)
        return cipher.encrypt(plaintext), {}

    raise ValueError(f"Unsupported algorithm: {algo}")


def _decrypt_layer(
    algo: str, key: bytes, ciphertext: bytes, meta: Dict[str, bytes]
) -> bytes:
    """Inverse of _encrypt_layer."""
    algo = algo.lower()

    if algo == "aes":
        cipher = AES.new(key, AES.MODE_EAX, nonce=meta["nonce"])
        return cipher.decrypt_and_verify(ciphertext, meta["tag"])

    if algo == "des":
        cipher = DES.new(key, DES.MODE_EAX, nonce=meta["nonce"])
        return cipher.decrypt_and_verify(ciphertext, meta["tag"])

    if algo == "des3":
        cipher = DES3.new(key, DES3.MODE_EAX, nonce=meta["nonce"])
        return cipher.decrypt_and_verify(ciphertext, meta["tag"])

    if algo == "blowfish":
        cipher = Blowfish.new(key, Blowfish.MODE_EAX, nonce=meta["nonce"])
        return cipher.decrypt_and_verify(ciphertext, meta["tag"])

    if algo == "arc2":
        cipher = ARC2.new(key, ARC2.MODE_EAX, nonce=meta["nonce"])
        return cipher.decrypt_and_verify(ciphertext, meta["tag"])

    if algo == "cast":
        cipher = CAST.new(key, CAST.MODE_EAX, nonce=meta["nonce"])
        return cipher.decrypt_and_verify(ciphertext, meta["tag"])

    if algo == "chacha20":
        cipher = ChaCha20.new(key=key, nonce=meta["nonce"])
        return cipher.decrypt(ciphertext)

    if algo == "salsa20":
        cipher = Salsa20.new(key=key, nonce=meta["nonce"])
        return cipher.decrypt(ciphertext)

    if algo == "arc4":
        cipher = ARC4.new(key)
        return cipher.decrypt(ciphertext)

    raise ValueError(f"Unsupported algorithm: {algo}")


# --------------------------------------------------------------------------- #
# Public API                                                                  #
# --------------------------------------------------------------------------- #
def encrypt_data(
    data: bytes, password: str, encryption_layers: List[str], hash_name: str
) -> Dict[str, Any]:
    key_material = password.encode()
    current = data

    nonces: Dict[str, str] = {}
    tags: Dict[str, str] = {}
    meta_store: Dict[str, Dict[str, str]] = {"nonces": {}, "tags": {}}

    for idx, algo in enumerate(encryption_layers):
        key_size = {"des": 8}.get(algo.lower(), 16)  # 16 bytes default
        if algo.lower() in {"chacha20", "salsa20"}:
            key_size = 32

        key = _kdf(key_material, hash_name, key_size, idx)
        ct, meta = _encrypt_layer(algo, key, current)

        key_name = f"{algo}_{idx}"
        if "nonce" in meta:
            nonces[key_name] = base64.b64encode(meta["nonce"]).decode()
        if "tag" in meta:
            tags[key_name] = base64.b64encode(meta["tag"]).decode()

        current = ct  # feed into next layer

    return {
        "encrypted_data": base64.b64encode(current).decode(),
        "codebook": {
            "hash": hash_name,
            "layers": encryption_layers,
            "nonces": nonces,
            "tags": tags,
        },
    }


def decrypt_data(
    encrypted_data: str,
    password: str,
    hash_name: str,
    encryption_layers: Optional[List[str]] = None,
    codebook: Optional[Dict[str, Any]] = None,
) -> bytes:
    if encryption_layers is None and codebook is None:
        raise ValueError("Either encryption_layers or codebook must be supplied.")

    if encryption_layers is not None:
        # Caller supplied layer order explicitly

        print(f"encryption layers: {encryption_layers}")
        print(f"codebook: {codebook}")
        if codebook is not None:
            # Prefer the code book
            layers = codebook["layers"]
            hash_name = codebook["hash"]
            nonces_b64 = codebook["nonces"]
            tags_b64 = codebook["tags"]
    elif codebook is not None:
        # Use the stored codebook
        layers = codebook["layers"]
        hash_name = codebook["hash"]
        nonces_b64 = codebook["nonces"]
        tags_b64 = codebook["tags"]
    else:
        raise ValueError("Either encryption_layers or codebook must be supplied.")

    # Decode base64 metadata once
    nonces = {k: base64.b64decode(v) for k, v in nonces_b64.items()}
    tags = {k: base64.b64decode(v) for k, v in tags_b64.items()}

    key_material = password.encode()
    current = base64.b64decode(encrypted_data)

    # ------------------------------------------------------------------ #
    # Decrypt layers in reverse order                                    #
    # ------------------------------------------------------------------ #
    for idx, algo in reversed(list(enumerate(layers))):
        key_size = {"des": 8}.get(algo.lower(), 16)
        if algo.lower() in {"chacha20", "salsa20"}:
            key_size = 32

        key = _kdf(key_material, hash_name, key_size, idx)

        # Use unique keys per layer to avoid collisions
        key_name = f"{algo}_{idx}"
        meta: Dict[str, bytes] = {}
        if key_name in nonces:
            meta["nonce"] = nonces[key_name]
        if key_name in tags:
            meta["tag"] = tags[key_name]

        current = _decrypt_layer(algo, key, current, meta)

    return current
