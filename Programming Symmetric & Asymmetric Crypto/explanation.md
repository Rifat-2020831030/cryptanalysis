## Task 1: AES Encryption/Decryption 

### Approach
- Used Python's `cryptography` library for AES implementation
- Implemented both ECB and CFB modes with 128-bit and 256-bit keys
- Created functions for encryption and decryption

### Steps Taken
1. **Key Generation**: Generated random keys using `os.urandom()` and saved to files
2. **Padding**: Applied PKCS7 padding for ECB mode (block cipher requirement)
3. **IV Management**: Generated random 16-byte IV for CFB mode and stored with ciphertext
4. **Encryption**: Created cipher objects with appropriate mode and encrypted data
5. **File Storage**: Saved encrypted output to binary files
6. **Decryption**: Read encrypted files, extracted IV (for CFB), decrypted and removed padding

### Code Reference
```python
# Key generation
key = os.urandom(key_length // 8)

# ECB mode with PKCS7 padding
cipher = Cipher(algorithms.AES(key), modes.ECB())
padding_length = block_size - (len(plaintext) % block_size)
plaintext = plaintext + bytes([padding_length] * padding_length)

# CFB mode with IV
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
```

### Resources Used
- Python Cryptography Library: https://cryptography.io/en/latest/
- NIST FIPS 197 (AES Standard): https://csrc.nist.gov/publications/detail/fips/197/final

---

## Task 2: RSA Encryption/Decryption 

### Approach
- Implemented RSA with configurable key sizes (1024, 2048, 3072, 4096 bits)
- Used OAEP padding for security
- Stored keys in PEM format for portability

### Steps Taken
1. **Key Pair Generation**: Used `rsa.generate_private_key()` with public exponent 65537
2. **Key Serialization**: Saved private and public keys as PEM files
3. **OAEP Padding**: Applied Optimal Asymmetric Encryption Padding with SHA-256
4. **Encryption**: Used public key to encrypt plaintext
5. **File Storage**: Saved ciphertext to binary files
6. **Decryption**: Used private key with OAEP to decrypt

### Code Reference
```python
# Key generation
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=key_size,
    backend=self.backend
)

# Encryption with OAEP
ciphertext = public_key.encrypt(
    plaintext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
```

### Resources Used
- RFC 8017 (RSA Specifications): https://tools.ietf.org/html/rfc8017
- Python Cryptography - RSA: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

---

## Task 3: RSA Digital Signatures 

### Approach
- Implemented PSS (Probabilistic Signature Scheme) padding
- Created separate functions for signing and verification
- Stored signatures in binary files

### Steps Taken
1. **Signature Generation**: Used private key to sign message with PSS padding
2. **Hash Function**: Applied SHA-256 hashing before signing
3. **Salt**: Used maximum salt length for security
4. **File Storage**: Saved signature to binary file
5. **Verification**: Used public key to verify signature against original message
6. **Validation**: Caught `InvalidSignature` exception for tampered messages

### Code Reference
```python
# Signing
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Verification
public_key.verify(
    signature,
    message,
    padding.PSS(...),
    hashes.SHA256()
)
```

### Resources Used
- PSS Signature Scheme: Bellare & Rogaway (1996)
- Python Cryptography - Signatures: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#signing

---

## Task 4: SHA-256 Hashing 

### Approach
- Used Python's `hashlib` for SHA-256 implementation
- Created separate functions for text and file hashing
- Implemented chunked reading for memory efficiency

### Steps Taken
1. **Text Hashing**: Encoded string to bytes and applied SHA-256
2. **File Hashing**: Read files in 8KB chunks to handle large files
3. **Output Format**: Displayed hash in hexadecimal format
4. **Performance**: Tracked execution time for hashing operations

### Code Reference
```python
# Text hashing
hasher = hashlib.sha256()
hasher.update(data)
hash_value = hasher.hexdigest()

# File hashing with chunks
with open(file_path, 'rb') as f:
    while chunk := f.read(8192):
        hasher.update(chunk)
```

