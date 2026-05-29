# Secure Password Generator
<img src="https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />

## Overview

A desktop application built with Python and Tkinter that generates **cryptographically secure** random passwords of a user-specified length. Passwords are generated using Python's `secrets` module and copied to the clipboard for immediate use.

## Features

- Generates cryptographically secure passwords using the `secrets` module (a CSPRNG), not `random`.
- Enforces complexity: every password includes at least one lowercase letter, one uppercase letter, one digit, and one symbol.
- Validates user input and requires a minimum length of 4 characters.
- Copies the generated password directly to the clipboard — nothing is written to disk.
- Provides a simple graphical interface for easy interaction.

## Why `secrets` and not `random`

Python's `random` module uses the Mersenne Twister algorithm, which is fast but **predictable** — given enough output, its future values can be reconstructed, which makes it unsuitable for anything security-related. The `secrets` module is purpose-built for generating cryptographically strong values like passwords and tokens. For a password generator, this is the difference between "looks random" and "is secure," so this project uses `secrets` throughout.

## Usage

1. Run the script.
2. Enter the desired password length (minimum 4) in the input field.
3. Click **Generate Password**.

If the input is valid, a secure password is generated, shown in the window, and copied to your clipboard. Invalid input displays an error message.

## How It Works

### Password Generation

The password is built with `secrets.choice`, guaranteeing one character from each required class before filling the remaining length from the full character set. The result is then shuffled securely so the guaranteed characters aren't predictably positioned.

```python
import secrets
import string

def generate_password(length):
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
```

### Input Validation

`validate_input` confirms the entered length is a valid integer before generation. Non-numeric input triggers an error dialog.

```python
def validate_input(value):
    try:
        int(value)
        return True
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for password length")
        return False
```

### Button Click Event

When **Generate Password** is clicked, the input is validated and checked against the minimum length. A valid request generates the password, displays it, and copies it to the clipboard rather than writing it to a file.

```python
def generate_button_click():
    length = entry.get()
    if not validate_input(length):
        return

    length = int(length)
    if length < 4:
        messagebox.showerror("Error", "Password length must be at least 4 characters")
        return

    password = generate_password(length)
    result_var.set(password)
    window.clipboard_clear()
    window.clipboard_append(password)
    messagebox.showinfo("Success", "Password generated and copied to clipboard.")
```

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)

## Design Notes

- **No plaintext storage.** Earlier versions wrote the password to `password.txt`. Writing a freshly generated password to disk in plaintext — and especially committing it to a repository — undermines the security goal, so the app now copies to the clipboard instead.
- **CSPRNG by default.** All randomness comes from `secrets`, so output is suitable for real credential generation.

## Future Improvements

- **Password strength indicator** — display entropy or a strength rating for the generated password.
- **Adjustable character sets** — let the user toggle symbols or specify excluded characters for systems with input restrictions.
- **Passphrase mode** — offer word-based passphrases as an alternative to character strings.
- **Generate multiple at once** — produce a batch of passwords in a single action.

