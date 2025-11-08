"""
Cryptography Operations Program
Implements AES, RSA, and SHA-256 operations with performance measurement

References:
- Python Cryptography Library: https://cryptography.io/en/latest/
- PyCryptodome Documentation: https://pycryptodome.readthedocs.io/
- Python hashlib: https://docs.python.org/3/library/hashlib.html
"""

import os
import time
import hashlib
import json
from pathlib import Path

# Cryptography imports
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature


class CryptoOperations:
    """Main class for cryptographic operations"""

    def __init__(self):
        self.backend = default_backend()
        self.keys_dir = Path("keys")
        self.output_dir = Path("output")
        self.performance_data = []

        # Create directories
        self.keys_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

    # ==================== AES OPERATIONS ====================

    def generate_aes_key(self, key_length):
        """Generate and save AES key"""
        key = os.urandom(key_length // 8)
        key_file = self.keys_dir / f"aes_{key_length}_key.bin"

        with open(key_file, 'wb') as f:
            f.write(key)

        print(f"[+] AES-{key_length} key generated and saved to {key_file}")
        return key

    def load_aes_key(self, key_length):
        """Load AES key from file"""
        key_file = self.keys_dir / f"aes_{key_length}_key.bin"

        if not key_file.exists():
            print(f"[!] Key file not found. Generating new key...")
            return self.generate_aes_key(key_length)

        with open(key_file, 'rb') as f:
            key = f.read()

        print(f"[+] AES-{key_length} key loaded from {key_file}")
        return key

    def aes_encrypt(self, plaintext, key_length, mode_name):
        """
        AES Encryption
        Args:
            plaintext: str or bytes - data to encrypt
            key_length: int - 128 or 256
            mode_name: str - 'ECB' or 'CFB'
        """
        start_time = time.time()

        # Convert string to bytes if needed
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')

        # Load or generate key
        key = self.load_aes_key(key_length)

        # Generate IV for CFB mode
        iv = None
        if mode_name.upper() == 'CFB':
            iv = os.urandom(16)

        # Apply padding for ECB mode
        if mode_name.upper() == 'ECB':
            block_size = 16
            padding_length = block_size - (len(plaintext) % block_size)
            plaintext = plaintext + bytes([padding_length] * padding_length)

        # Create cipher
        if mode_name.upper() == 'ECB':
            cipher = Cipher(algorithms.AES(key), modes.ECB(),
                            backend=self.backend)
        elif mode_name.upper() == 'CFB':
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                            backend=self.backend)
        else:
            raise ValueError("Mode must be 'ECB' or 'CFB'")

        # Encrypt
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        # Save encrypted data
        output_file = self.output_dir / \
            f"aes_{key_length}_{mode_name.lower()}_encrypted.bin"
        with open(output_file, 'wb') as f:
            if iv:
                f.write(iv + ciphertext)  # Prepend IV for CFB
            else:
                f.write(ciphertext)

        elapsed_time = time.time() - start_time

        print(f"[+] Encryption completed in {elapsed_time:.6f} seconds")
        print(f"[+] Encrypted data saved to {output_file}")
        print(f"[+] Ciphertext length: {len(ciphertext)} bytes")

        # Store performance data
        self.performance_data.append({
            'operation': f'AES-{key_length}-{mode_name}-Encrypt',
            'key_bits': key_length,
            'time': elapsed_time,
            'data_size': len(plaintext)
        })

        return ciphertext, output_file

    def aes_decrypt(self, key_length, mode_name):
        """
        AES Decryption
        Reads encrypted file and decrypts it
        """
        start_time = time.time()

        # Load key
        key = self.load_aes_key(key_length)

        # Read encrypted file
        input_file = self.output_dir / \
            f"aes_{key_length}_{mode_name.lower()}_encrypted.bin"

        if not input_file.exists():
            print(f"[!] Encrypted file not found: {input_file}")
            return None

        with open(input_file, 'rb') as f:
            encrypted_data = f.read()

        # Extract IV for CFB mode
        iv = None
        ciphertext = encrypted_data
        if mode_name.upper() == 'CFB':
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]

        # Create cipher
        if mode_name.upper() == 'ECB':
            cipher = Cipher(algorithms.AES(key), modes.ECB(),
                            backend=self.backend)
        elif mode_name.upper() == 'CFB':
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                            backend=self.backend)

        # Decrypt
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding for ECB mode
        if mode_name.upper() == 'ECB':
            padding_length = plaintext[-1]
            plaintext = plaintext[:-padding_length]

        elapsed_time = time.time() - start_time

        print(f"[+] Decryption completed in {elapsed_time:.6f} seconds")
        print(
            f"[+] Decrypted text: {plaintext.decode('utf-8', errors='ignore')}")

        # Store performance data
        self.performance_data.append({
            'operation': f'AES-{key_length}-{mode_name}-Decrypt',
            'key_bits': key_length,
            'time': elapsed_time,
            'data_size': len(ciphertext)
        })

        return plaintext

    # ==================== RSA OPERATIONS ====================

    def generate_rsa_keypair(self, key_size=2048):
        """Generate and save RSA key pair"""
        start_time = time.time()

        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=self.backend
        )

        # Get public key
        public_key = private_key.public_key()

        # Serialize and save private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        private_key_file = self.keys_dir / f"rsa_{key_size}_private.pem"
        with open(private_key_file, 'wb') as f:
            f.write(private_pem)

        # Serialize and save public key
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        public_key_file = self.keys_dir / f"rsa_{key_size}_public.pem"
        with open(public_key_file, 'wb') as f:
            f.write(public_pem)

        elapsed_time = time.time() - start_time

        print(
            f"[+] RSA-{key_size} key pair generated in {elapsed_time:.6f} seconds")
        print(f"[+] Private key saved to {private_key_file}")
        print(f"[+] Public key saved to {public_key_file}")

        return private_key, public_key

    def load_rsa_keys(self, key_size=2048):
        """Load RSA key pair from files"""
        private_key_file = self.keys_dir / f"rsa_{key_size}_private.pem"
        public_key_file = self.keys_dir / f"rsa_{key_size}_public.pem"

        if not private_key_file.exists() or not public_key_file.exists():
            print(f"[!] RSA key files not found. Generating new key pair...")
            return self.generate_rsa_keypair(key_size)

        # Load private key
        with open(private_key_file, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=self.backend
            )

        # Load public key
        with open(public_key_file, 'rb') as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=self.backend
            )

        print(f"[+] RSA-{key_size} key pair loaded")
        return private_key, public_key

    def rsa_encrypt(self, plaintext, key_size=2048):
        """RSA Encryption"""
        start_time = time.time()

        # Convert string to bytes if needed
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')

        # Load keys
        _, public_key = self.load_rsa_keys(key_size)

        # Encrypt
        ciphertext = public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Save encrypted data
        output_file = self.output_dir / f"rsa_{key_size}_encrypted.bin"
        with open(output_file, 'wb') as f:
            f.write(ciphertext)

        elapsed_time = time.time() - start_time

        print(f"[+] RSA Encryption completed in {elapsed_time:.6f} seconds")
        print(f"[+] Encrypted data saved to {output_file}")
        print(f"[+] Ciphertext length: {len(ciphertext)} bytes")

        # Store performance data
        self.performance_data.append({
            'operation': f'RSA-{key_size}-Encrypt',
            'key_bits': key_size,
            'time': elapsed_time,
            'data_size': len(plaintext)
        })

        return ciphertext

    def rsa_decrypt(self, key_size=2048):
        """RSA Decryption"""
        start_time = time.time()

        # Load keys
        private_key, _ = self.load_rsa_keys(key_size)

        # Read encrypted file
        input_file = self.output_dir / f"rsa_{key_size}_encrypted.bin"

        if not input_file.exists():
            print(f"[!] Encrypted file not found: {input_file}")
            return None

        with open(input_file, 'rb') as f:
            ciphertext = f.read()

        # Decrypt
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        elapsed_time = time.time() - start_time

        print(f"[+] RSA Decryption completed in {elapsed_time:.6f} seconds")
        print(
            f"[+] Decrypted text: {plaintext.decode('utf-8', errors='ignore')}")

        # Store performance data
        self.performance_data.append({
            'operation': f'RSA-{key_size}-Decrypt',
            'key_bits': key_size,
            'time': elapsed_time,
            'data_size': len(ciphertext)
        })

        return plaintext

    # ==================== RSA SIGNATURE ====================

    def rsa_sign(self, message, key_size=2048):
        """Generate RSA signature for a message"""
        start_time = time.time()

        # Convert string to bytes if needed
        if isinstance(message, str):
            message = message.encode('utf-8')

        # Load private key
        private_key, _ = self.load_rsa_keys(key_size)

        # Sign
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Save signature
        signature_file = self.output_dir / f"rsa_{key_size}_signature.bin"
        with open(signature_file, 'wb') as f:
            f.write(signature)

        elapsed_time = time.time() - start_time

        print(f"[+] RSA Signature generated in {elapsed_time:.6f} seconds")
        print(f"[+] Signature saved to {signature_file}")
        print(f"[+] Signature length: {len(signature)} bytes")

        # Store performance data
        self.performance_data.append({
            'operation': f'RSA-{key_size}-Sign',
            'key_bits': key_size,
            'time': elapsed_time,
            'data_size': len(message)
        })

        return signature

    def rsa_verify(self, message, key_size=2048):
        """Verify RSA signature"""
        start_time = time.time()

        # Convert string to bytes if needed
        if isinstance(message, str):
            message = message.encode('utf-8')

        # Load public key
        _, public_key = self.load_rsa_keys(key_size)

        # Read signature file
        signature_file = self.output_dir / f"rsa_{key_size}_signature.bin"

        if not signature_file.exists():
            print(f"[!] Signature file not found: {signature_file}")
            return False

        with open(signature_file, 'rb') as f:
            signature = f.read()

        # Verify
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            elapsed_time = time.time() - start_time

            print(
                f"[+] Signature verification completed in {elapsed_time:.6f} seconds")
            print(f"[+] Signature is VALID ✓")

            # Store performance data
            self.performance_data.append({
                'operation': f'RSA-{key_size}-Verify',
                'key_bits': key_size,
                'time': elapsed_time,
                'data_size': len(message)
            })

            return True

        except InvalidSignature:
            print(f"[!] Signature is INVALID ✗")
            return False

    # ==================== SHA-256 HASHING ====================

    def sha256_hash(self, data):
        """Generate SHA-256 hash"""
        start_time = time.time()

        # Convert string to bytes if needed
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Generate hash
        hasher = hashlib.sha256()
        hasher.update(data)
        hash_value = hasher.hexdigest()

        elapsed_time = time.time() - start_time

        print(f"[+] SHA-256 hash generated in {elapsed_time:.6f} seconds")
        print(f"[+] Hash: {hash_value}")
        print(f"[+] Data size: {len(data)} bytes")

        # Store performance data
        self.performance_data.append({
            'operation': 'SHA256-Hash',
            'key_bits': 256,
            'time': elapsed_time,
            'data_size': len(data)
        })

        return hash_value

    def sha256_file(self, file_path):
        """Generate SHA-256 hash of a file"""
        start_time = time.time()

        file_path = Path(file_path)

        if not file_path.exists():
            print(f"[!] File not found: {file_path}")
            return None

        # Read and hash file
        hasher = hashlib.sha256()

        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)

        hash_value = hasher.hexdigest()
        file_size = file_path.stat().st_size

        elapsed_time = time.time() - start_time

        print(
            f"[+] SHA-256 hash of '{file_path.name}' generated in {elapsed_time:.6f} seconds")
        print(f"[+] Hash: {hash_value}")
        print(f"[+] File size: {file_size} bytes")

        # Store performance data
        self.performance_data.append({
            'operation': 'SHA256-File-Hash',
            'key_bits': 256,
            'time': elapsed_time,
            'data_size': file_size
        })

        return hash_value

    # ==================== PERFORMANCE MEASUREMENT ====================

    def save_performance_data(self):
        """Save performance data to JSON file"""
        output_file = self.output_dir / "performance_data.json"

        with open(output_file, 'w') as f:
            json.dump(self.performance_data, f, indent=2)

        print(f"\n[+] Performance data saved to {output_file}")

    def display_performance_summary(self):
        """Display summary of performance measurements"""
        if not self.performance_data:
            print("\n[!] No performance data available")
            return

        print("\n" + "="*70)
        print("PERFORMANCE SUMMARY")
        print("="*70)
        print(f"{'Operation':<30} {'Key Bits':<12} {'Time (s)':<15} {'Data Size'}")
        print("-"*70)

        for entry in self.performance_data:
            print(f"{entry['operation']:<30} {entry['key_bits']:<12} "
                  f"{entry['time']:<15.6f} {entry['data_size']} bytes")

        print("="*70)


