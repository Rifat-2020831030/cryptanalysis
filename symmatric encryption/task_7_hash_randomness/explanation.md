## Task 7: Hash Randomness Test (Avalanche Effect)

**Steps Taken:**

1. Created original message (95 bytes)
2. Generated hash H1 using MD5 and SHA256
3. Modified message by flipping bit 0 of byte 10
4. Generated hash H2 for modified message
5. Compared H1 and H2 bit-by-bit
6. Counted number of different bits
7. Calculated percentage change

**Results:**

- **MD5:** 55/128 bits changed (42.97%)
- **SHA256:** 107/256 bits changed (41.80%)

**Key Observations:**

- Single bit flip → approximately 50% of output bits change
- Demonstrates strong avalanche effect
- Makes prediction impossible
- Critical security property for cryptographic hashes
- Prevents controlled manipulation attacks

---
