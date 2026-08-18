import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import numpy as np

# Import all cipher modules
from algorithms import caesar
from algorithms import monoalphabetic
from algorithms import playfair
from algorithms import hill
from algorithms import vigenere
from algorithms import otp
from algorithms import railfence
from algorithms import columnar


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Classical Cryptography Toolkit")
root.geometry("1000x850")
root.minsize(900, 750)


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#f2f2f2"
TITLE_COLOR = "#1f3c88"

root.configure(bg=BG_COLOR)


# ============================================================
# VARIABLES
# ============================================================

algorithm_var = tk.StringVar()

execution_time_var = tk.StringVar(
    value="Execution Time: -- seconds"
)


# ============================================================
# KEY INSTRUCTION FUNCTION
# ============================================================

def update_key_instruction(event=None):

    algorithm = algorithm_var.get()

    instructions = {

        "Caesar Cipher":
            "Enter shift value (example: 5)",

        "Monoalphabetic Cipher":
            "Enter 26 unique letters "
            "(example: QWERTYUIOPASDFGHJKLZXCVBNM)",

        "Playfair Cipher":
            "Enter keyword (example: MONARCHY)",

        "Hill Cipher":
            "Enter 4 matrix values "
            "(example: 3 3 2 5)",

        "Vigenère Cipher":
            "Enter keyword (example: KEY)",

        "One-Time Pad":
            "Enter key with same length as plaintext",

        "Rail Fence Cipher":
            "Enter depth (example: 3)",

        "Columnar Transposition Cipher":
            "Enter column order "
            "(example: 43125)"
    }

    key_instruction_label.config(
        text=instructions.get(
            algorithm,
            "Select an algorithm"
        )
    )


# ============================================================
# GET PLAINTEXT
# ============================================================

def get_plaintext():

    return plain_text_box.get(
        "1.0",
        tk.END
    ).strip()


# ============================================================
# GET KEY
# ============================================================

def get_key():

    return key_entry.get().strip()


# ============================================================
# DISPLAY PLAYFAIR MATRIX
# ============================================================

def display_playfair_matrix(matrix):

    # Clear previous matrix
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    matrix_title = tk.Label(
        matrix_frame,
        text="Playfair 5 × 5 Key Matrix",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR
    )

    matrix_title.grid(
        row=0,
        column=0,
        columnspan=5,
        pady=(0, 8)
    )

    for i in range(5):

        for j in range(5):

            label = tk.Label(
                matrix_frame,
                text=matrix[i][j],
                width=4,
                height=2,
                font=("Arial", 12, "bold"),
                relief="solid",
                bg="white"
            )

            label.grid(
                row=i + 1,
                column=j,
                padx=2,
                pady=2
            )


# ============================================================
# DISPLAY HILL MATRIX
# ============================================================

def display_hill_matrix(matrix):

    # Clear previous matrix
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    matrix_title = tk.Label(
        matrix_frame,
        text="Hill 2 × 2 Key Matrix",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR
    )

    matrix_title.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=(0, 8)
    )

    for i in range(2):

        for j in range(2):

            label = tk.Label(
                matrix_frame,
                text=str(matrix[i][j]),
                width=5,
                height=2,
                font=("Arial", 12, "bold"),
                relief="solid",
                bg="white"
            )

            label.grid(
                row=i + 1,
                column=j,
                padx=3,
                pady=3
            )


# ============================================================
# CLEAR MATRIX
# ============================================================

def clear_matrix():

    for widget in matrix_frame.winfo_children():
        widget.destroy()


# ============================================================
# ENCRYPT FUNCTION
# ============================================================

