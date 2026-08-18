# Vigenere Cipher - Encryption and Decryption

def encrypt(plain, key):
    plain = plain.upper()
    key = key.upper()

    # Repeat the key to match plaintext length
    repeated_key = ""
    j = 0

    for i in range(len(plain)):
        if plain[i].isalpha():
            repeated_key += key[j % len(key)]
            j += 1
        else:
            repeated_key += plain[i]

    cipher = ""

    for i in range(len(plain)):
        if plain[i].isalpha():
            p = ord(plain[i]) - ord('A')
            k = ord(repeated_key[i]) - ord('A')

            c = (p + k) % 26

            cipher += chr(c + ord('A'))
        else:
            cipher += plain[i]

    return cipher


def decrypt(cipher, key):
    cipher = cipher.upper()
    key = key.upper()

    # Repeat the key to match ciphertext length
    repeated_key = ""
    j = 0

    for i in range(len(cipher)):
        if cipher[i].isalpha():
            repeated_key += key[j % len(key)]
            j += 1
        else:
            repeated_key += cipher[i]

    plain = ""

    for i in range(len(cipher)):
        if cipher[i].isalpha():
            c = ord(cipher[i]) - ord('A')
            k = ord(repeated_key[i]) - ord('A')

            p = (c - k + 26) % 26

            plain += chr(p + ord('A'))
        else:
            plain += cipher[i]

    return plain