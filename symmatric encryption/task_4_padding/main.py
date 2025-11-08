"""
Task 4: Padding Analysis
Identifies which encryption modes require padding
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def run():
    """Task 4: Padding analysis"""
    backend = default_backend()
    results = []

    # Create plaintexts of different sizes
    test_cases = [
        (b"A" * 15, "15 bytes"),
        (b"B" * 16, "16 bytes"),
        (b"C" * 17, "17 bytes"),
    ]

    key = bytes.fromhex('00112233445566778889aabbccddeeff')
    iv = bytes.fromhex('0102030405060708090a0b0c0d0e0f10')

    modes_to_test = [
        ('ECB', modes.ECB(), True),
        ('CBC', modes.CBC(iv), True),
        ('CFB', modes.CFB(iv), False),
        ('OFB', modes.OFB(iv), False),
    ]

    for plaintext, description in test_cases:
        test_result = {'plaintext_size': description, 'modes': {}}

        for mode_name, mode, needs_padding in modes_to_test:
            if needs_padding:
                # Apply PKCS7 padding
                block_size = 16
                padding_length = block_size - (len(plaintext) % block_size)
                padded = plaintext + bytes([padding_length] * padding_length)
            else:
                padded = plaintext

            cipher = Cipher(algorithms.AES(key), mode, backend=backend)
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded) + encryptor.finalize()

            test_result['modes'][mode_name] = {
                'needs_padding': needs_padding,
                'input_size': len(plaintext),
                'padded_size': len(padded),
                'output_size': len(ciphertext)
            }

        results.append(test_result)

    return {
        'results': results,
        'conclusion': {
            'block_modes': 'ECB and CBC require padding (block ciphers)',
            'stream_modes': 'CFB and OFB do not require padding (stream ciphers)'
        }
    }


if __name__ == "__main__":
    result = run()