def encrypt_text():

    try:

        plaintext = get_plaintext()
        key = get_key()
        algorithm = algorithm_var.get()

        # Validation
        if not algorithm:

            messagebox.showerror(
                "Error",
                "Please select an algorithm."
            )

            return

        if not plaintext:

            messagebox.showerror(
                "Error",
                "Please enter plaintext."
            )

            return

        # Start execution timer
        start_time = time.perf_counter()

        # ====================================================
        # CAESAR
        # ====================================================

        if algorithm == "Caesar Cipher":

            if not key:
                raise ValueError(
                    "Please enter a shift value."
                )

            try:
                shift = int(key)

            except ValueError:
                raise ValueError(
                    "Caesar key must be an integer."
                )

            result = caesar.encrypt(
                plaintext,
                shift
            )

            clear_matrix()

        # ====================================================
        # MONOALPHABETIC
        # ====================================================

        elif algorithm == "Monoalphabetic Cipher":

            if not key:
                raise ValueError(
                    "Please enter a 26-letter key."
                )

            result = monoalphabetic.encrypt(
                plaintext,
                key
            )

            clear_matrix()

        # ====================================================
        # PLAYFAIR
        # ====================================================

        elif algorithm == "Playfair Cipher":

            if not key:
                raise ValueError(
                    "Please enter a Playfair keyword."
                )

            matrix = playfair.generate_key_matrix(
                key
            )

            prepared_text = playfair.prepare_text(
                plaintext
            )

            result = playfair.encrypt(
                prepared_text,
                matrix
            )

            display_playfair_matrix(
                matrix
            )

        # ====================================================
        # HILL
        # ====================================================

        elif algorithm == "Hill Cipher":

            if not key:
                raise ValueError(
                    "Please enter 4 matrix values."
                )

            # Accept:
            # 3 3 2 5
            # 3,3,2,5

            values = key.replace(
                ",",
                " "
            ).split()

            if len(values) != 4:

                raise ValueError(
                    "Hill key must contain exactly "
                    "4 numbers.\n\n"
                    "Example:\n"
                    "3 3 2 5"
                )

            try:

                values = [
                    int(value)
                    for value in values
                ]

            except ValueError:

                raise ValueError(
                    "Hill key must contain only numbers."
                )

            key_matrix = np.array([
                [values[0], values[1]],
                [values[2], values[3]]
            ])

            # Validate whether inverse exists
            hill.inverse_matrix_mod26(
                key_matrix
            )

            result = hill.hill_encrypt(
                plaintext,
                key_matrix
            )

            display_hill_matrix(
                key_matrix
            )

        # ====================================================
        # VIGENERE
        # ====================================================

        elif algorithm == "Vigenère Cipher":

            if not key:
                raise ValueError(
                    "Please enter a Vigenère keyword."
                )

            result = vigenere.encrypt(
                plaintext,
                key
            )

            clear_matrix()

        # ====================================================
        # OTP
        # ====================================================

        elif algorithm == "One-Time Pad":

            if not key:
                raise ValueError(
                    "Please enter an OTP key."
                )

            # Remove spaces for length validation
            plain_letters = "".join(
                ch for ch in plaintext
                if ch.isalpha()
            )

            key_letters = "".join(
                ch for ch in key
                if ch.isalpha()
            )

            if len(plain_letters) != len(key_letters):

                raise ValueError(
                    "OTP key must have the same "
                    "number of letters as plaintext."
                )

            result = otp.encrypt(
                plaintext,
                key
            )

            clear_matrix()

        # ====================================================
        # RAIL FENCE
        # ====================================================

        elif algorithm == "Rail Fence Cipher":

            if not key:
                raise ValueError(
                    "Please enter the depth."
                )

            try:
                depth = int(key)

            except ValueError:

                raise ValueError(
                    "Rail Fence depth must be an integer."
                )

            if depth < 2:

                raise ValueError(
                    "Rail Fence depth must be at least 2."
                )

            result = railfence.encrypt(
                plaintext,
                depth
            )

            clear_matrix()

        # ====================================================
        # COLUMNAR
        # ====================================================

        elif algorithm == "Columnar Transposition Cipher":

            if not key:
                raise ValueError(
                    "Please enter column order."
                )

            if not key.isdigit():

                raise ValueError(
                    "Column order must contain only numbers.\n\n"
                    "Example: 43125"
                )

            key_order = [
                int(x)
                for x in key
            ]

            # Check that numbers are continuous
            expected = list(
                range(
                    1,
                    len(key_order) + 1
                )
            )

            if sorted(key_order) != expected:

                raise ValueError(
                    "Column order must contain "
                    "each number from 1 to N exactly once.\n\n"
                    "Example: 43125"
                )

            result = columnar.encrypt(
                plaintext,
                key_order
            )

            clear_matrix()

        else:

            raise ValueError(
                "Unknown algorithm selected."
            )

        # End timer
        end_time = time.perf_counter()

        execution_time = (
            end_time - start_time
        )

        # Display encrypted result
        encrypted_text_box.delete(
            "1.0",
            tk.END
        )

        encrypted_text_box.insert(
            tk.END,
            result
        )

        # Update execution time
        execution_time_var.set(
            f"Execution Time: "
            f"{execution_time:.6f} seconds"
        )

    except Exception as e:

        messagebox.showerror(
            "Encryption Error",
            str(e)
        )