def print_banner():
    """Print program banner"""
    print("\n" + "="*70)
    print(" " * 15 + "CRYPTOGRAPHY OPERATIONS PROGRAM")
    print(" " * 20 + "AES | RSA | SHA-256")
    print("="*70)


def print_menu():
    """Print main menu"""
    print("\n" + "-"*70)
    print("MAIN MENU")
    print("-"*70)
    print("1.  AES-128 ECB Encryption")
    print("2.  AES-128 ECB Decryption")
    print("3.  AES-128 CFB Encryption")
    print("4.  AES-128 CFB Decryption")
    print("5.  AES-256 ECB Encryption")
    print("6.  AES-256 ECB Decryption")
    print("7.  AES-256 CFB Encryption")
    print("8.  AES-256 CFB Decryption")
    print("9.  RSA Encryption")
    print("10. RSA Decryption")
    print("11. RSA Sign Message")
    print("12. RSA Verify Signature")
    print("13. SHA-256 Hash (Text)")
    print("14. SHA-256 Hash (File)")
    print("15. Generate AES Keys")
    print("16. Generate RSA Key Pair")
    print("17. View Performance Summary")
    print("18. Save Performance Data")
    print("0.  Exit")
    print("-"*70)


def main():
    """Main program function"""
    crypto = CryptoOperations()
    print_banner()

    while True:
        print_menu()

        try:
            choice = input("\nEnter your choice (0-18): ").strip()

            if choice == '0':
                print("\n[+] Exiting program. Goodbye!")
                break

            elif choice == '1':  # AES-128 ECB Encrypt
                text = input("Enter text to encrypt: ")
                crypto.aes_encrypt(text, 128, 'ECB')

            elif choice == '2':  # AES-128 ECB Decrypt
                crypto.aes_decrypt(128, 'ECB')

            elif choice == '3':  # AES-128 CFB Encrypt
                text = input("Enter text to encrypt: ")
                crypto.aes_encrypt(text, 128, 'CFB')

            elif choice == '4':  # AES-128 CFB Decrypt
                crypto.aes_decrypt(128, 'CFB')

            elif choice == '5':  # AES-256 ECB Encrypt
                text = input("Enter text to encrypt: ")
                crypto.aes_encrypt(text, 256, 'ECB')

            elif choice == '6':  # AES-256 ECB Decrypt
                crypto.aes_decrypt(256, 'ECB')

            elif choice == '7':  # AES-256 CFB Encrypt
                text = input("Enter text to encrypt: ")
                crypto.aes_encrypt(text, 256, 'CFB')

            elif choice == '8':  # AES-256 CFB Decrypt
                crypto.aes_decrypt(256, 'CFB')

            elif choice == '9':  # RSA Encrypt
                text = input("Enter text to encrypt: ")
                key_size = input(
                    "Enter RSA key size (1024/2048/3072/4096) [default: 2048]: ").strip()
                key_size = int(key_size) if key_size else 2048
                crypto.rsa_encrypt(text, key_size)

            elif choice == '10':  # RSA Decrypt
                key_size = input(
                    "Enter RSA key size (1024/2048/3072/4096) [default: 2048]: ").strip()
                key_size = int(key_size) if key_size else 2048
                crypto.rsa_decrypt(key_size)

            elif choice == '11':  # RSA Sign
                message = input("Enter message to sign: ")
                key_size = input(
                    "Enter RSA key size (1024/2048/3072/4096) [default: 2048]: ").strip()
                key_size = int(key_size) if key_size else 2048
                crypto.rsa_sign(message, key_size)

            elif choice == '12':  # RSA Verify
                message = input("Enter original message to verify: ")
                key_size = input(
                    "Enter RSA key size (1024/2048/3072/4096) [default: 2048]: ").strip()
                key_size = int(key_size) if key_size else 2048
                crypto.rsa_verify(message, key_size)

            elif choice == '13':  # SHA-256 Hash Text
                text = input("Enter text to hash: ")
                crypto.sha256_hash(text)

            elif choice == '14':  # SHA-256 Hash File
                file_path = input("Enter file path: ")
                crypto.sha256_file(file_path)

            elif choice == '15':  # Generate AES Keys
                print("\nGenerating AES keys...")
                crypto.generate_aes_key(128)
                crypto.generate_aes_key(256)

            elif choice == '16':  # Generate RSA Key Pair
                key_size = input(
                    "Enter RSA key size (1024/2048/3072/4096) [default: 2048]: ").strip()
                key_size = int(key_size) if key_size else 2048
                crypto.generate_rsa_keypair(key_size)

            elif choice == '17':  # View Performance Summary
                crypto.display_performance_summary()

            elif choice == '18':  # Save Performance Data
                crypto.save_performance_data()

            else:
                print("[!] Invalid choice. Please try again.")

        except KeyboardInterrupt:
            print("\n\n[!] Operation cancelled by user")
        except Exception as e:
            print(f"\n[!] Error: {str(e)}")

    # Save performance data before exit
    if crypto.performance_data:
        crypto.save_performance_data()


if __name__ == "__main__":
    main()
