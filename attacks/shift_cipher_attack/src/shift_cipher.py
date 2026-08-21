# shift_cipher.py

def encrypt(text, key):
    result = ""

    for ch in text:
        if ch.isalpha():
            if ch.isupper():
                result += chr((ord(ch) - ord('A') + key) % 26 + ord('A'))
            else:
                result += chr((ord(ch) - ord('a') + key) % 26 + ord('a'))
        else:
            result += ch

    return result


def decrypt(text, key):
    return encrypt(text, -key)


# Simple testing
if __name__ == "__main__":

    plaintext = "Hello My code is 2024ucp1426"
    key = 3

    ciphertext = encrypt(plaintext, key)

    print("Plaintext :", plaintext)
    print("Key       :", key)
    print("Ciphertext:", ciphertext)
    print("Decrypted :", decrypt(ciphertext, key))