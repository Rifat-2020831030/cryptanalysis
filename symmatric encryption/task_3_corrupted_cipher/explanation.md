## Task 3: Corrupted Cipher Text Analysis

**Steps Taken:**

1. Created 128-byte plaintext with repeated patterns
2. Encrypted using 4 modes: ECB, CBC, CFB, OFB
3. Corrupted byte 30 by flipping 1 bit (XOR with 0x01)
4. Decrypted corrupted ciphertext with correct key and IV
5. Compared decrypted output with original plaintext
6. Calculated recovery rate (matched bytes / total bytes)
7. Identified affected 16-byte blocks

**Results:**

- **ECB:** 87.5% recovery (block 1 affected only)
- **CBC:** 87.5% recovery (blocks 1-2 affected)
- **CFB:** 86.7% recovery (blocks 1-2 affected)
- **OFB:** 99.2% recovery (only byte 30 affected)

**Key Observations:**

- OFB has minimal error propagation (best for noisy channels)
- ECB isolates errors to single block but is insecure
- CBC provides security with moderate error propagation

---
