"""
Task 1: AES Encryption Using Different Modes
Encrypts a text file using various AES cipher modes
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


def run():
    """Task 1: AES encryption using different modes"""
    backend = default_backend()
    results = []

    # Create plaintext
    plaintext = b"This is a test file for symmetric encryption using AES. " * 3

    # Define key and IV
    key_128 = bytes.fromhex('00112233445566778889aabbccddeeff')
    key_256 = bytes.fromhex(
        '00112233445566778889aabbccddeeff00112233445566778889aabbccddeeff')
    iv = bytes.fromhex('0102030405060708090a0b0c0d0e0f10')

    modes_config = [
        ('AES-128-CBC', algorithms.AES(key_128), modes.CBC(iv)),
        ('AES-128-CFB', algorithms.AES(key_128), modes.CFB(iv)),
        ('AES-256-ECB', algorithms.AES(key_256), modes.ECB()),
        ('AES-128-OFB', algorithms.AES(key_128), modes.OFB(iv)),
        ('AES-256-CBC', algorithms.AES(key_256), modes.CBC(iv)),
        ('AES-128-CTR', algorithms.AES(key_256), modes.CTR(iv)),
    ]

    for mode_name, algorithm, mode in modes_config:
        # Pad plaintext if needed (for block modes)
        if isinstance(mode, (modes.CBC, modes.ECB)):
            block_size = algorithm.block_size // 8
            padding_length = block_size - (len(plaintext) % block_size)
            padded_plaintext = plaintext + \
                bytes([padding_length] * padding_length)
        else:
            padded_plaintext = plaintext

        # Encrypt
        cipher = Cipher(algorithm, mode, backend=backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        # Save encrypted file
        filename = f"cipher_{mode_name.lower().replace('-', '_')}.bin"
        with open(filename, 'wb') as f:
            f.write(ciphertext)

        # Decrypt to verify
        if isinstance(mode, (modes.CBC, modes.ECB)):
            if mode_name == 'AES-128-CBC':
                new_mode = modes.CBC(iv)
            elif mode_name == 'AES-256-CBC':
                new_mode = modes.CBC(iv)
            else:
                new_mode = modes.ECB()
        elif isinstance(mode, modes.CFB):
            new_mode = modes.CFB(iv)
        elif isinstance(mode, modes.OFB):
            new_mode = modes.OFB(iv)
        else:
            new_mode = modes.CTR(iv)

        cipher = Cipher(algorithm, new_mode, backend=backend)
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding if needed
        if isinstance(mode, (modes.CBC, modes.ECB)):
            padding_length = decrypted[-1]
            decrypted = decrypted[:-padding_length]

        verification = "SUCCESS" if decrypted == plaintext else "FAILED"

        results.append({
            'mode': mode_name,
            'ciphertext_length': len(ciphertext),
            'verification': verification,
            'filename': filename
        })

    # Save original plaintext
    with open('plaintext.txt', 'wb') as f:
        f.write(plaintext)

    return results


if __name__ == "__main__":
    results = run()
