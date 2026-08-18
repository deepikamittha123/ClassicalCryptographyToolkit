# One-Time Pad (OTP) Cipher - Encryption and Decryption

def encrypt(plain, key):
    plain = plain.upper()
    key = key.upper()

    cipher = ""

    for i in range(len(plain)):
        if plain[i].isalpha():
            p = ord(plain[i]) - ord('A')
            k = ord(key[i]) - ord('A')

            c = (p + k) % 26

            cipher += chr(c + ord('A'))
        else:
            cipher += plain[i]

    return cipher


def decrypt(cipher, key):
    cipher = cipher.upper()
    key = key.upper()

    plain = ""

    for i in range(len(cipher)):
        if cipher[i].isalpha():
            c = ord(cipher[i]) - ord('A')
            k = ord(key[i]) - ord('A')

            p = (c - k + 26) % 26

            plain += chr(p + ord('A'))
        else:
            plain += cipher[i]

    return plain