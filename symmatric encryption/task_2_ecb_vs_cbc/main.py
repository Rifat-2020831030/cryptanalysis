"""
Task 2: ECB vs CBC Mode Comparison
Encrypts an image file using ECB and CBC modes to demonstrate security differences
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PIL import Image
import os


def run():
    """Task 2: ECB vs CBC mode with image encryption"""
    backend = default_backend()

    # Load the maskot image from parent directory
    maskot_path = os.path.join('..', 'maskot.jpg')

    try:
        img = Image.open(maskot_path)

        # Convert to BMP format if not already
        if img.format != 'BMP':
            img.save('original.bmp', 'BMP')
            img = Image.open('original.bmp')
        else:
            img.save('original.bmp', 'BMP')

        # Read BMP file
        with open('original.bmp', 'rb') as f:
            bmp_data = f.read()

        # BMP header is first 54 bytes
        header = bmp_data[:54]
        pixel_data = bmp_data[54:]

    except FileNotFoundError:
        # If maskot.jpg not found, create a simple pattern image
        width, height = 200, 200
        img = Image.new('RGB', (width, height))
        pixels = img.load()

        # Create a pattern
        for y in range(height):
            for x in range(width):
                if (x // 20) % 2 == 0:
                    pixels[x, y] = (255, 0, 0)  # Red
                else:
                    pixels[x, y] = (0, 0, 255)  # Blue

        img.save('original.bmp', 'BMP')

        with open('original.bmp', 'rb') as f:
            bmp_data = f.read()

        header = bmp_data[:54]
        pixel_data = bmp_data[54:]

    # Encryption key and IV
    key = bytes.fromhex('00112233445566778889aabbccddeeff')
    iv = bytes.fromhex('0102030405060708090a0b0c0d0e0f10')

    # Pad data for block cipher
    block_size = 16
    padding_length = block_size - (len(pixel_data) % block_size)
    if padding_length != block_size:
        data_padded = pixel_data + bytes([padding_length] * padding_length)
    else:
        data_padded = pixel_data

    # Encrypt with ECB
    cipher_ecb = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor_ecb = cipher_ecb.encryptor()
    encrypted_data_ecb = encryptor_ecb.update(
        data_padded) + encryptor_ecb.finalize()

    # Replace header and save
    encrypted_bmp_ecb = header + encrypted_data_ecb[:len(pixel_data)]
    with open('encrypted_ecb.bmp', 'wb') as f:
        f.write(encrypted_bmp_ecb)

    # Encrypt with CBC
    cipher_cbc = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor_cbc = cipher_cbc.encryptor()
    encrypted_data_cbc = encryptor_cbc.update(
        data_padded) + encryptor_cbc.finalize()

    # Replace header and save
    encrypted_bmp_cbc = header + encrypted_data_cbc[:len(pixel_data)]
    with open('encrypted_cbc.bmp', 'wb') as f:
        f.write(encrypted_bmp_cbc)

    return {
        'original': 'original.bmp',
        'ecb': 'encrypted_ecb.bmp',
        'cbc': 'encrypted_cbc.bmp',
        'analysis': 'ECB preserves patterns, CBC obscures them'
    }


if __name__ == "__main__":
    result = run()