# ============================================================
# DECRYPT FUNCTION
# ============================================================

def decrypt_text():

    try:

        ciphertext = encrypted_text_box.get(
            "1.0",
            tk.END
        ).strip()

        key = get_key()
        algorithm = algorithm_var.get()

        if not algorithm:

            messagebox.showerror(
                "Error",
                "Please select an algorithm."
            )

            return

        if not ciphertext:

            messagebox.showerror(
                "Error",
                "Please enter or generate ciphertext."
            )

            return

        start_time = time.perf_counter()

        # ====================================================
        # CAESAR
        # ====================================================

        if algorithm == "Caesar Cipher":

            if not key:
                raise ValueError(
                    "Please enter a shift value."
                )

            shift = int(key)

            result = caesar.decrypt(
                ciphertext,
                shift
            )

        # ====================================================
        # MONOALPHABETIC
        # ====================================================

        elif algorithm == "Monoalphabetic Cipher":

            result = monoalphabetic.decrypt(
                ciphertext,
                key
            )

        # ====================================================
        # PLAYFAIR
        # ====================================================

        elif algorithm == "Playfair Cipher":

            matrix = playfair.generate_key_matrix(
                key
            )

            result = playfair.decrypt(
                ciphertext,
                matrix
            )

            display_playfair_matrix(
                matrix
            )

        # ====================================================
        # HILL
        # ====================================================

        elif algorithm == "Hill Cipher":

            values = key.replace(
                ",",
                " "
            ).split()

            if len(values) != 4:

                raise ValueError(
                    "Hill key must contain exactly "
                    "4 numbers."
                )

            values = [
                int(value)
                for value in values
            ]

            key_matrix = np.array([
                [values[0], values[1]],
                [values[2], values[3]]
            ])

            result = hill.hill_decrypt(
                ciphertext,
                key_matrix
            )

            display_hill_matrix(
                key_matrix
            )

        # ====================================================
        # VIGENERE
        # ====================================================

        elif algorithm == "Vigenère Cipher":

            result = vigenere.decrypt(
                ciphertext,
                key
            )

        # ====================================================
        # OTP
        # ====================================================

        elif algorithm == "One-Time Pad":

            result = otp.decrypt(
                ciphertext,
                key
            )

        # ====================================================
        # RAIL FENCE
        # ====================================================

        elif algorithm == "Rail Fence Cipher":

            depth = int(key)

            if depth < 2:

                raise ValueError(
                    "Rail Fence depth must be at least 2."
                )

            result = railfence.decrypt(
                ciphertext,
                depth
            )

        # ====================================================
        # COLUMNAR
        # ====================================================

        elif algorithm == "Columnar Transposition Cipher":

            if not key.isdigit():

                raise ValueError(
                    "Column order must contain only numbers."
                )

            key_order = [
                int(x)
                for x in key
            ]

            expected = list(
                range(
                    1,
                    len(key_order) + 1
                )
            )

            if sorted(key_order) != expected:

                raise ValueError(
                    "Column order must contain "
                    "each number from 1 to N exactly once."
                )

            result = columnar.decrypt(
                ciphertext,
                key_order
            )

        else:

            raise ValueError(
                "Unknown algorithm selected."
            )

        end_time = time.perf_counter()

        execution_time = (
            end_time - start_time
        )

        # Display decrypted result
        decrypted_text_box.delete(
            "1.0",
            tk.END
        )

        decrypted_text_box.insert(
            tk.END,
            result
        )

        execution_time_var.set(
            f"Execution Time: "
            f"{execution_time:.6f} seconds"
        )

    except Exception as e:

        messagebox.showerror(
            "Decryption Error",
            str(e)
        )


