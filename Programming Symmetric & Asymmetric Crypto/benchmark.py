"""
Performance Benchmark Script
Measures execution time as a function of key size for AES and RSA operations

"""

import os
import time
import matplotlib.pyplot as plt
from pathlib import Path
from crypto_program import CryptoOperations


def benchmark_aes():
    """Benchmark AES encryption/decryption with different key sizes"""
    crypto = CryptoOperations()

    # Test data of different sizes
    test_sizes = [16, 64, 256, 1024, 4096]  # bytes
    key_lengths = [128, 256]
    modes = ['ECB', 'CFB']

    results = {
        'key_length': [],
        'data_size': [],
        'mode': [],
        'encrypt_time': [],
        'decrypt_time': []
    }

    print("\n" + "="*70)
    print("AES PERFORMANCE BENCHMARK")
    print("="*70)

    for key_length in key_lengths:
        for mode in modes:
            for data_size in test_sizes:
                # Generate test data
                test_data = os.urandom(data_size)

                print(
                    f"\n[*] Testing AES-{key_length} {mode} with {data_size} bytes...")

                # Encrypt
                start = time.time()
                crypto.aes_encrypt(test_data, key_length, mode)
                encrypt_time = time.time() - start

                # Decrypt
                start = time.time()
                crypto.aes_decrypt(key_length, mode)
                decrypt_time = time.time() - start

                results['key_length'].append(key_length)
                results['data_size'].append(data_size)
                results['mode'].append(mode)
                results['encrypt_time'].append(encrypt_time)
                results['decrypt_time'].append(decrypt_time)

                print(f"    Encryption: {encrypt_time:.6f}s")
                print(f"    Decryption: {decrypt_time:.6f}s")

    return results


def benchmark_rsa():
    """Benchmark RSA operations with different key sizes"""
    crypto = CryptoOperations()

    # Different RSA key sizes
    key_sizes = [1024, 2048, 3072, 4096]

    # Test message (must be smaller than key size - padding)
    test_message = b"This is a test message for RSA encryption benchmark."

    results = {
        'key_size': [],
        'keygen_time': [],
        'encrypt_time': [],
        'decrypt_time': [],
        'sign_time': [],
        'verify_time': []
    }

    print("\n" + "="*70)
    print("RSA PERFORMANCE BENCHMARK")
    print("="*70)

    for key_size in key_sizes:
        print(f"\n[*] Testing RSA-{key_size}...")

        # Key generation
        start = time.time()
        crypto.generate_rsa_keypair(key_size)
        keygen_time = time.time() - start
        print(f"    Key Generation: {keygen_time:.6f}s")

        # Encryption
        start = time.time()
        crypto.rsa_encrypt(test_message, key_size)
        encrypt_time = time.time() - start
        print(f"    Encryption: {encrypt_time:.6f}s")

        # Decryption
        start = time.time()
        crypto.rsa_decrypt(key_size)
        decrypt_time = time.time() - start
        print(f"    Decryption: {decrypt_time:.6f}s")

        # Signing
        start = time.time()
        crypto.rsa_sign(test_message, key_size)
        sign_time = time.time() - start
        print(f"    Signing: {sign_time:.6f}s")

        # Verification
        start = time.time()
        crypto.rsa_verify(test_message, key_size)
        verify_time = time.time() - start
        print(f"    Verification: {verify_time:.6f}s")

        results['key_size'].append(key_size)
        results['keygen_time'].append(keygen_time)
        results['encrypt_time'].append(encrypt_time)
        results['decrypt_time'].append(decrypt_time)
        results['sign_time'].append(sign_time)
        results['verify_time'].append(verify_time)

    return results