### Resources Used
- Python hashlib Documentation: https://docs.python.org/3/library/hashlib.html
- FIPS 180-4 (SHA Standard): https://csrc.nist.gov/publications/detail/fips/180/4/final

---

## Task 5: Performance Measurement

### Approach
- Added timer wrapper around all cryptographic operations
- Collected performance data in structured format
- Created benchmark suite with visualization

### Steps Taken
1. **Timer Implementation**: Used `time.time()` before and after operations
2. **Data Collection**: Stored operation name, key size, time, and data size
3. **Performance Tracking**: Created list to accumulate all measurements
4. **JSON Export**: Saved performance data for analysis
5. **Visualization**: Used matplotlib to generate comparison graphs
6. **Testing Matrix**:
   - AES: 5 data sizes (16, 64, 256, 1024, 4096 bytes)
   - RSA: 4 key sizes (1024, 2048, 3072, 4096 bits)


### Code Reference
```python
# Timer implementation
start_time = time.time()
# ... crypto operation ...
elapsed_time = time.time() - start_time

# Store performance data
self.performance_data.append({
    'operation': 'AES-256-CFB-Encrypt',
    'key_bits': 256,
    'time': elapsed_time,
    'data_size': len(plaintext)
})

# Visualization
plt.plot(key_sizes, encryption_times, marker='o')
plt.xlabel('Key Size (bits)')
plt.ylabel('Time (seconds)')
```

### Resources Used
- Matplotlib Documentation: https://matplotlib.org/
- Python time module: https://docs.python.org/3/library/time.html

---

## Implementation Highlights

### Architecture
- **Modular Design**: Single `CryptoOperations` class with 18 methods
- **Error Handling**: Try-catch blocks for all operations
- **User Interface**: Menu-driven command-line interface
- **Automatic Key Management**: Keys generated on first use and cached

### Performance Insights
- **AES**: Very fast (< 5ms), suitable for bulk data
- **RSA**: Slower (20-2000ms), use for key exchange only
- **Key Generation**: Most expensive RSA operation
- **Scaling**: AES scales linearly, RSA scales exponentially

---

## Tools & Libraries

### Primary Library
- **cryptography** (v43.0.1): Industry-standard cryptographic library
  - Source: https://cryptography.io/
  - Backend: OpenSSL
  - License: Apache/BSD

### Visualization
- **matplotlib** (v3.10.0): Graph generation
  - Source: https://matplotlib.org/

### Standard Library
- **hashlib**: SHA-256 hashing
- **time**: Performance measurement
- **pathlib**: File system operations
- **json**: Data serialization

---

## Challenges & Solutions

### Challenge 1: RSA Message Size Limit
- **Problem**: RSA can only encrypt limited data size
- **Solution**: Documented limitation, recommended hybrid encryption approach

### Challenge 2: Padding Management
- **Problem**: Different modes require different padding
- **Solution**: Mode-specific padding logic (PKCS7 for ECB, none for CFB)

### Challenge 3: IV Storage for CFB
- **Problem**: Decryption requires same IV as encryption
- **Solution**: Prepended IV to ciphertext in encrypted file

### Challenge 4: Performance Measurement
- **Problem**: Small operations complete too fast to measure accurately
- **Solution**: Used high-precision `time.time()` and tested with various data sizes

---

## References

1. **Python Cryptography Library**: https://cryptography.io/en/latest/
2. **Python hashlib**: https://docs.python.org/3/library/hashlib.html
3. **Matplotlib**: https://matplotlib.org/
4. **NIST FIPS 197 (AES)**: https://csrc.nist.gov/publications/detail/fips/197/final
5. **RFC 8017 (RSA)**: https://tools.ietf.org/html/rfc8017
6. **FIPS 180-4 (SHA)**: https://csrc.nist.gov/publications/detail/fips/180/4/final
7. **Java Cryptography Tutorial**: http://tutorials.jenkov.com/java-cryptography/index.html (conceptual reference)
8. **Python and Cryptography with PyCrypto**: https://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/ (initial guidance)

---
