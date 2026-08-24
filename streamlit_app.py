import streamlit as st
import numpy as np
import time

from algorithms import caesar
from algorithms import monoalphabetic
from algorithms import playfair
from algorithms import hill
from algorithms import vigenere
from algorithms import otp
from algorithms import railfence
from algorithms import columnar

st.set_page_config(page_title="Classical Cryptography Toolkit", page_icon="🔐", layout="wide")

ALGORITHMS = [
    "Caesar Cipher", "Monoalphabetic Cipher", "Playfair Cipher",
    "Hill Cipher", "Vigenère Cipher", "One-Time Pad",
    "Rail Fence Cipher", "Columnar Transposition Cipher"
]

KEY_INSTRUCTIONS = {
    "Caesar Cipher": "Enter shift value (example: 5)",
    "Monoalphabetic Cipher": "Enter 26 unique letters (example: QWERTYUIOPASDFGHJKLZXCVBNM)",
    "Playfair Cipher": "Enter keyword (example: MONARCHY)",
    "Hill Cipher": "Enter 4 matrix values (example: 3 3 2 5)",
    "Vigenère Cipher": "Enter keyword (example: KEY)",
    "One-Time Pad": "Enter key with same length as plaintext",
    "Rail Fence Cipher": "Enter depth (example: 3)",
    "Columnar Transposition Cipher": "Enter column order (example: 43125)"
}

def validate_mono_key(key):
    key = key.upper().strip()
    if len(key) != 26:
        raise ValueError("Monoalphabetic key must contain exactly 26 letters.")
    if not key.isalpha():
        raise ValueError("Monoalphabetic key must contain letters only.")
    if len(set(key)) != 26:
        raise ValueError("Monoalphabetic key must contain 26 unique letters.")
    return key

def get_hill_matrix(key):
    values = key.replace(",", " ").split()
    if len(values) != 4:
        raise ValueError("Hill Cipher requires exactly 4 numbers.")
    try:
        values = [int(x) for x in values]
    except ValueError:
        raise ValueError("Hill key must contain numbers only.")
    matrix = np.array([[values[0], values[1]], [values[2], values[3]]])
    det = int(round(np.linalg.det(matrix)))
    if np.gcd(det, 26) != 1:
        raise ValueError("Invalid Hill key. Determinant must be relatively prime to 26.")
    return matrix

def get_columnar_key(key):
    key = key.strip()
    if not key.isdigit():
        raise ValueError("Columnar key must contain numbers only.")
    numbers = [int(x) for x in key]
    if sorted(numbers) != list(range(1, len(numbers) + 1)):
        raise ValueError("Column order must contain consecutive numbers starting from 1. Example: 43125")
    return numbers

def validate_vigenere_key(key):
    key = key.strip()
    if not key or not key.isalpha():
        raise ValueError("Vigenère key must contain letters only.")
    return key

def validate_playfair_key(key):
    key = key.strip()
    if not key or not key.isalpha():
        raise ValueError("Playfair key must contain letters only.")
    return key

def get_integer_key(key, name):
    try:
        value = int(key)
    except ValueError:
        raise ValueError(f"{name} key must be an integer.")
    if value <= 0:
        raise ValueError(f"{name} key must be greater than 0.")
    return value

def validate_otp_key(text, key):
    letters = "".join(ch for ch in text if ch.isalpha())
    clean_key = "".join(ch for ch in key.upper() if ch.isalpha())
    if len(clean_key) != len(letters):
        raise ValueError("OTP key must have the same number of letters as the plaintext/ciphertext.")
    return clean_key

def encrypt_text(algorithm, plaintext, key):
    if not plaintext:
        raise ValueError("Please enter plaintext.")
    start = time.perf_counter()

    if algorithm == "Caesar Cipher":
        result = caesar.encrypt(plaintext, get_integer_key(key, "Caesar"))
    elif algorithm == "Monoalphabetic Cipher":
        result = monoalphabetic.encrypt(plaintext, validate_mono_key(key))
    elif algorithm == "Playfair Cipher":
        matrix = playfair.generate_key_matrix(validate_playfair_key(key))
        result = playfair.encrypt(playfair.prepare_text(plaintext), matrix)
    elif algorithm == "Hill Cipher":
        result = hill.hill_encrypt(plaintext, get_hill_matrix(key))
    elif algorithm == "Vigenère Cipher":
        result = vigenere.encrypt(plaintext, validate_vigenere_key(key))
    elif algorithm == "One-Time Pad":
        clean = "".join(ch for ch in plaintext.upper() if ch.isalpha())
        result = otp.encrypt(clean, validate_otp_key(plaintext, key))
    elif algorithm == "Rail Fence Cipher":
        depth = get_integer_key(key, "Rail Fence")
        if depth < 2:
            raise ValueError("Rail Fence depth must be at least 2.")
        result = railfence.encrypt(plaintext, depth)
    elif algorithm == "Columnar Transposition Cipher":
        result = columnar.encrypt(plaintext, get_columnar_key(key))
    else:
        raise ValueError("Unknown algorithm.")

    return result, time.perf_counter() - start

