import random
import string
import tkinter as tk
from tkinter import messagebox

# Function to generate a password


def generate_password(length):
    password = []
    for i in range(length):
        password.append(random.choice(string.ascii_letters +
                        string.digits + string.punctuation))
    return ''.join(password)

# Function to validate input


def validate_input(input):
    try:
        int(input)
        return True
    except ValueError:
        messagebox.showerror(
            "Error", "Please enter a valid number for password length")
        return False

# Function to handle button click event


def generate_button_click():
    length = entry.get()
    if not validate_input(length):
        return
    elif int(length) < 4:
        messagebox.showerror(
            "Error", "Password length must be at least 4 characters")
    else:
        password = generate_password(int(length))
        with open('password.txt', 'w') as file:
            file.write(password)
        messagebox.showinfo(
            "Success", "Password generated and saved to password.txt")


# Create the GUI
window = tk.Tk()
window.title("Password Generator")
window.geometry("400x200")
window.configure(background="white")

label = tk.Label(window, text="Enter password length:")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Generate Password",
                   command=generate_button_click)
button.pack()

# Set the label font and size
label.config(font=("Arial", 12))

# Set the entry font and size
entry.config(font=("Arial", 12))

# Set the button font and size
button.config(font=("Arial", 12))

# Set the window size and position
window.geometry("400x200+500+200")

# Run the GUI
window.mainloop()
