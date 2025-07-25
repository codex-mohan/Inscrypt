"""
Comprehensive hashing service supporting multiple algorithms
"""

import hashlib
import hmac
from typing import Optional, Dict, Any, List
from Crypto.Hash import (
    SHA3_224,
    SHA3_256,
    SHA3_384,
    SHA3_512,
    SHAKE128,
    SHAKE256,
    cSHAKE128,
    cSHAKE256,
    BLAKE2b,
    BLAKE2s,
)
from Crypto.Hash import keccak as keccak_hash
from Crypto.Hash import TupleHash128, TupleHash256
from Crypto.Hash import KangarooTwelve
from Crypto.Hash import SHA512 as Whirlpool

from app.core.exceptions import (
    HashingException,
    InvalidKeyException,
    UnsupportedAlgorithmException,
)
from .models import HashAlgorithm, HashResult, SupportedHash


class HashingService:
    """Service for handling various hashing algorithms"""

    def __init__(self):
        self.supported_algorithms = {
            HashAlgorithm.SHA1: self._hash_sha1,
            HashAlgorithm.SHA224: self._hash_sha224,
            HashAlgorithm.SHA256: self._hash_sha256,
            HashAlgorithm.SHA384: self._hash_sha384,
            HashAlgorithm.SHA512: self._hash_sha512,
            HashAlgorithm.SHA3_224: self._hash_sha3_224,
            HashAlgorithm.SHA3_256: self._hash_sha3_256,
            HashAlgorithm.SHA3_384: self._hash_sha3_384,
            HashAlgorithm.SHA3_512: self._hash_sha3_512,
            HashAlgorithm.SHAKE128: self._hash_shake128,
            HashAlgorithm.SHAKE256: self._hash_shake256,
            HashAlgorithm.CSHAKE128: self._hash_cshake128,
            HashAlgorithm.CSHAKE256: self._hash_cshake256,
            HashAlgorithm.TUPLEHASH128: self._hash_tuplehash128,
            HashAlgorithm.TUPLEHASH256: self._hash_tuplehash256,
            HashAlgorithm.KANGAROOTWELVE: self._hash_kangarootwelve,
            HashAlgorithm.WHIRLPOOL: self._hash_whirlpool,
            HashAlgorithm.BLAKE2B: self._hash_blake2b,
            HashAlgorithm.BLAKE2S: self._hash_blake2s,
            HashAlgorithm.KECCAK: self._hash_keccak,
        }

    def hash(
        self,
        data: bytes,
        algorithm: HashAlgorithm,
        key: Optional[bytes] = None,
        output_length: Optional[int] = None,
        custom: Optional[bytes] = None,
    ) -> HashResult:
        """Hash data using specified algorithm"""

        if algorithm not in self.supported_algorithms:
            raise UnsupportedAlgorithmException(algorithm.value)

        try:
            return self.supported_algorithms[algorithm](
                data, key, output_length, custom
            )
        except Exception as e:
            raise HashingException(f"Hashing failed: {str(e)}")

    def verify(
        self,
        data: bytes,
        expected_hash: bytes,
        algorithm: HashAlgorithm,
        key: Optional[bytes] = None,
        output_length: Optional[int] = None,
        custom: Optional[bytes] = None,
    ) -> bool:
        """Verify data against expected hash"""

        try:
            result = self.hash(data, algorithm, key, output_length, custom)
            return hmac.compare_digest(result.hash_value, expected_hash)
        except Exception:
            return False

    def _hash_sha1(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHA1 hashing"""
        if key:
            result = hmac.new(key, data, hashlib.sha1).digest()
        else:
            result = hashlib.sha1(data).digest()

        return HashResult(hash_value=result, algorithm="SHA1", length=len(result))

    def _hash_sha224(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHA224 hashing"""
        if key:
            result = hmac.new(key, data, hashlib.sha224).digest()
        else:
            result = hashlib.sha224(data).digest()

        return HashResult(hash_value=result, algorithm="SHA224", length=len(result))

    def _hash_sha256(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHA256 hashing"""
        if key:
            result = hmac.new(key, data, hashlib.sha256).digest()
        else:
            result = hashlib.sha256(data).digest()

        return HashResult(hash_value=result, algorithm="SHA256", length=len(result))

    def _hash_sha384(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHA384 hashing"""
        if key:
            result = hmac.new(key, data, hashlib.sha384).digest()
        else:
            result = hashlib.sha384(data).digest()

        return HashResult(hash_value=result, algorithm="SHA384", length=len(result))

    def _hash_sha512(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHA512 hashing"""
        if key:
            result = hmac.new(key, data, hashlib.sha512).digest()
        else:
            result = hashlib.sha512(data).digest()

        return HashResult(hash_value=result, algorithm="SHA512", length=len(result))

    def _hash_sha3_224(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHA3-224 hashing"""
        if key:
            h = SHA3_224.new()
            h.update(key + data)
            result = h.digest()
        else:
            result = SHA3_224.new(data).digest()

        return HashResult(hash_value=result, algorithm="SHA3-224", length=len(result))

    def _hash_sha3_256(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHA3-256 hashing"""
        if key:
            h = SHA3_256.new()
            h.update(key + data)
            result = h.digest()
        else:
            result = SHA3_256.new(data).digest()

        return HashResult(hash_value=result, algorithm="SHA3-256", length=len(result))

    def _hash_sha3_384(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHA3-384 hashing"""
        if key:
            h = SHA3_384.new()
            h.update(key + data)
            result = h.digest()
        else:
            result = SHA3_384.new(data).digest()

        return HashResult(hash_value=result, algorithm="SHA3-384", length=len(result))

    def _hash_sha3_512(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHA3-512 hashing"""
        if key:
            h = SHA3_512.new()
            h.update(key + data)
            result = h.digest()
        else:
            result = SHA3_512.new(data).digest()

        return HashResult(hash_value=result, algorithm="SHA3-512", length=len(result))

    def _hash_shake128(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHAKE128 hashing"""
        if not output_length:
            output_length = 32

        if key:
            h = SHAKE128.new()
            h.update(key + data)
            result = h.read(output_length)
        else:
            h = SHAKE128.new(data)
            result = h.read(output_length)

        return HashResult(hash_value=result, algorithm="SHAKE128", length=len(result))

    def _hash_shake256(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """SHAKE256 hashing"""
        if not output_length:
            output_length = 64

        if key:
            h = SHAKE256.new()
            h.update(key + data)
            result = h.read(output_length)
        else:
            h = SHAKE256.new(data)
            result = h.read(output_length)

        return HashResult(hash_value=result, algorithm="SHAKE256", length=len(result))

    def _hash_cshake128(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """cSHAKE128 hashing"""
        if not output_length:
            output_length = 32

        if custom:
            h = cSHAKE128.new(custom=custom)
        else:
            h = cSHAKE128.new()

        if key:
            h.update(key + data)
        else:
            h.update(data)

        result = h.read(output_length)

        return HashResult(hash_value=result, algorithm="cSHAKE128", length=len(result))

    def _hash_cshake256(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """cSHAKE256 hashing"""
        if not output_length:
            output_length = 64

        if custom:
            h = cSHAKE256.new(custom=custom)
        else:
            h = cSHAKE256.new()

        if key:
            h.update(key + data)
        else:
            h.update(data)

        result = h.read(output_length)

        return HashResult(hash_value=result, algorithm="cSHAKE256", length=len(result))

    def _hash_tuplehash128(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """TupleHash128 hashing"""
        if not output_length:
            output_length = 32

        h = TupleHash128.new(custom=custom)

        if key:
            h.update(key + data)
        else:
            h.update(data)

        result = h.read(output_length)

        return HashResult(
            hash_value=result, algorithm="TupleHash128", length=len(result)
        )

    def _hash_tuplehash256(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """TupleHash256 hashing"""
        if not output_length:
            output_length = 64

        h = TupleHash256.new(custom=custom)

        if key:
            h.update(key + data)
        else:
            h.update(data)

        result = h.read(output_length)

        return HashResult(
            hash_value=result, algorithm="TupleHash256", length=len(result)
        )

    def _hash_kangarootwelve(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """KangarooTwelve hashing"""
        if not output_length:
            output_length = 32

        if key:
            h = KangarooTwelve.new()
            h.update(key + data)
            result = h.read(output_length)
        else:
            h = KangarooTwelve.new(data)
            result = h.read(output_length)

        return HashResult(
            hash_value=result, algorithm="KangarooTwelve", length=len(result)
        )

    def _hash_whirlpool(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """Whirlpool hashing"""
        if key:
            h = Whirlpool.new()
            h.update(key + data)
            result = h.digest()
        else:
            result = Whirlpool.new(data).digest()

        return HashResult(hash_value=result, algorithm="Whirlpool", length=len(result))

    def _hash_blake2b(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """BLAKE2b hashing"""
        if not output_length:
            output_length = 64

        if key:
            h = BLAKE2b.new(key=key, digest_bytes=output_length)
            h.update(data)
            result = h.digest()
        else:
            h = BLAKE2b.new(digest_bytes=output_length)
            h.update(data)
            result = h.digest()

        return HashResult(hash_value=result, algorithm="BLAKE2b", length=len(result))

    def _hash_blake2s(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """BLAKE2s hashing"""
        if not output_length:
            output_length = 32

        if key:
            h = BLAKE2s.new(key=key, digest_bytes=output_length)
            h.update(data)
            result = h.digest()
        else:
            h = BLAKE2s.new(digest_bytes=output_length)
            h.update(data)
            result = h.digest()

        return HashResult(hash_value=result, algorithm="BLAKE2s", length=len(result))

    def _hash_keccak(
        self,
        data: bytes,
        key: Optional[bytes],
        output_length: Optional[int],
        custom: Optional[bytes],
    ) -> HashResult:
        """Keccak hashing"""
        if key:
            h = keccak_hash.new()
            h.update(key + data)
            result = h.digest()
        else:
            result = keccak_hash.new(data).digest()

        return HashResult(hash_value=result, algorithm="Keccak", length=len(result))

    def get_supported_hashes(self) -> List[SupportedHash]:
        """Get a list of supported hash algorithms and their settings"""
        supported_hashes = [
            SupportedHash(name="sha1", key_required=True),
            SupportedHash(name="sha224", key_required=True),
            SupportedHash(name="sha256", key_required=True),
            SupportedHash(name="sha384", key_required=True),
            SupportedHash(name="sha512", key_required=True),
            SupportedHash(name="sha3_224"),
            SupportedHash(name="sha3_256"),
            SupportedHash(name="sha3_384"),
            SupportedHash(name="sha3_512"),
            SupportedHash(name="shake128", output_lengths=[16, 20, 28, 32, 48, 64]),
            SupportedHash(name="shake256", output_lengths=[16, 20, 28, 32, 48, 64]),
            SupportedHash(name="cshake128", custom_required=True, output_lengths=[16, 20, 28, 32, 48, 64]),
            SupportedHash(name="cshake256", custom_required=True, output_lengths=[16, 20, 28, 32, 48, 64]),
            SupportedHash(name="tuplehash128", custom_required=True, output_lengths=[16, 20, 28, 32, 48, 64]),
            SupportedHash(name="tuplehash256", custom_required=True, output_lengths=[16, 20, 28, 32, 48, 64]),
            SupportedHash(name="kangarootwelve", output_lengths=[16, 20, 28, 32, 48, 64]),
            SupportedHash(name="whirlpool"),
            SupportedHash(name="blake2b", key_required=True, output_lengths=[16, 20, 28, 32, 48, 64]),
            SupportedHash(name="blake2s", key_required=True, output_lengths=[16, 20, 28, 32, 48, 64]),
            SupportedHash(name="keccak"),
        ]
        return supported_hashes