def decrypt_text(algorithm, ciphertext, key):
    if not ciphertext:
        raise ValueError("Please enter ciphertext.")
    start = time.perf_counter()

    if algorithm == "Caesar Cipher":
        result = caesar.decrypt(ciphertext, get_integer_key(key, "Caesar"))
    elif algorithm == "Monoalphabetic Cipher":
        result = monoalphabetic.decrypt(ciphertext, validate_mono_key(key))
    elif algorithm == "Playfair Cipher":
        matrix = playfair.generate_key_matrix(validate_playfair_key(key))
        result = playfair.decrypt(ciphertext, matrix)
    elif algorithm == "Hill Cipher":
        k = get_hill_matrix(key)
        det = int(round(np.linalg.det(k))) % 26
        inv_det = pow(det, -1, 26)
        a, b = int(k[0,0]), int(k[0,1])
        c, d = int(k[1,0]), int(k[1,1])
        inverse = np.array([[d*inv_det, -b*inv_det], [-c*inv_det, a*inv_det]]) % 26
        result = hill.hill_decrypt(ciphertext, inverse)
    elif algorithm == "Vigenère Cipher":
        result = vigenere.decrypt(ciphertext, validate_vigenere_key(key))
    elif algorithm == "One-Time Pad":
        clean = "".join(ch for ch in ciphertext.upper() if ch.isalpha())
        result = otp.decrypt(clean, validate_otp_key(ciphertext, key))
    elif algorithm == "Rail Fence Cipher":
        depth = get_integer_key(key, "Rail Fence")
        if depth < 2:
            raise ValueError("Rail Fence depth must be at least 2.")
        result = railfence.decrypt(ciphertext, depth)
    elif algorithm == "Columnar Transposition Cipher":
        result = columnar.decrypt(ciphertext, get_columnar_key(key))
    else:
        raise ValueError("Unknown algorithm.")

    return result, time.perf_counter() - start

def compare_algorithms(plaintext):
    if not plaintext:
        raise ValueError("Enter plaintext first.")
    results = []

    tests = [
        ("Caesar Cipher", lambda: caesar.encrypt(plaintext, 5)),
        ("Monoalphabetic Cipher", lambda: monoalphabetic.encrypt(plaintext, "QWERTYUIOPASDFGHJKLZXCVBNM")),
        ("Playfair Cipher", lambda: playfair.encrypt(
            playfair.prepare_text(plaintext),
            playfair.generate_key_matrix("MONARCHY"))),
        ("Hill Cipher", lambda: hill.hill_encrypt(plaintext, np.array([[3,3],[2,5]]))),
        ("Vigenère Cipher", lambda: vigenere.encrypt(plaintext, "KEY")),
        ("Rail Fence Cipher", lambda: railfence.encrypt(plaintext, 3)),
        ("Columnar Transposition Cipher", lambda: columnar.encrypt(plaintext, [4,3,1,2,5]))
    ]

    letters = "".join(ch for ch in plaintext if ch.isalpha())
    if letters:
        tests.insert(5, ("One-Time Pad", lambda: otp.encrypt(letters, "A" * len(letters))))

    for name, func in tests:
        start = time.perf_counter()
        func()
        results.append((name, time.perf_counter() - start))

    results.sort(key=lambda x: x[1])
    return [{"Rank": i, "Algorithm": n, "Execution Time (seconds)": t}
            for i, (n, t) in enumerate(results, 1)]

def help_text():
    st.markdown("""
### 🔐 Algorithm Instructions

**Caesar:** shift value, e.g. `5`

**Monoalphabetic:** exactly 26 unique letters, e.g. `QWERTYUIOPASDFGHJKLZXCVBNM`

**Playfair:** keyword, e.g. `MONARCHY`

**Hill:** four numbers for a 2×2 matrix, e.g. `3 3 2 5`

**Vigenère:** keyword, e.g. `KEY`

**OTP:** key with the same number of letters as the plaintext

**Rail Fence:** depth, e.g. `3`

**Columnar:** column order, e.g. `43125`

File processing supports UTF-8 `.txt` files.
""")

