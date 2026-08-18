# Rail Fence Cipher (Zigzag Pattern)

def encrypt(text, key):
    text = text.replace(" ", "").upper()

    rail = [['\n' for _ in range(len(text))] for _ in range(key)]

    row = 0
    direction = 1

    for col in range(len(text)):
        rail[row][col] = text[col]

        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1

        row += direction

    cipher = ""

    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                cipher += rail[i][j]

    return cipher


def decrypt(cipher, key):
    cipher = cipher.replace(" ", "").upper()

    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]

    row = 0
    direction = 1

    # Mark zigzag positions
    for col in range(len(cipher)):
        rail[row][col] = '*'

        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1

        row += direction

    # Fill marked positions with ciphertext
    index = 0

    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    # Read zigzag to obtain plaintext
    plain = ""

    row = 0
    direction = 1

    for col in range(len(cipher)):
        plain += rail[row][col]

        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1

        row += direction

    return plain