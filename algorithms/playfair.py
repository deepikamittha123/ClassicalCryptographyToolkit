def generate_key_matrix(key):
    key = key.upper().replace("J", "I")

    matrix = []
    used = set()

    for ch in key:
        if ch.isalpha() and ch not in used:
            used.add(ch)
            matrix.append(ch)

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # J is omitted
        if ch not in used:
            used.add(ch)
            matrix.append(ch)

    return [matrix[i:i+5] for i in range(0, 25, 5)]


def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = "".join([c for c in text if c.isalpha()])

    prepared = ""
    i = 0

    while i < len(text):
        a = text[i]

        if i + 1 < len(text):
            b = text[i + 1]

            if a == b:
                prepared += a + "X"
                i += 1
            else:
                prepared += a + b
                i += 2
        else:
            prepared += a + "X"
            i += 1

    return prepared


def find_position(matrix, letter):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == letter:
                return i, j

    return None


def encrypt(text, matrix):
    cipher = ""

    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i + 1]

        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        # Same row
        if row1 == row2:
            cipher += matrix[row1][(col1 + 1) % 5]
            cipher += matrix[row2][(col2 + 1) % 5]

        # Same column
        elif col1 == col2:
            cipher += matrix[(row1 + 1) % 5][col1]
            cipher += matrix[(row2 + 1) % 5][col2]

        # Rectangle
        else:
            cipher += matrix[row1][col2]
            cipher += matrix[row2][col1]

    return cipher


def decrypt(cipher, matrix):
    plaintext = ""

    for i in range(0, len(cipher), 2):
        a = cipher[i]
        b = cipher[i + 1]

        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        # Same row
        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]

        # Same column
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]

        # Rectangle
        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]

    return plaintext