def plot_aes_results(results):
    """Plot AES benchmark results"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot for AES-128
    aes128_ecb_encrypt = [results['encrypt_time'][i] for i in range(len(results['key_length']))
                          if results['key_length'][i] == 128 and results['mode'][i] == 'ECB']
    aes128_cfb_encrypt = [results['encrypt_time'][i] for i in range(len(results['key_length']))
                          if results['key_length'][i] == 128 and results['mode'][i] == 'CFB']

    aes256_ecb_encrypt = [results['encrypt_time'][i] for i in range(len(results['key_length']))
                          if results['key_length'][i] == 256 and results['mode'][i] == 'ECB']
    aes256_cfb_encrypt = [results['encrypt_time'][i] for i in range(len(results['key_length']))
                          if results['key_length'][i] == 256 and results['mode'][i] == 'CFB']

    data_sizes = [16, 64, 256, 1024, 4096]

    ax1.plot(data_sizes, aes128_ecb_encrypt, marker='o', label='AES-128 ECB')
    ax1.plot(data_sizes, aes128_cfb_encrypt, marker='s', label='AES-128 CFB')
    ax1.plot(data_sizes, aes256_ecb_encrypt, marker='^', label='AES-256 ECB')
    ax1.plot(data_sizes, aes256_cfb_encrypt, marker='d', label='AES-256 CFB')

    ax1.set_xlabel('Data Size (bytes)')
    ax1.set_ylabel('Encryption Time (seconds)')
    ax1.set_title('AES Encryption Performance')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')

    # Plot decryption times
    aes128_ecb_decrypt = [results['decrypt_time'][i] for i in range(len(results['key_length']))
                          if results['key_length'][i] == 128 and results['mode'][i] == 'ECB']
    aes128_cfb_decrypt = [results['decrypt_time'][i] for i in range(len(results['key_length']))
                          if results['key_length'][i] == 128 and results['mode'][i] == 'CFB']

    aes256_ecb_decrypt = [results['decrypt_time'][i] for i in range(len(results['key_length']))
                          if results['key_length'][i] == 256 and results['mode'][i] == 'ECB']
    aes256_cfb_decrypt = [results['decrypt_time'][i] for i in range(len(results['key_length']))
                          if results['key_length'][i] == 256 and results['mode'][i] == 'CFB']

    ax2.plot(data_sizes, aes128_ecb_decrypt, marker='o', label='AES-128 ECB')
    ax2.plot(data_sizes, aes128_cfb_decrypt, marker='s', label='AES-128 CFB')
    ax2.plot(data_sizes, aes256_ecb_decrypt, marker='^', label='AES-256 ECB')
    ax2.plot(data_sizes, aes256_cfb_decrypt, marker='d', label='AES-256 CFB')

    ax2.set_xlabel('Data Size (bytes)')
    ax2.set_ylabel('Decryption Time (seconds)')
    ax2.set_title('AES Decryption Performance')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')

    plt.tight_layout()
    plt.savefig('output/aes_performance.png', dpi=300, bbox_inches='tight')
    print("\n[+] AES performance graph saved to output/aes_performance.png")
    plt.close()


def plot_rsa_results(results):
    """Plot RSA benchmark results"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    key_sizes = results['key_size']

    # Key Generation
    ax1.plot(key_sizes, results['keygen_time'],
             marker='o', color='blue', linewidth=2)
    ax1.set_xlabel('Key Size (bits)')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('RSA Key Generation Time')
    ax1.grid(True, alpha=0.3)

    # Encryption
    ax2.plot(key_sizes, results['encrypt_time'],
             marker='s', color='green', linewidth=2)
    ax2.set_xlabel('Key Size (bits)')
    ax2.set_ylabel('Time (seconds)')
    ax2.set_title('RSA Encryption Time')
    ax2.grid(True, alpha=0.3)

    # Decryption
    ax3.plot(key_sizes, results['decrypt_time'],
             marker='^', color='red', linewidth=2)
    ax3.set_xlabel('Key Size (bits)')
    ax3.set_ylabel('Time (seconds)')
    ax3.set_title('RSA Decryption Time')
    ax3.grid(True, alpha=0.3)

    # Signing and Verification
    ax4.plot(key_sizes, results['sign_time'],
             marker='d', label='Signing', linewidth=2)
    ax4.plot(key_sizes, results['verify_time'],
             marker='*', label='Verification', linewidth=2)
    ax4.set_xlabel('Key Size (bits)')
    ax4.set_ylabel('Time (seconds)')
    ax4.set_title('RSA Signing & Verification Time')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('output/rsa_performance.png', dpi=300, bbox_inches='tight')
    print("[+] RSA performance graph saved to output/rsa_performance.png")
    plt.close()


def main():
    """Main benchmark function"""
    print("\n" + "="*70)
    print(" " * 15 + "CRYPTOGRAPHY PERFORMANCE BENCHMARK")
    print("="*70)

    # Benchmark AES
    aes_results = benchmark_aes()
    plot_aes_results(aes_results)

    # Benchmark RSA
    rsa_results = benchmark_rsa()
    plot_rsa_results(rsa_results)

    print("\n" + "="*70)
    print("BENCHMARK COMPLETED")
    print("="*70)
    print("\n[+] Results have been saved as graphs in the 'output' directory")
    print("[+] Check 'aes_performance.png' and 'rsa_performance.png'")


if __name__ == "__main__":
    main()