st.title("🔐 Classical Cryptography Toolkit")
st.caption("Encryption • Decryption • File Processing • Algorithm Comparison")

with st.sidebar:
    st.header("⚙️ Settings")
    algorithm = st.selectbox("Select Algorithm", ALGORITHMS)
    st.info(KEY_INSTRUCTIONS[algorithm])
    st.markdown("---")
    st.write("Supports all 8 classical cryptographic algorithms.")

key = st.text_input("🔑 Key", placeholder=KEY_INSTRUCTIONS[algorithm])
plaintext = st.text_area("📝 Plain Text", height=180, placeholder="Enter plaintext here...")

c1, c2 = st.columns(2)
with c1:
    encrypt_clicked = st.button("🔒 Encrypt", use_container_width=True)
with c2:
    decrypt_clicked = st.button("🔓 Decrypt", use_container_width=True)

if encrypt_clicked:
    try:
        result, elapsed = encrypt_text(algorithm, plaintext, key)
        st.session_state["ciphertext"] = result
        st.session_state["decrypted"] = ""
        st.session_state["elapsed"] = elapsed
        st.success("Encryption successful.")
    except Exception as e:
        st.error(str(e))

ciphertext = st.text_area(
    "🔐 Encrypted / Cipher Text",
    value=st.session_state.get("ciphertext", ""),
    height=180
)

if decrypt_clicked:
    try:
        result, elapsed = decrypt_text(algorithm, ciphertext, key)
        st.session_state["decrypted"] = result
        st.session_state["elapsed"] = elapsed
        st.success("Decryption successful.")
    except Exception as e:
        st.error(str(e))

if st.session_state.get("ciphertext"):
    st.subheader("Encrypted Output")
    st.code(st.session_state["ciphertext"])

if st.session_state.get("decrypted"):
    st.subheader("Decrypted Output")
    st.code(st.session_state["decrypted"])

if "elapsed" in st.session_state:
    st.info(f"⏱️ Execution Time: {st.session_state['elapsed']:.8f} seconds")

st.markdown("---")
st.header("📁 File Encryption / Decryption")

uploaded = st.file_uploader("Upload a UTF-8 .txt file", type=["txt"])

fc1, fc2 = st.columns(2)
with fc1:
    encrypt_file_clicked = st.button("🔒 Encrypt File", use_container_width=True)
with fc2:
    decrypt_file_clicked = st.button("🔓 Decrypt File", use_container_width=True)

if encrypt_file_clicked:
    try:
        if uploaded is None:
            raise ValueError("Please upload a .txt file.")
        text = uploaded.getvalue().decode("utf-8")
        result, elapsed = encrypt_text(algorithm, text, key)
        st.success(f"File encrypted in {elapsed:.8f} seconds.")
        st.download_button(
            "⬇️ Download Encrypted File",
            result.encode("utf-8"),
            "encrypted_output.txt",
            "text/plain"
        )
    except Exception as e:
        st.error(str(e))

if decrypt_file_clicked:
    try:
        if uploaded is None:
            raise ValueError("Please upload a .txt file.")
        text = uploaded.getvalue().decode("utf-8")
        result, elapsed = decrypt_text(algorithm, text, key)
        st.success(f"File decrypted in {elapsed:.8f} seconds.")
        st.download_button(
            "⬇️ Download Decrypted File",
            result.encode("utf-8"),
            "decrypted_output.txt",
            "text/plain"
        )
    except Exception as e:
        st.error(str(e))

st.markdown("---")
st.header("📊 Compare Algorithms")

compare_clicked = st.button("📊 Compare All 8 Algorithms", use_container_width=True)

if compare_clicked:
    try:
        data = compare_algorithms(plaintext)
        st.dataframe(data, use_container_width=True, hide_index=True)
        st.success(
            f"Fastest: {data[0]['Algorithm']} "
            f"({data[0]['Execution Time (seconds)']:.8f} seconds)"
        )
    except Exception as e:
        st.error(str(e))

st.markdown("---")
with st.expander("❓ Help / Instructions"):
    help_text()

st.markdown("---")
st.caption("Classical Cryptography Toolkit | Educational Project")