# ============================================================
# CLEAR FUNCTION
# ============================================================

def clear_all():

    plain_text_box.delete(
        "1.0",
        tk.END
    )

    key_entry.delete(
        0,
        tk.END
    )

    encrypted_text_box.delete(
        "1.0",
        tk.END
    )

    decrypted_text_box.delete(
        "1.0",
        tk.END
    )

    execution_time_var.set(
        "Execution Time: -- seconds"
    )

    clear_matrix()


# ============================================================
# OPEN FILE
# ============================================================

def open_file():

    filename = filedialog.askopenfilename(
        title="Open Text File",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if not filename:
        return

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        plain_text_box.delete(
            "1.0",
            tk.END
        )

        plain_text_box.insert(
            tk.END,
            content
        )

    except Exception as e:

        messagebox.showerror(
            "File Error",
            str(e)
        )


# ============================================================
# SAVE ENCRYPTED FILE
# ============================================================

def save_encrypted_file():

    content = encrypted_text_box.get(
        "1.0",
        tk.END
    ).strip()

    if not content:

        messagebox.showerror(
            "Error",
            "There is no encrypted text to save."
        )

        return

    filename = filedialog.asksaveasfilename(
        title="Save Encrypted File",
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if not filename:
        return

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        messagebox.showinfo(
            "Success",
            "Encrypted file saved successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "File Error",
            str(e)
        )


# ============================================================
# SAVE DECRYPTED FILE
# ============================================================

def save_decrypted_file():

    content = decrypted_text_box.get(
        "1.0",
        tk.END
    ).strip()

    if not content:

        messagebox.showerror(
            "Error",
            "There is no decrypted text to save."
        )

        return

    filename = filedialog.asksaveasfilename(
        title="Save Decrypted File",
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if not filename:
        return

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        messagebox.showinfo(
            "Success",
            "Decrypted file saved successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "File Error",
            str(e)
        )


# ============================================================
# HELP WINDOW
# ============================================================

def show_help():

    help_window = tk.Toplevel(root)

    help_window.title(
        "Cryptography Toolkit - Help"
    )

    help_window.geometry(
        "700x600"
    )

    help_window.configure(
        bg="white"
    )

    title = tk.Label(
        help_window,
        text="Classical Cryptography Toolkit - Help",
        font=("Arial", 18, "bold"),
        bg="white"
    )

    title.pack(
        pady=15
    )

    help_text = """
CLASSICAL CRYPTOGRAPHY TOOLKIT
==============================

This application implements eight classical
cryptographic algorithms.

1. CAESAR CIPHER
----------------
Key:
Enter an integer shift value.

Example:
5


2. MONOALPHABETIC CIPHER
------------------------
Key:
Enter exactly 26 unique alphabet letters.

Example:
QWERTYUIOPASDFGHJKLZXCVBNM


3. PLAYFAIR CIPHER
------------------
Key:
Enter a keyword.

Example:
MONARCHY

The Playfair cipher uses a 5 × 5 matrix.
I and J are normally treated as one character.


4. HILL CIPHER
--------------
Key:
Enter four numbers representing a 2 × 2 matrix.

Example:
3 3 2 5

This represents:

3 3
2 5

The matrix must have a valid modular inverse
modulo 26 for decryption.


5. VIGENERE CIPHER
------------------
Key:
Enter a keyword.

Example:
KEY


6. ONE-TIME PAD
---------------
Key:
The key must contain the same number of
letters as the plaintext.

Example:

Plaintext:
HELLO

Key:
XMCKL


7. RAIL FENCE CIPHER
--------------------
Key:
Enter the depth.

Example:
3


8. COLUMNAR TRANSPOSITION CIPHER
---------------------------------
Key:
Enter the column order.

Example:
43125


FILE OPERATIONS
===============

OPEN FILE
Loads a .txt file into the plaintext area.

SAVE ENCRYPTED
Saves encrypted text to a file.

SAVE DECRYPTED
Saves decrypted text to a file.


OTHER FEATURES
==============

ENCRYPT
Encrypts the plaintext using the selected algorithm.

DECRYPT
Decrypts the ciphertext.

CLEAR
Clears all input and output fields.

COMPARE ALGORITHMS
Compares the execution time of all eight
algorithms.

EXECUTION TIME
Displays the time required to perform
the encryption or decryption operation.
"""

    text_widget = tk.Text(
        help_window,
        wrap="word",
        font=("Arial", 11),
        padx=15,
        pady=15
    )

    text_widget.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    text_widget.insert(
        tk.END,
        help_text
    )

    text_widget.config(
        state="disabled"
    )


# ============================================================
# COMPARE ALGORITHMS
# ============================================================

def compare_algorithms():

    plaintext = get_plaintext()

    if not plaintext:

        messagebox.showerror(
            "Error",
            "Please enter plaintext before comparison."
        )

        return

    results = []

    # --------------------------------------------------------
    # Caesar
    # --------------------------------------------------------

    start = time.perf_counter()

    caesar.encrypt(
        plaintext,
        5
    )

    end = time.perf_counter()

    results.append(
        ("Caesar Cipher", end - start)
    )

    # --------------------------------------------------------
    # Monoalphabetic
    # --------------------------------------------------------

    mono_key = (
        "QWERTYUIOPASDFGHJKLZXCVBNM"
    )

    start = time.perf_counter()

    monoalphabetic.encrypt(
        plaintext,
        mono_key
    )

    end = time.perf_counter()

    results.append(
        ("Monoalphabetic", end - start)
    )

    # --------------------------------------------------------
    # Playfair
    # --------------------------------------------------------

    try:

        matrix = playfair.generate_key_matrix(
            "MONARCHY"
        )

        prepared = playfair.prepare_text(
            plaintext
        )

        # Playfair requires pairs
        if len(prepared) % 2 != 0:
            prepared += "X"

        start = time.perf_counter()

        playfair.encrypt(
            prepared,
            matrix
        )

        end = time.perf_counter()

        results.append(
            ("Playfair", end - start)
        )

    except Exception:

        results.append(
            ("Playfair", 0)
        )

    # --------------------------------------------------------
    # Hill
    # --------------------------------------------------------

    try:

        hill_key = np.array([
            [3, 3],
            [2, 5]
        ])

        start = time.perf_counter()

        hill.hill_encrypt(
            plaintext,
            hill_key
        )

        end = time.perf_counter()

        results.append(
            ("Hill", end - start)
        )

    except Exception:

        results.append(
            ("Hill", 0)
        )

    # --------------------------------------------------------
    # Vigenere
    # --------------------------------------------------------

    start = time.perf_counter()

    vigenere.encrypt(
        plaintext,
        "KEY"
    )

    end = time.perf_counter()

    results.append(
        ("Vigenère", end - start)
    )

    # --------------------------------------------------------
    # OTP
    # --------------------------------------------------------

    otp_plaintext = "".join(
        ch
        for ch in plaintext
        if ch.isalpha()
    )

    otp_key = "A" * len(
        otp_plaintext
    )

    start = time.perf_counter()

    otp.encrypt(
        otp_plaintext,
        otp_key
    )

    end = time.perf_counter()

    results.append(
        ("One-Time Pad", end - start)
    )

    # --------------------------------------------------------
    # Rail Fence
    # --------------------------------------------------------

    start = time.perf_counter()

    railfence.encrypt(
        plaintext,
        3
    )

    end = time.perf_counter()

    results.append(
        ("Rail Fence", end - start)
    )

    # --------------------------------------------------------
    # Columnar
    # --------------------------------------------------------

    # Use a key matching the number of columns
    columnar_key = [4, 3, 1, 2, 5]

    start = time.perf_counter()

    columnar.encrypt(
        plaintext,
        columnar_key
    )

    end = time.perf_counter()

    results.append(
        ("Columnar", end - start)
    )

    # Show result
    show_comparison_results(
        results
    )


# ============================================================
# SHOW COMPARISON RESULTS
# ============================================================

def show_comparison_results(results):

    comparison_window = tk.Toplevel(
        root
    )

    comparison_window.title(
        "Algorithm Performance Comparison"
    )

    comparison_window.geometry(
        "650x550"
    )

    comparison_window.configure(
        bg=BG_COLOR
    )

    title = tk.Label(
        comparison_window,
        text="Algorithm Execution Time",
        font=("Arial", 18, "bold"),
        bg=BG_COLOR
    )

    title.pack(
        pady=15
    )

    info = tk.Label(
        comparison_window,
        text=(
            "Execution time may vary depending "
            "on system hardware and input size."
        ),
        font=("Arial", 10),
        bg=BG_COLOR
    )

    info.pack(
        pady=5
    )

    tree_frame = tk.Frame(
        comparison_window,
        bg=BG_COLOR
    )

    tree_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    tree = ttk.Treeview(
        tree_frame,
        columns=(
            "Algorithm",
            "ExecutionTime"
        ),
        show="headings",
        height=12
    )

    tree.heading(
        "Algorithm",
        text="Algorithm"
    )

    tree.heading(
        "ExecutionTime",
        text="Execution Time (seconds)"
    )

    tree.column(
        "Algorithm",
        width=250,
        anchor="center"
    )

    tree.column(
        "ExecutionTime",
        width=250,
        anchor="center"
    )

    tree.pack(
        fill="both",
        expand=True
    )

    # Sort from fastest to slowest
    results_sorted = sorted(
        results,
        key=lambda x: x[1]
    )

    for algorithm, execution_time in results_sorted:

        tree.insert(
            "",
            tk.END,
            values=(
                algorithm,
                f"{execution_time:.8f}"
            )
        )


# ============================================================
# GUI LAYOUT
# ============================================================

# Main container
main_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    main_frame,
    text="CLASSICAL CRYPTOGRAPHY TOOLKIT",
    font=("Arial", 22, "bold"),
    fg=TITLE_COLOR,
    bg=BG_COLOR
)

title_label.pack(
    pady=(5, 2)
)


subtitle_label = tk.Label(
    main_frame,
    text="Encryption and Decryption using Classical Ciphers",
    font=("Arial", 11),
    bg=BG_COLOR
)

subtitle_label.pack(
    pady=(0, 15)
)


# ============================================================
# ALGORITHM SECTION
# ============================================================

algorithm_label = tk.Label(
    main_frame,
    text="Select Algorithm:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
)

algorithm_label.pack(
    anchor="w"
)


algorithm_dropdown = ttk.Combobox(
    main_frame,
    textvariable=algorithm_var,
    values=[
        "Caesar Cipher",
        "Monoalphabetic Cipher",
        "Playfair Cipher",
        "Hill Cipher",
        "Vigenère Cipher",
        "One-Time Pad",
        "Rail Fence Cipher",
        "Columnar Transposition Cipher"
    ],
    state="readonly",
    width=55
)

algorithm_dropdown.pack(
    pady=(3, 3)
)


# Connect dropdown
algorithm_dropdown.bind(
    "<<ComboboxSelected>>",
    update_key_instruction
)


# ============================================================
# KEY INSTRUCTION
# ============================================================

key_instruction_label = tk.Label(
    main_frame,
    text="Select an algorithm",
    font=("Arial", 9),
    fg="gray",
    bg=BG_COLOR,
    wraplength=700
)

key_instruction_label.pack(
    pady=(0, 8)
)


# ============================================================
# KEY SECTION
# ============================================================

key_label = tk.Label(
    main_frame,
    text="Key:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
)

key_label.pack(
    anchor="w"
)


key_entry = tk.Entry(
    main_frame,
    width=60,
    font=("Arial", 11)
)

key_entry.pack(
    pady=(3, 12)
)


# ============================================================
# MATRIX FRAME
# ============================================================

matrix_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

matrix_frame.pack(
    pady=5
)


# ============================================================
# PLAINTEXT
# ============================================================

plain_label = tk.Label(
    main_frame,
    text="Plain Text:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
)

plain_label.pack(
    anchor="w"
)


plain_text_box = tk.Text(
    main_frame,
    height=5,
    width=85,
    font=("Arial", 11),
    wrap="word"
)

plain_text_box.pack(
    pady=(3, 12)
)


# ============================================================
# ENCRYPTED TEXT
# ============================================================

encrypted_label = tk.Label(
    main_frame,
    text="Encrypted Text:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
)

encrypted_label.pack(
    anchor="w"
)


encrypted_text_box = tk.Text(
    main_frame,
    height=5,
    width=85,
    font=("Arial", 11),
    wrap="word"
)

encrypted_text_box.pack(
    pady=(3, 12)
)


# ============================================================
# DECRYPTED TEXT
# ============================================================

decrypted_label = tk.Label(
    main_frame,
    text="Decrypted Text:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
)

decrypted_label.pack(
    anchor="w"
)


decrypted_text_box = tk.Text(
    main_frame,
    height=5,
    width=85,
    font=("Arial", 11),
    wrap="word"
)

decrypted_text_box.pack(
    pady=(3, 12)
)


# ============================================================
# EXECUTION TIME
# ============================================================

execution_time_label = tk.Label(
    main_frame,
    textvariable=execution_time_var,
    font=("Arial", 10, "bold"),
    fg=TITLE_COLOR,
    bg=BG_COLOR
)

execution_time_label.pack(
    pady=5
)


# ============================================================
# MAIN BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

button_frame.pack(
    pady=10
)


# Encrypt button
encrypt_button = tk.Button(
    button_frame,
    text="ENCRYPT",
    command=encrypt_text,
    width=15,
    font=("Arial", 10, "bold")
)

encrypt_button.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


# Decrypt button
decrypt_button = tk.Button(
    button_frame,
    text="DECRYPT",
    command=decrypt_text,
    width=15,
    font=("Arial", 10, "bold")
)

decrypt_button.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


# Clear button
clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_all,
    width=15,
    font=("Arial", 10, "bold")
)

clear_button.grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)


