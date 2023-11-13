import sqlite3
from tkinter import *
from tkinter import messagebox
import subprocess

# Create a SQLite database for user accounts
conn = sqlite3.connect('user_accounts.db')
c = conn.cursor()

# Create a user_accounts table
c.execute('''
    CREATE TABLE IF NOT EXISTS user_accounts (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        username TEXT,
        password TEXT
    )
''')
conn.commit()
conn.close()

def register():
    full_name = full_name_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not full_name or not username or not password:
        messagebox.showerror('Error', 'Please fill in all the fields')
    else:
        conn = sqlite3.connect('user_accounts.db')
        c = conn.cursor()

        # Check if the username already exists
        c.execute('SELECT * FROM user_accounts WHERE username = ?', (username,))
        user = c.fetchone()

        if user:
            messagebox.showerror('Error', 'Username already exists. Please choose another username.')
        else:
            # Insert the new user into the database
            c.execute('INSERT INTO user_accounts (full_name, username, password) VALUES (?, ?, ?)', (full_name, username, password))
            conn.commit()
            conn.close()

            messagebox.showinfo('Success', 'Registration successful. You can now login.')

            # Clear the registration fields
            full_name_entry.delete(0, END)
            username_entry.delete(0, END)
            password_entry.delete(0, END)

def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showerror('Error', 'Please fill in all the fields')
    else:
        conn = sqlite3.connect('user_accounts.db')
        c = conn.cursor()

        # Check if the username and password match a user in the database
        c.execute('SELECT * FROM user_accounts WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()

        conn.close()

        if user:
            # If the user is found, open main.py and pass the user ID as an argument
            subprocess.Popen(["python", "main.py", str(user[0])]) # Pass user ID as an argument
        else:
            messagebox.showerror('Error', 'Invalid username or password')
# Create the registration and login GUI
root = Tk()
root.title('Expense Tracker - Login')
root.configure(bg='#003399')

# Registration frame
Label(root, text='New to Expensemate? Register Now', bg='#003399', fg='white', font=("Arial", 18)).pack()
registration_frame = Frame(root)
registration_frame.pack()

Label(registration_frame, text='Full Name:').pack()
full_name_entry = Entry(registration_frame)
full_name_entry.pack()

Label(registration_frame, text='Username:').pack()
username_entry = Entry(registration_frame)
username_entry.pack()

Label(registration_frame, text='Password:').pack()
password_entry = Entry(registration_frame, show='*')
password_entry.pack()

register_button = Button(registration_frame, text='Register', command=register, bg="#27ae60", fg="white")
register_button.pack(pady=10)

# Login frame
Label(root, text='Existing User ? Login Now', bg='#003399', fg='white', font=("Arial", 18)).pack()
login_frame = Frame(root)
login_frame.pack()

Label(login_frame, text='Username:').pack()
login_username_entry = Entry(login_frame)
login_username_entry.pack()

Label(login_frame, text='Password:').pack()
login_password_entry = Entry(login_frame, show='*')
login_password_entry.pack()

login_button = Button(login_frame, text='Login', command=login, bg="#3498db", fg="white")
login_button.pack(pady=10)

root.mainloop()