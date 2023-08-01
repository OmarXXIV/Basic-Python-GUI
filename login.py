import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys

# Global variable to store the login credentials
login_credentials = {
    'username': 'admin',
    'password': 'password'
}


def create_account():
    # Implement your create account functionality here
    username = username_entry.get()
    password = password_entry.get()

    # Check if password meets the criteria
    if password:
        if len(password) < 8:
            messagebox.showerror('Account Creation Failed', 'Password must be at least 8 characters long.')
        elif not any(char.isdigit() for char in password):
            messagebox.showerror('Account Creation Failed', 'Password must contain at least one digit.')
        elif not any(char.isupper() for char in password):
            messagebox.showerror('Account Creation Failed', 'Password must contain at least one uppercase letter.')
        elif any(char in '!@#$%^&*()' for char in password):
            messagebox.showerror('Account Creation Failed', 'Password cannot contain special characters: !@#$%^&*().')
        else:
            login_credentials['username'] = username
            login_credentials['password'] = password
            messagebox.showinfo('Account Created', 'Account created successfully!')
    else:
        messagebox.showerror('Account Creation Failed', 'Invalid username or password.')


def login(event=None):
    username = username_entry.get()
    password = password_entry.get()

    if username == login_credentials['username'] and password == login_credentials['password']:
        messagebox.showinfo('Login Successful', 'Welcome!')
        login_window.destroy()
        open_cropper()
    else:
        messagebox.showerror('Login Failed', 'Invalid username or password')


def open_cropper():
    subprocess.Popen(['python', 'cropping.py'])
    sys.exit()  # Exit the script after opening the cropping script


# Create the login window using customtkinter
login_window = ctk.CTk()
login_window.title('Login')

# Calculate the screen width and height
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()

# Set the login window dimensions
window_width = 300
window_height = 250

# Calculate the position to center the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

login_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
login_window.protocol('WM_DELETE_WINDOW', sys.exit)  # Exit the script when the login window is closed

# Create login labels and entry fields
username_label = ctk.CTkLabel(login_window, text='Username:')
username_label.pack()
username_entry = ctk.CTkEntry(login_window)
username_entry.pack(pady=5)

password_label = ctk.CTkLabel(login_window, text='Password:')
password_label.pack()
password_entry = ctk.CTkEntry(login_window, show='*')
password_entry.pack(pady=5)

login_window.bind('<Return>', login)

# Create login and create account button
login_button = ctk.CTkButton(login_window, text='Login', command=login)
login_button.pack(pady=10)

create_button = ctk.CTkButton(login_window, text='Create Account', command=create_account)
create_button.pack(pady=10)

login_window.mainloop()