# Exit button
exit_button = tk.Button(
    button_frame,
    text="EXIT",
    command=root.destroy,
    width=15,
    font=("Arial", 10, "bold")
)

exit_button.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)


# ============================================================
# FILE BUTTON FRAME
# ============================================================

file_button_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

file_button_frame.pack(
    pady=5
)


# Open file
open_file_button = tk.Button(
    file_button_frame,
    text="OPEN FILE",
    command=open_file,
    width=18,
    font=("Arial", 10)
)

open_file_button.grid(
    row=0,
    column=0,
    padx=5
)


# Save encrypted
save_encrypted_button = tk.Button(
    file_button_frame,
    text="SAVE ENCRYPTED",
    command=save_encrypted_file,
    width=18,
    font=("Arial", 10)
)

save_encrypted_button.grid(
    row=0,
    column=1,
    padx=5
)


# Save decrypted
save_decrypted_button = tk.Button(
    file_button_frame,
    text="SAVE DECRYPTED",
    command=save_decrypted_file,
    width=18,
    font=("Arial", 10)
)

save_decrypted_button.grid(
    row=0,
    column=2,
    padx=5
)


# ============================================================
# EXTRA BUTTON FRAME
# ============================================================

extra_button_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

extra_button_frame.pack(
    pady=8
)


# Compare algorithms
compare_button = tk.Button(
    extra_button_frame,
    text="COMPARE ALGORITHMS",
    command=compare_algorithms,
    width=22,
    font=("Arial", 10, "bold")
)

compare_button.grid(
    row=0,
    column=0,
    padx=5
)


# Help
help_button = tk.Button(
    extra_button_frame,
    text="HELP",
    command=show_help,
    width=15,
    font=("Arial", 10, "bold")
)

help_button.grid(
    row=0,
    column=1,
    padx=5
)


# ============================================================
# INITIAL GUI STATE
# ============================================================

algorithm_dropdown.current(0)

update_key_instruction()


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()