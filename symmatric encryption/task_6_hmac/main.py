"""
Task 6: HMAC with Different Keys
Generates HMAC with various key lengths
"""

from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend


def run():
    """Task 6: HMAC with different keys"""
    backend = default_backend()
    results = []

    message = b"This is a test message for HMAC generation."

    with open('message.txt', 'wb') as f:
        f.write(message)

    # Test different keys with different lengths
    keys_to_test = [
        (b"abc", "3 bytes"),
        (b"abcdefg", "7 bytes"),
        (b"0123456789abcdef", "16 bytes"),
        (b"0123456789abcdef0123456789abcdef", "32 bytes"),
        (b"verylongkeythatisgreaterthan64bytes" * 2, "144 bytes"),
    ]

    hash_algorithms = [
        ('MD5', hashes.MD5),
        ('SHA256', hashes.SHA256),
        ('SHA1', hashes.SHA1),
    ]

    for algo_name, algo_class in hash_algorithms:
        algo_results = {'algorithm': algo_name, 'keys': []}

        for key, key_desc in keys_to_test:
            h = hmac.HMAC(key, algo_class(), backend=backend)
            h.update(message)
            mac = h.finalize()

            with open(f'hmac_{algo_name.lower()}_key{len(key)}.txt', 'w') as f:
                f.write(
                    f"HMAC-{algo_name} with {key_desc} key:\n{mac.hex()}\n")

            algo_results['keys'].append({
                'key_length': len(key),
                'key_description': key_desc,
                'hmac': mac.hex()
            })

        results.append(algo_results)

    return {
        'results': results,
        'conclusion': 'HMAC does NOT require a fixed key size. Keys of any length are accepted.'
    }


if __name__ == "__main__":
    result = run()
