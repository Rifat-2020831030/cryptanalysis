"""
Task 3: Corrupted Cipher Text Analysis
Analyzes how different encryption modes handle corruption in ciphertext
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def run():
    """Task 3: Corrupted cipher text analysis"""
    backend = default_backend()
    results = []

    # Create plaintext (at least 64 bytes)
    plaintext = b"A" * 32 + b"B" * 32 + b"C" * 32 + b"D" * 32

    with open('plaintext.txt', 'wb') as f:
        f.write(plaintext)

    key = bytes.fromhex('00112233445566778889aabbccddeeff')
    iv = bytes.fromhex('0102030405060708090a0b0c0d0e0f10')

    modes_to_test = [
        ('ECB', modes.ECB()),
        ('CBC', modes.CBC(iv)),
        ('CFB', modes.CFB(iv)),
        ('OFB', modes.OFB(iv)),
    ]

    for mode_name, mode in modes_to_test:
        # Pad if needed
        if isinstance(mode, (modes.CBC, modes.ECB)):
            block_size = 16
            padding_length = block_size - (len(plaintext) % block_size)
            if padding_length != block_size:
                padded_plaintext = plaintext + \
                    bytes([padding_length] * padding_length)
            else:
                padded_plaintext = plaintext
        else:
            padded_plaintext = plaintext

        # Encrypt
        cipher = Cipher(algorithms.AES(key), mode, backend=backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        # Corrupt 30th byte (flip one bit)
        corrupted_ciphertext = bytearray(ciphertext)
        corrupted_ciphertext[29] ^= 0x01  # Flip the least significant bit
        corrupted_ciphertext = bytes(corrupted_ciphertext)

        # Decrypt corrupted ciphertext
        if mode_name == 'ECB':
            decrypt_mode = modes.ECB()
        elif mode_name == 'CBC':
            decrypt_mode = modes.CBC(iv)
        elif mode_name == 'CFB':
            decrypt_mode = modes.CFB(iv)
        else:
            decrypt_mode = modes.OFB(iv)

        cipher = Cipher(algorithms.AES(key), decrypt_mode, backend=backend)
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(
            corrupted_ciphertext) + decryptor.finalize()

        # Remove padding if needed
        if isinstance(mode, (modes.CBC, modes.ECB)):
            try:
                padding_length = decrypted[-1]
                if padding_length <= 16:
                    decrypted = decrypted[:-padding_length]
            except:
                pass

        # Analyze recovery
        if len(decrypted) >= len(plaintext):
            decrypted = decrypted[:len(plaintext)]
            matches = sum(1 for a, b in zip(plaintext, decrypted) if a == b)
            recovery_rate = (matches / len(plaintext)) * 100

            # Calculate affected blocks
            affected_blocks = []
            for i in range(0, len(plaintext), 16):
                if plaintext[i:i+16] != decrypted[i:i+16]:
                    affected_blocks.append(i // 16)
        else:
            matches = 0
            recovery_rate = 0.0
            affected_blocks = []

        # Save files
        with open(f'cipher_{mode_name.lower()}.bin', 'wb') as f:
            f.write(ciphertext)
        with open(f'corrupted_{mode_name.lower()}.bin', 'wb') as f:
            f.write(corrupted_ciphertext)
        with open(f'decrypted_{mode_name.lower()}.txt', 'wb') as f:
            f.write(decrypted)

        results.append({
            'mode': mode_name,
            'recovery_rate': recovery_rate,
            'recovered_bytes': f"{matches}/{len(plaintext)}",
            'affected_blocks': affected_blocks
        })

    return results


if __name__ == "__main__":
    results = run()
