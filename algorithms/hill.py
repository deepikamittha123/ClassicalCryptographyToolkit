import numpy as np
from math import gcd


def text_to_numbers(text):
    return [ord(ch) - ord('A') for ch in text]


def numbers_to_text(numbers):
    return ''.join(
        chr(int(num) + ord('A'))
        for num in numbers
    )


def mod_inverse(a, m):
    a = a % m

    for x in range(1, m):
        if (a * x) % m == 1:
            return x

    raise ValueError(
        "Modular inverse does not exist."
    )


def inverse_matrix_mod26(key):

    a = int(key[0][0])
    b = int(key[0][1])
    c = int(key[1][0])
    d = int(key[1][1])

    determinant = (a * d - b * c) % 26

    if gcd(determinant, 26) != 1:
        raise ValueError(
            "Invalid Hill key. "
            "Determinant must be coprime with 26."
        )

    determinant_inverse = mod_inverse(
        determinant,
        26
    )

    inverse = np.array([
        [d, -b],
        [-c, a]
    ])

    inverse = (
        determinant_inverse * inverse
    ) % 26

    return inverse.astype(int)


def hill_encrypt(plaintext, key):

    plaintext = plaintext.upper()

    plaintext = ''.join(
        ch for ch in plaintext
        if ch.isalpha()
    )

    if len(plaintext) % 2 != 0:
        plaintext += "X"

    cipher = ""

    for i in range(0, len(plaintext), 2):

        pair = plaintext[i:i + 2]

        vector = np.array(
            text_to_numbers(pair)
        ).reshape(2, 1)

        result = np.dot(
            key,
            vector
        ) % 26

        cipher += numbers_to_text(
            result.flatten()
        )

    return cipher


def hill_decrypt(ciphertext, key):

    ciphertext = ciphertext.upper()

    ciphertext = ''.join(
        ch for ch in ciphertext
        if ch.isalpha()
    )

    inverse_key = inverse_matrix_mod26(key)

    plaintext = ""

    for i in range(0, len(ciphertext), 2):

        pair = ciphertext[i:i + 2]

        vector = np.array(
            text_to_numbers(pair)
        ).reshape(2, 1)

        result = np.dot(
            inverse_key,
            vector
        ) % 26

        plaintext += numbers_to_text(
            result.flatten()
        )

    return plaintext