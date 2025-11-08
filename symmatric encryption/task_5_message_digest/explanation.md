## Task 5: Generating Message Digest

**Steps Taken:**

1. Created test message (92 bytes)
2. Generated hash for 5 algorithms:
   - MD5 → 128 bits (32 hex chars)
   - SHA1 → 160 bits (40 hex chars)
   - SHA256 → 256 bits (64 hex chars)
   - SHA512 → 512 bits (128 hex chars)
   - SHA3-256 → 256 bits (64 hex chars)
3. Saved each digest to separate text file
4. Compared digest lengths and characteristics

**Key Observations:**

- Different algorithms produce different output lengths
- Same input always produces same output (deterministic)
- Cannot reverse hash to get original input (one-way)
- MD5 and SHA1 are deprecated due to collision vulnerabilities
- SHA256/SHA512/SHA3 are currently secure

---
