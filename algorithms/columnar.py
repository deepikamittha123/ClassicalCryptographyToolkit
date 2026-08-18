import math


def encrypt(text, key_order):
    text = text.replace(" ", "").upper()

    cols = len(key_order)
    rows = math.ceil(len(text) / cols)

    # Create matrix and fill empty positions with X
    matrix = [['X' for _ in range(cols)] for _ in range(rows)]

    index = 0

    for i in range(rows):
        for j in range(cols):
            if index < len(text):
                matrix[i][j] = text[index]
                index += 1

    # Encrypt
    cipher = ""

    for num in range(1, cols + 1):
        col = key_order.index(num)

        for i in range(rows):
            cipher += matrix[i][col]

    return cipher


def decrypt(cipher, key_order):
    cipher = cipher.replace(" ", "").upper()

    cols = len(key_order)
    rows = math.ceil(len(cipher) / cols)

    matrix = [['' for _ in range(cols)] for _ in range(rows)]

    index = 0

    # Fill columns according to key order
    for num in range(1, cols + 1):
        col = key_order.index(num)

        for i in range(rows):
            if index < len(cipher):
                matrix[i][col] = cipher[index]
                index += 1

    # Read row-wise
    plain = ""

    for i in range(rows):
        for j in range(cols):
            plain += matrix[i][j]

    return plain.rstrip('X')