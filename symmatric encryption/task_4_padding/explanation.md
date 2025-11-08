## Task 4: Padding Analysis

**Steps Taken:**

1. Created test plaintexts of different sizes:
   - 15 bytes (not multiple of 16)
   - 16 bytes (exact block size)
   - 17 bytes (1 byte over)
2. Encrypted each with ECB, CBC, CFB, OFB
3. Observed which modes added padding
4. Calculated output sizes for each mode

**Results:**

- **ECB & CBC:** Required PKCS7 padding
  - 15 bytes → 16 bytes (added 1 byte)
  - 16 bytes → 32 bytes (added 16 bytes)
  - 17 bytes → 32 bytes (added 15 bytes)
- **CFB & OFB:** No padding required
  - Output size = input size

**Key Observations:**

- Block ciphers must pad to block size multiples
- Stream cipher modes eliminate padding need
- PKCS7 adds N bytes of value N

---
