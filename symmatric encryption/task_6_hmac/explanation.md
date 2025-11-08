## Task 6: Keyed Hash and HMAC

**Steps Taken:**

1. Created test message for HMAC generation
2. Tested with 3 hash algorithms: MD5, SHA1, SHA256
3. Generated HMAC with 5 different key lengths:
   - 3 bytes (short key)
   - 7 bytes
   - 16 bytes
   - 32 bytes
   - 144 bytes (long key)
4. Saved HMAC outputs for each combination
5. Analyzed if key size is fixed

**Results:**

- All key lengths successfully generated HMACs
- Output length depends on hash algorithm, not key length
- Short keys: padded with zeros
- Long keys: hashed first, then padded

**Key Observations:**

- HMAC does NOT require fixed key size
- Recommended: key length ≥ hash output length
- Key entropy matters more than key length

---