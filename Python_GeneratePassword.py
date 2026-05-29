"""
Secure Password Generator
Generates cryptographically secure random passwords using Python's `secrets`
module (not `random`, which is predictable and unsuitable for security use).

Enforces complexity: every generated password contains at least one lowercase
letter, one uppercase letter, one digit, and one symbol.
"""

import secrets
import string
import tkinter as tk
from tkinter import messagebox


def generate_password(length):
    """Generate a cryptographically secure password of the given length.

    Uses secrets.choice (CSPRNG) and guarantees at least one character from
    each class, then shuffles so the required characters aren't predictably
    placed at the front.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 to satisfy complexity rules.")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    all_chars = lowercase + uppercase + digits + symbols

    # Guarantee one of each required class.
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]

    # Fill the rest from the full set.
    password += [secrets.choice(all_chars) for _ in range(length - 4)]

    # Shuffle securely so the guaranteed characters aren't always first.
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def validate_input(value):
    """Return True if value is a valid integer length, else show an error."""
    try:
        int(value)
        return True
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for password length")
        return False


def generate_button_click():
    length = entry.get()
    if not validate_input(length):
        return

    length = int(length)
    if length < 4:
        messagebox.showerror("Error", "Password length must be at least 4 characters")
        return

    password = generate_password(length)

    # Show the result in the GUI and copy to clipboard instead of writing it
    # to a file. Writing passwords to disk (and especially committing them to
    # a repo) defeats the purpose of generating a strong one.
    result_var.set(password)
    window.clipboard_clear()
    window.clipboard_append(password)
    messagebox.showinfo("Success", "Password generated and copied to clipboard.")


# ----- GUI -----
window = tk.Tk()
window.title("Secure Password Generator")
window.geometry("420x220+500+200")
window.configure(background="white")

label = tk.Label(window, text="Enter password length (min 4):", background="white")
label.config(font=("Arial", 12))
label.pack(pady=(16, 4))

entry = tk.Entry(window, font=("Arial", 12))
entry.pack()

button = tk.Button(window, text="Generate Password", command=generate_button_click, font=("Arial", 12))
button.pack(pady=10)

result_var = tk.StringVar()
result_entry = tk.Entry(window, textvariable=result_var, font=("Consolas", 11), width=36, justify="center")
result_entry.pack(pady=6)

window.mainloop()
