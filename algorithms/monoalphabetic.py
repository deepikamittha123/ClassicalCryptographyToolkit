# Monoalphabetic Substitution Cipher

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def validate_key(key):
    key = key.upper().replace(" ", "")

    # Check length
    if len(key) != 26:
        raise ValueError(
            "Monoalphabetic key must contain exactly 26 letters."
        )

    # Check only alphabets
    if not key.isalpha():
        raise ValueError(
            "Monoalphabetic key must contain only letters A-Z."
        )

    # Check duplicate letters
    if len(set(key)) != 26:
        raise ValueError(
            "Monoalphabetic key must contain all 26 different letters."
        )

    return key


def encrypt(text, key):
    key = validate_key(key)

    result = ""

    for ch in text.upper():

        if ch in alphabet:
            result += key[alphabet.index(ch)]
        else:
            result += ch

    return result


def decrypt(text, key):
    key = validate_key(key)

    result = ""

    for ch in text.upper():

        if ch in key:
            result += alphabet[key.index(ch)]
        else:
            result += ch

    return result