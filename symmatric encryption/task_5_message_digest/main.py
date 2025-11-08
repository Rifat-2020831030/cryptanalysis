"""
Task 5: Generate Message Digests
Generates hash digests using multiple algorithms
"""

import hashlib


def run():
    """Task 5: Generate message digests"""
    results = []

    # Create a test file
    message = b"This is a test message for generating hash digests.\nWe will use multiple hashing algorithms."

    with open('message.txt', 'wb') as f:
        f.write(message)

    # Test different hash algorithms
    algorithms_to_test = [
        ('MD5', hashlib.md5),
        ('SHA1', hashlib.sha1),
        ('SHA256', hashlib.sha256),
        ('SHA512', hashlib.sha512),
        ('SHA3-256', hashlib.sha3_256),
    ]

    for algo_name, algo_func in algorithms_to_test:
        hasher = algo_func()
        hasher.update(message)
        digest = hasher.hexdigest()

        # Save to file
        with open(f'digest_{algo_name.lower().replace("-", "_")}.txt', 'w') as f:
            f.write(f"{algo_name}: {digest}\n")

        results.append({
            'algorithm': algo_name,
            'digest': digest,
            'length_bits': len(digest) * 4,
            'length_bytes': len(digest) // 2
        })

    return results


if __name__ == "__main__":
    results = run()
