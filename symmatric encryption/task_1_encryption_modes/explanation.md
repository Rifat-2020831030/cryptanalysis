## Task 1: AES Encryption Using Different Modes

**Steps Taken:**

1. Created plaintext message (168 bytes)
2. Generated encryption keys:
   - 128-bit key for AES-128
   - 256-bit key for AES-256
3. Generated initialization vector (IV) for modes requiring it
4. Encrypted plaintext using 6 different modes:
   - AES-128-CBC (with padding)
   - AES-128-CFB (no padding)
   - AES-256-ECB (with padding)
   - AES-128-OFB (no padding)
   - AES-256-CBC (with padding)
   - AES-128-CTR (no padding)
5. Applied PKCS7 padding for block cipher modes (CBC, ECB)
6. Decrypted each ciphertext to verify correctness
7. Saved encrypted outputs as `.bin` files

**Key Observations:**

- Block modes (CBC, ECB) required padding to 16-byte blocks
- Stream modes (CFB, OFB, CTR) handled any length without padding
- All encryptions verified successfully through decryption

---