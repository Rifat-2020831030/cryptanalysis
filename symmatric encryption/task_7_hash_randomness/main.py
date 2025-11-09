"""
Task 7: Hash Randomness Test (Avalanche Effect)
Demonstrates the avalanche effect in cryptographic hash functions
"""

import hashlib


def run():
    """Task 7: Hash randomness test"""
    results = []

    # Create original message
    message = b"This is a test message to demonstrate the avalanche effect in cryptographic hash functions."

    with open('original.txt', 'wb') as f:
        f.write(message)

    # Test with MD5 and SHA256
    hash_algorithms = [
        ('MD5', hashlib.md5),
        ('SHA256', hashlib.sha256),
    ]

    for algo_name, algo_func in hash_algorithms:
        # Generate H1 (original)
        hasher1 = algo_func()
        hasher1.update(message)
        h1 = hasher1.digest()
        h1_hex = hasher1.hexdigest()

        # Flip one bit (flip bit 0 of byte 10)
        modified_message = bytearray(message)
        modified_message[10] ^= 0x01
        modified_message = bytes(modified_message)

        with open(f'modified_{algo_name.lower()}.txt', 'wb') as f:
            f.write(modified_message)

        # Generate H2 (modified)
        hasher2 = algo_func()
        hasher2.update(modified_message)
        h2 = hasher2.digest()
        h2_hex = hasher2.hexdigest()

        # Count bit differences
        total_bits = len(h1) * 8
        different_bits = 0

        for byte1, byte2 in zip(h1, h2):
            xor = byte1 ^ byte2
            different_bits += bin(xor).count('1')

        same_bits = total_bits - different_bits

        # Save results
        with open(f'analysis_{algo_name.lower()}.txt', 'w') as f:
            f.write(f"{algo_name} Hash Randomness Analysis\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"H1: {h1_hex}\n")
            f.write(f"H2: {h2_hex}\n\n")
            f.write(f"Total bits: {total_bits}\n")
            f.write(
                f"Same bits: {same_bits} ({100*same_bits/total_bits:.2f}%)\n")
            f.write(
                f"Different bits: {different_bits} ({100*different_bits/total_bits:.2f}%)\n")

        results.append({
            'algorithm': algo_name,
            'h1': h1_hex,
            'h2': h2_hex,
            'total_bits': total_bits,
            'same_bits': same_bits,
            'different_bits': different_bits,
            'change_percentage': 100 * different_bits / total_bits
        })

    return results


if __name__ == "__main__":
    results = run()
    for res in results:
        print(f"Algorithm: {res['algorithm']}")
        print(f"  H1: {res['h1']}")
        print(f"  H2: {res['h2']}")
        print(f"  Total bits: {res['total_bits']}")
        print(f"  Same bits: {res['same_bits']} ({100*res['same_bits']/res['total_bits']:.2f}%)")
        print(f"  Different bits: {res['different_bits']} ({res['change_percentage']:.2f}%)\n")
