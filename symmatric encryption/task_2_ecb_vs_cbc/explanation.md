## Task 2: ECB vs CBC Mode Comparison

**Steps Taken:**

1. Loaded `maskot.jpg` image file
2. Converted image to BMP format for easier manipulation
3. Extracted BMP header (first 54 bytes) - kept unchanged
4. Extracted pixel data (after byte 54)
5. Applied PKCS7 padding to pixel data
6. Encrypted pixel data using ECB mode with AES-128
7. Encrypted pixel data using CBC mode with AES-128
8. Replaced header back to each encrypted data
9. Saved as `encrypted_ecb.bmp` and `encrypted_cbc.bmp`
10. Compared visual results

**Key Observations:**

- ECB: Patterns in original image remain partially visible (INSECURE)
- CBC: Patterns completely obscured, appears random (SECURE)
- Same key and plaintext produce vastly different security levels

---
