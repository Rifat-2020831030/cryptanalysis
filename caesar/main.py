from pathlib import Path

base = Path(__file__).parent
cipher_path = base / "cipher_text.txt"
draft_path = base / "draft_output.txt"

cipher_text = cipher_path.read_text()

def caesar_decrypt(cipher_text, key):
    decrypted_txt = ""
    for ch in cipher_text:
        if 'a' <= ch <= 'z':
            decoded = chr(((ord(ch) - ord('a') - key) % 26) + ord('a'))
            decrypted_txt += decoded
        elif 'A' <= ch <= 'Z':
            decoded = chr(((ord(ch) - ord('A') - key) % 26) + ord('A'))
            decrypted_txt += decoded
        else:
            decrypted_txt += ch
    return decrypted_txt

def dry_run(cipher_text):
    with draft_path.open("w") as output_file:
        for key in range(1, 26):
            decrypted_message = caesar_decrypt(cipher_text, key)
            print(f"Key {key}: {decrypted_message}")
            output_file.write(f"Key {key}: {decrypted_message}\n")

dry_run(cipher_text)
result = caesar_decrypt(cipher_text, 10) 
with open("output.txt", "w") as output_file:
    output_file.write(result)