"""
Comprehensive encryption service supporting multiple algorithms
"""

import os
from typing import Optional, Tuple, Dict, Any
from Crypto.Cipher import (
    AES, DES, DES3, ChaCha20_Poly1305, ChaCha20,
    Blowfish, ARC2, ARC4, CAST
)
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from app.core.exceptions import (
    EncryptionException, DecryptionException, InvalidKeyException,
    UnsupportedAlgorithmException
)
from .models import (
    EncryptionAlgorithm, EncryptionMode, EncryptionResult, DecryptionResult
)
from app.services.hashing.models import HashSettings
from app.services.hashing.hashing_service import HashingService


class EncryptionService:
    """Service for handling various encryption algorithms"""
    
    def __init__(self):
        self.hashing_service = HashingService()
        self.supported_algorithms = {
            EncryptionAlgorithm.AES: self._encrypt_aes,
            EncryptionAlgorithm.DES: self._encrypt_des,
            EncryptionAlgorithm.DES3: self._encrypt_des3,
            EncryptionAlgorithm.CHACHA20: self._encrypt_chacha20,
            EncryptionAlgorithm.CHACHA20_POLY1305: self._encrypt_chacha20_poly1305,
            EncryptionAlgorithm.BLOWFISH: self._encrypt_blowfish,
            EncryptionAlgorithm.ARC2: self._encrypt_arc2,
            EncryptionAlgorithm.ARC4: self._encrypt_arc4,
            EncryptionAlgorithm.SALSA20: self._encrypt_salsa20,
            EncryptionAlgorithm.CAST: self._encrypt_cast,
            EncryptionAlgorithm.PKCS1_OAEP: self._encrypt_pkcs1_oaep,
            EncryptionAlgorithm.PKCS1_V1_5: self._encrypt_pkcs1_v1_5,
            EncryptionAlgorithm.XOR: self._encrypt_xor,
        }
        
        self.supported_modes = {
            EncryptionMode.CBC: "CBC",
            EncryptionMode.CFB: "CFB",
            EncryptionMode.OFB: "OFB",
            EncryptionMode.CTR: "CTR",
            EncryptionMode.ECB: "ECB",
            EncryptionMode.GCM: "GCM",
        }
    
    def encrypt(
        self,
        data: bytes,
        algorithm: EncryptionAlgorithm,
        key: Optional[bytes] = None,
        mode: Optional[EncryptionMode] = None,
        key_size: Optional[int] = None,
        hash_settings: Optional[HashSettings] = None
    ) -> EncryptionResult:
        """Encrypt data using specified algorithm"""
        
        metadata = {}
        if hash_settings:
            hash_result = self.hashing_service.hash_data(
                data=data,
                algorithm=hash_settings.algorithm,
                key=hash_settings.key,
                output_length=hash_settings.output_length,
                custom=hash_settings.custom
            )
            data = hash_result.hash_value
            metadata['hash'] = hash_result.dict()

        if algorithm not in self.supported_algorithms:
            raise UnsupportedAlgorithmException(algorithm.value)
        
        try:
            encryption_result = self.supported_algorithms[algorithm](
                data, key, mode, key_size
            )
            if encryption_result.metadata:
                encryption_result.metadata.update(metadata)
            else:
                encryption_result.metadata = metadata
            return encryption_result
        except Exception as e:
            raise EncryptionException(f"Encryption failed: {str(e)}")
    
    def decrypt(
        self,
        encrypted_data: bytes,
        key: bytes,
        algorithm: EncryptionAlgorithm,
        mode: Optional[EncryptionMode] = None,
        iv: Optional[bytes] = None,
        nonce: Optional[bytes] = None,
        tag: Optional[bytes] = None
    ) -> DecryptionResult:
        """Decrypt data using specified algorithm"""
        
        if algorithm not in self.supported_algorithms:
            raise UnsupportedAlgorithmException(algorithm.value)
        
        try:
            return self._decrypt_data(
                encrypted_data, key, algorithm, mode, iv, nonce, tag
            )
        except Exception as e:
            raise DecryptionException(f"Decryption failed: {str(e)}")
    
    def generate_key(self, algorithm: EncryptionAlgorithm, key_size: Optional[int] = None) -> bytes:
        """Generate a key for the specified algorithm"""
        
        key_sizes = {
            EncryptionAlgorithm.AES: key_size or 32,
            EncryptionAlgorithm.DES: 8,
            EncryptionAlgorithm.DES3: 24,
            EncryptionAlgorithm.CHACHA20: 32,
            EncryptionAlgorithm.CHACHA20_POLY1305: 32,
            EncryptionAlgorithm.BLOWFISH: key_size or 32,
            EncryptionAlgorithm.ARC2: key_size or 16,
            EncryptionAlgorithm.ARC4: key_size or 16,
            EncryptionAlgorithm.SALSA20: 32,
            EncryptionAlgorithm.CAST: key_size or 16,
            EncryptionAlgorithm.PKCS1_OAEP: 0,  # RSA key pair needed
            EncryptionAlgorithm.PKCS1_V1_5: 0,  # RSA key pair needed
            EncryptionAlgorithm.XOR: key_size or 32,
        }
        
        if algorithm in [EncryptionAlgorithm.PKCS1_OAEP, EncryptionAlgorithm.PKCS1_V1_5]:
            raise EncryptionException("RSA key pairs require special generation")
        
        key_length = key_sizes.get(algorithm, key_size or 32)
        return get_random_bytes(key_length)
    
    def _encrypt_aes(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """AES encryption"""
        if not key:
            key = get_random_bytes(key_size or 32)
        
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = AES.new(key, AES.MODE_ECB)
            encrypted = cipher.encrypt(pad(data, AES.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                algorithm="AES",
                mode="ECB"
            )
        elif mode == EncryptionMode.GCM:
            cipher = AES.new(key, AES.MODE_GCM)
            encrypted, tag = cipher.encrypt_and_digest(data)
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                nonce=cipher.nonce,
                tag=tag,
                algorithm="AES",
                mode="GCM"
            )
        else:
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(key, getattr(AES, f"MODE_{mode.value}"), iv)
            encrypted = cipher.encrypt(pad(data, AES.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                iv=iv,
                algorithm="AES",
                mode=mode.value
            )
    
    def _encrypt_des(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """DES encryption"""
        if not key:
            key = get_random_bytes(8)
        elif len(key) != 8:
            raise InvalidKeyException("DES key must be 8 bytes")
        
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = DES.new(key, DES.MODE_ECB)
            encrypted = cipher.encrypt(pad(data, DES.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                algorithm="DES",
                mode="ECB"
            )
        else:
            iv = get_random_bytes(DES.block_size)
            cipher = DES.new(key, getattr(DES, f"MODE_{mode.value}"), iv)
            encrypted = cipher.encrypt(pad(data, DES.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                iv=iv,
                algorithm="DES",
                mode=mode.value
            )
    
    def _encrypt_des3(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """3DES encryption"""
        if not key:
            key = get_random_bytes(24)
        elif len(key) != 16 and len(key) != 24:
            raise InvalidKeyException("3DES key must be 16 or 24 bytes")
        
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = DES3.new(key, DES3.MODE_ECB)
            encrypted = cipher.encrypt(pad(data, DES3.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                algorithm="3DES",
                mode="ECB"
            )
        else:
            iv = get_random_bytes(DES3.block_size)
            cipher = DES3.new(key, getattr(DES3, f"MODE_{mode.value}"), iv)
            encrypted = cipher.encrypt(pad(data, DES3.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                iv=iv,
                algorithm="3DES",
                mode=mode.value
            )
    
    def _encrypt_chacha20(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """ChaCha20 encryption"""
        if not key:
            key = get_random_bytes(32)
        elif len(key) != 32:
            raise InvalidKeyException("ChaCha20 key must be 32 bytes")
        
        cipher = ChaCha20.new(key=key)
        encrypted = cipher.encrypt(data)
        return EncryptionResult(
            encrypted_data=encrypted,
            key=key,
            nonce=cipher.nonce,
            algorithm="ChaCha20"
        )
    
    def _encrypt_chacha20_poly1305(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """ChaCha20-Poly1305 encryption"""
        if not key:
            key = get_random_bytes(32)
        elif len(key) != 32:
            raise InvalidKeyException("ChaCha20-Poly1305 key must be 32 bytes")
        
        cipher = ChaCha20_Poly1305.new(key=key)
        encrypted, tag = cipher.encrypt_and_digest(data)
        return EncryptionResult(
            encrypted_data=encrypted,
            key=key,
            nonce=cipher.nonce,
            tag=tag,
            algorithm="ChaCha20-Poly1305"
        )
    
    def _encrypt_blowfish(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """Blowfish encryption"""
        if not key:
            key = get_random_bytes(32)
        elif len(key) < 4 or len(key) > 56:
            raise InvalidKeyException("Blowfish key must be 4-56 bytes")
        
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = Blowfish.new(key, Blowfish.MODE_ECB)
            encrypted = cipher.encrypt(pad(data, Blowfish.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                algorithm="Blowfish",
                mode="ECB"
            )
        else:
            iv = get_random_bytes(Blowfish.block_size)
            cipher = Blowfish.new(key, getattr(Blowfish, f"MODE_{mode.value}"), iv)
            encrypted = cipher.encrypt(pad(data, Blowfish.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                iv=iv,
                algorithm="Blowfish",
                mode=mode.value
            )
    
    def _encrypt_arc2(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """ARC2 encryption"""
        if not key:
            key = get_random_bytes(16)
        
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = ARC2.new(key, ARC2.MODE_ECB)
            encrypted = cipher.encrypt(pad(data, ARC2.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                algorithm="ARC2",
                mode="ECB"
            )
        else:
            iv = get_random_bytes(ARC2.block_size)
            cipher = ARC2.new(key, getattr(ARC2, f"MODE_{mode.value}"), iv)
            encrypted = cipher.encrypt(pad(data, ARC2.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                iv=iv,
                algorithm="ARC2",
                mode=mode.value
            )
    
    def _encrypt_arc4(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """ARC4 encryption"""
        if not key:
            key = get_random_bytes(16)
        
        cipher = ARC4.new(key)
        encrypted = cipher.encrypt(data)
        return EncryptionResult(
            encrypted_data=encrypted,
            key=key,
            algorithm="ARC4"
        )
    
    def _encrypt_salsa20(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """Salsa20 encryption"""
        if not key:
            key = get_random_bytes(32)
        elif len(key) != 32:
            raise InvalidKeyException("Salsa20 key must be 32 bytes")
        
        cipher = ChaCha20.new(key=key)  # Salsa20 is similar to ChaCha20
        encrypted = cipher.encrypt(data)
        return EncryptionResult(
            encrypted_data=encrypted,
            key=key,
            nonce=cipher.nonce,
            algorithm="Salsa20"
        )
    
    def _encrypt_cast(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """CAST encryption"""
        if not key:
            key = get_random_bytes(16)
        
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = CAST.new(key, CAST.MODE_ECB)
            encrypted = cipher.encrypt(pad(data, CAST.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                algorithm="CAST",
                mode="ECB"
            )
        else:
            iv = get_random_bytes(CAST.block_size)
            cipher = CAST.new(key, getattr(CAST, f"MODE_{mode.value}"), iv)
            encrypted = cipher.encrypt(pad(data, CAST.block_size))
            return EncryptionResult(
                encrypted_data=encrypted,
                key=key,
                iv=iv,
                algorithm="CAST",
                mode=mode.value
            )
    
    def _encrypt_pkcs1_oaep(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """RSA PKCS1_OAEP encryption"""
        if not key:
            key = RSA.generate(2048)
        elif isinstance(key, bytes):
            key = RSA.import_key(key)
        
        cipher = PKCS1_OAEP.new(key)
        encrypted = cipher.encrypt(data)
        return EncryptionResult(
            encrypted_data=encrypted,
            key=key.export_key(),
            algorithm="PKCS1_OAEP"
        )
    
    def _encrypt_pkcs1_v1_5(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """RSA PKCS1_v1_5 encryption"""
        if not key:
            key = RSA.generate(2048)
        elif isinstance(key, bytes):
            key = RSA.import_key(key)
        
        cipher = PKCS1_v1_5.new(key)
        encrypted = cipher.encrypt(data)
        return EncryptionResult(
            encrypted_data=encrypted,
            key=key.export_key(),
            algorithm="PKCS1_v1_5"
        )
    
    def _encrypt_xor(
        self, data: bytes, key: Optional[bytes], mode: Optional[EncryptionMode], key_size: Optional[int]
    ) -> EncryptionResult:
        """XOR encryption"""
        if not key:
            key = get_random_bytes(key_size or 32)
        
        encrypted = bytes(a ^ b for a, b in zip(data, key * ((len(data) // len(key)) + 1)))
        return EncryptionResult(
            encrypted_data=encrypted,
            key=key,
            algorithm="XOR"
        )
    
    def _decrypt_data(
        self, encrypted_data: bytes, key: bytes, algorithm: EncryptionAlgorithm,
        mode: Optional[EncryptionMode], iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """Generic decryption method"""
        
        decrypt_methods = {
            EncryptionAlgorithm.AES: self._decrypt_aes,
            EncryptionAlgorithm.DES: self._decrypt_des,
            EncryptionAlgorithm.DES3: self._decrypt_des3,
            EncryptionAlgorithm.CHACHA20: self._decrypt_chacha20,
            EncryptionAlgorithm.CHACHA20_POLY1305: self._decrypt_chacha20_poly1305,
            EncryptionAlgorithm.BLOWFISH: self._decrypt_blowfish,
            EncryptionAlgorithm.ARC2: self._decrypt_arc2,
            EncryptionAlgorithm.ARC4: self._decrypt_arc4,
            EncryptionAlgorithm.SALSA20: self._decrypt_salsa20,
            EncryptionAlgorithm.CAST: self._decrypt_cast,
            EncryptionAlgorithm.PKCS1_OAEP: self._decrypt_pkcs1_oaep,
            EncryptionAlgorithm.PKCS1_V1_5: self._decrypt_pkcs1_v1_5,
            EncryptionAlgorithm.XOR: self._decrypt_xor,
        }
        
        if algorithm not in decrypt_methods:
            raise UnsupportedAlgorithmException(algorithm.value)
        
        return decrypt_methods[algorithm](
            encrypted_data, key, mode, iv, nonce, tag
        )
    
    def _decrypt_aes(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """AES decryption"""
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = AES.new(key, AES.MODE_ECB)
            decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        elif mode == EncryptionMode.GCM:
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            decrypted = cipher.decrypt_and_verify(encrypted_data, tag)
        else:
            if not iv:
                raise InvalidKeyException("IV required for AES CBC/CFB/OFB/CTR modes")
            cipher = AES.new(key, getattr(AES, f"MODE_{mode.value}"), iv)
            decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="AES",
            mode=mode.value
        )
    
    def _decrypt_des(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """DES decryption"""
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = DES.new(key, DES.MODE_ECB)
            decrypted = unpad(cipher.decrypt(encrypted_data), DES.block_size)
        else:
            if not iv:
                raise InvalidKeyException("IV required for DES CBC/CFB/OFB/CTR modes")
            cipher = DES.new(key, getattr(DES, f"MODE_{mode.value}"), iv)
            decrypted = unpad(cipher.decrypt(encrypted_data), DES.block_size)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="DES",
            mode=mode.value
        )
    
    def _decrypt_des3(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """3DES decryption"""
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = DES3.new(key, DES3.MODE_ECB)
            decrypted = unpad(cipher.decrypt(encrypted_data), DES3.block_size)
        else:
            if not iv:
                raise InvalidKeyException("IV required for 3DES CBC/CFB/OFB/CTR modes")
            cipher = DES3.new(key, getattr(DES3, f"MODE_{mode.value}"), iv)
            decrypted = unpad(cipher.decrypt(encrypted_data), DES3.block_size)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="3DES",
            mode=mode.value
        )
    
    def _decrypt_chacha20(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """ChaCha20 decryption"""
        if not nonce:
            raise InvalidKeyException("Nonce required for ChaCha20")
        
        cipher = ChaCha20.new(key=key, nonce=nonce)
        decrypted = cipher.decrypt(encrypted_data)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="ChaCha20"
        )
    def _decrypt_chacha20_poly1305(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """ChaCha20-Poly1305 decryption"""
        if not nonce or not tag:
            raise InvalidKeyException("Nonce and tag required for ChaCha20-Poly1305")
        
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(encrypted_data, tag)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="ChaCha20-Poly1305"
        )
    
    def _decrypt_blowfish(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """Blowfish decryption"""
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = Blowfish.new(key, Blowfish.MODE_ECB)
            decrypted = unpad(cipher.decrypt(encrypted_data), Blowfish.block_size)
        else:
            if not iv:
                raise InvalidKeyException("IV required for Blowfish CBC/CFB/OFB/CTR modes")
            cipher = Blowfish.new(key, getattr(Blowfish, f"MODE_{mode.value}"), iv)
            decrypted = unpad(cipher.decrypt(encrypted_data), Blowfish.block_size)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="Blowfish",
            mode=mode.value
        )
    
    def _decrypt_arc2(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """ARC2 decryption"""
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = ARC2.new(key, ARC2.MODE_ECB)
            decrypted = unpad(cipher.decrypt(encrypted_data), ARC2.block_size)
        else:
            if not iv:
                raise InvalidKeyException("IV required for ARC2 CBC/CFB/OFB/CTR modes")
            cipher = ARC2.new(key, getattr(ARC2, f"MODE_{mode.value}"), iv)
            decrypted = unpad(cipher.decrypt(encrypted_data), ARC2.block_size)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="ARC2",
            mode=mode.value
        )
    
    def _decrypt_arc4(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """ARC4 decryption"""
        cipher = ARC4.new(key)
        decrypted = cipher.decrypt(encrypted_data)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="ARC4"
        )
    
    def _decrypt_salsa20(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """Salsa20 decryption"""
        if not nonce:
            raise InvalidKeyException("Nonce required for Salsa20")
        
        cipher = ChaCha20.new(key=key, nonce=nonce)
        decrypted = cipher.decrypt(encrypted_data)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="Salsa20"
        )
    
    def _decrypt_cast(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """CAST decryption"""
        mode = mode or EncryptionMode.CBC
        
        if mode == EncryptionMode.ECB:
            cipher = CAST.new(key, CAST.MODE_ECB)
            decrypted = unpad(cipher.decrypt(encrypted_data), CAST.block_size)
        else:
            if not iv:
                raise InvalidKeyException("IV required for CAST CBC/CFB/OFB/CTR modes")
            cipher = CAST.new(key, getattr(CAST, f"MODE_{mode.value}"), iv)
            decrypted = unpad(cipher.decrypt(encrypted_data), CAST.block_size)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="CAST",
            mode=mode.value
        )
    
    def _decrypt_pkcs1_oaep(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """RSA PKCS1_OAEP decryption"""
        if isinstance(key, bytes):
            key = RSA.import_key(key)
        
        cipher = PKCS1_OAEP.new(key)
        decrypted = cipher.decrypt(encrypted_data)
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="PKCS1_OAEP"
        )
    
    def _decrypt_pkcs1_v1_5(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """RSA PKCS1_v1_5 decryption"""
        if isinstance(key, bytes):
            key = RSA.import_key(key)
        
        cipher = PKCS1_v1_5.new(key)
        decrypted = cipher.decrypt(encrypted_data, None)
        
        if decrypted is None:
            raise DecryptionException("PKCS1_v1_5 decryption failed")
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="PKCS1_v1_5"
        )
    
    def _decrypt_xor(
        self, encrypted_data: bytes, key: bytes, mode: Optional[EncryptionMode],
        iv: Optional[bytes], nonce: Optional[bytes], tag: Optional[bytes]
    ) -> DecryptionResult:
        """XOR decryption"""
        decrypted = bytes(a ^ b for a, b in zip(encrypted_data, key * ((len(encrypted_data) // len(key)) + 1)))
        
        return DecryptionResult(
            decrypted_data=decrypted,
            algorithm="XOR"
        )
       
