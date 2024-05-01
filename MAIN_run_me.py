import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector as sql
import datetime as dt
from menu import RoyalBankApp1

class RoyalBankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Royal Bank")
        self.geometry("600x400")
        self.configure(bg="#F0EAD6")  # Set a background color
        self.create_widgets()  # Call method to create the widgets
        self.conn = sql.connect(host="localhost", user="root", passwd="root@123", database="the_royal_bank")
        self.mycursor = self.conn.cursor()
        print("========================================================== <<<<<<<<<<  WELCOME TO THE ROYAL BANK  >>>>>>>>>> ==========================================================")
        print(dt.datetime.now())

    def create_widgets(self):
        # Create a title label
        self.title_label = tk.Label(self, text="Welcome to The Royal Bank", font=("Arial", 16, "bold"), fg="navy", bg="#F0EAD6")
        self.title_label.pack(pady=10)

        # Create choice selection menu
        self.menu_frame = tk.Frame(self, bg="#F0EAD6")
        self.menu_frame.pack(pady=10)

        self.choice_var = tk.IntVar()  # Variable to store user choice

        # Radio buttons for menu options
        self.radio1 = tk.Radiobutton(self.menu_frame, text="Register", variable=self.choice_var, value=1, bg="#F0EAD6")
        self.radio1.grid(row=0, column=0, padx=10)

        self.radio2 = tk.Radiobutton(self.menu_frame, text="Login", variable=self.choice_var, value=2, bg="#F0EAD6")
        self.radio2.grid(row=0, column=1, padx=10)

        self.radio3 = tk.Radiobutton(self.menu_frame, text="Change Username/Password", variable=self.choice_var, value=3, bg="#F0EAD6")
        self.radio3.grid(row=0, column=2, padx=10)

        self.radio4 = tk.Radiobutton(self.menu_frame, text="Exit", variable=self.choice_var, value=4, bg="#F0EAD6")
        self.radio4.grid(row=0, column=3, padx=10)

        # Submit button to handle choices
        self.submit_button = tk.Button(self, text="Submit", command=self.handle_choice, bg="navy", fg="white", font=("Arial", 12, "bold"))
        self.submit_button.pack(pady=10)

        # Message label for feedback
        self.message_label = tk.Label(self, font=("Arial", 12), bg="#F0EAD6")
        self.message_label.pack(pady=10)

    def handle_choice(self):
        choice = self.choice_var.get()

        if choice == 1:
            self.handle_register()
        elif choice == 2:
            self.handle_login()
        elif choice == 3:
            self.handle_change_credentials()
        elif choice == 4:
            self.quit()
        else:
            self.message_label.config(text="Invalid choice. Please try again.", fg="red")

    def handle_register(self):
        # Create a new window for registration
        register_window = tk.Toplevel(self)
        register_window.title("Register")
        register_window.geometry("400x300")

        # Labels and entries for registration
        tk.Label(register_window, text="Enter a Username:", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(register_window, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Label(register_window, text="Enter a numeric Password:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(register_window, font=("Arial", 12), show='*')
        self.password_entry.pack(pady=5)

        # Submit button for registration
        register_button = tk.Button(register_window, text="Register", command=self.register_user, font=("Arial", 12, "bold"), bg="navy", fg="white")
        register_button.pack(pady=10)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username.isalnum():
            messagebox.showerror("Error", "Username must be alphanumeric.")
            return
        
        try:
            password = int(password)
        except ValueError:
            messagebox.showerror("Error", "Password must be numeric.")
            return
        
        SQL_cmd = "INSERT INTO user_table(Username, Password) VALUES(%s, %s)"
        val = (username, password)
        try:
            self.mycursor.execute(SQL_cmd, val)
            self.conn.commit()
            messagebox.showinfo("Success", f"User registered successfully. Welcome, {username}!")
        except sql.Error as err:
            messagebox.showerror("Error", f"Could not register user: {err}")

    def handle_login(self):
        # Create a new window for login
        login_window = tk.Toplevel(self)
        login_window.title("Login")
        login_window.geometry("400x300")

        # Labels and entries for login
        tk.Label(login_window, text="Enter Username:", font=("Arial", 12)).pack(pady=5)
        self.login_username_entry = tk.Entry(login_window, font=("Arial", 12))
        self.login_username_entry.pack(pady=5)

        tk.Label(login_window, text="Enter Password:", font=("Arial", 12)).pack(pady=5)
        self.login_password_entry = tk.Entry(login_window, font=("Arial", 12), show='*')
        self.login_password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(login_window, text="Login", command=self.login_user, font=("Arial", 12, "bold"), bg="navy", fg="white")
        login_button.pack(pady=10)

    def login_user(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        if not username.isalnum():
            messagebox.showerror("Error", "Username must be alphanumeric.")
            return
        
        try:
            password = int(password)
        except ValueError:
            messagebox.showerror("Error", "Password must be numeric.")
            return

        SQL_cmd = "SELECT * FROM user_table WHERE Username = %s AND Password = %s"
        val = (username, password)
        self.mycursor.execute(SQL_cmd, val)

        if self.mycursor.fetchone() is None:
            messagebox.showerror("Error", "Invalid username or password. Please try again.")
        else:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            # Create a new instance of the menu application
            menu_app = RoyalBankApp1()
            # Close the current login window
            self.destroy()
            # Start the main loop of the menu application
            menu_app.mainloop()

    def handle_change_credentials(self):
        # Create a new window for changing credentials
        change_window = tk.Toplevel(self)
        change_window.title("Change Username/Password")
        change_window.geometry("400x300")

        # Labels and entries for change credentials
        tk.Label(change_window, text="Enter your old Username:", font=("Arial", 12)).pack(pady=5)
        self.old_username_entry = tk.Entry(change_window, font=("Arial", 12))
        self.old_username_entry.pack(pady=5)

        tk.Label(change_window, text="Enter your old Password:", font=("Arial", 12)).pack(pady=5)
        self.old_password_entry = tk.Entry(change_window, font=("Arial", 12), show='*')
        self.old_password_entry.pack(pady=5)

        tk.Label(change_window, text="Choose an option:", font=("Arial", 12)).pack(pady=5)
        self.change_var = tk.IntVar()
        change_option1 = tk.Radiobutton(change_window, text="Change Username", variable=self.change_var, value=1, font=("Arial", 12))
        change_option1.pack(pady=5)
        change_option2 = tk.Radiobutton(change_window, text="Change Password", variable=self.change_var, value=2, font=("Arial", 12))
        change_option2.pack(pady=5)

        change_button = tk.Button(change_window, text="Submit", command=self.change_credentials, font=("Arial", 12, "bold"), bg="navy", fg="white")
        change_button.pack(pady=10)

    def change_credentials(self):
        old_username = self.old_username_entry.get()
        old_password = self.old_password_entry.get()
        choice = self.change_var.get()

        if not old_username.isalnum():
            messagebox.showerror("Error", "Username must be alphanumeric.")
            return
        
        try:
            old_password = int(old_password)
        except ValueError:
            messagebox.showerror("Error", "Password must be numeric.")
            return

        # SQL command to find the user in the database
        SQL_cmd = "SELECT * FROM user_table WHERE Username = %s AND Password = %s"
        val = (old_username, old_password)
        self.mycursor.execute(SQL_cmd, val)

        if self.mycursor.fetchone() is None:
            messagebox.showerror("Error", "Invalid old username or password.")
            return

        if choice == 1:  # Change Username
            new_username = simpledialog.askstring("New Username", "Enter your new username:")
            if not new_username.isalnum():
                messagebox.showerror("Error", "Username must be alphanumeric.")
                return
            
            # Update SQL command
            update_cmd = "UPDATE user_table SET Username = %s WHERE Password = %s"
            update_val = (new_username, old_password)

            try:
                self.mycursor.execute(update_cmd, update_val)
                self.conn.commit()
                messagebox.showinfo("Success", f"Username changed successfully from '{old_username}' to '{new_username}'")
            except sql.Error as err:
                messagebox.showerror("Error", f"Could not update username: {err}")

        elif choice == 2:  # Change Password
            new_password = simpledialog.askstring("New Password", "Enter your new password:", show='*')
            try:
                new_password = int(new_password)
            except ValueError:
                messagebox.showerror("Error", "Password must be numeric.")
                return
            
            # Update SQL command
            update_cmd = "UPDATE user_table SET Password = %s WHERE Username = %s"
            update_val = (new_password, old_username)

            try:
                self.mycursor.execute(update_cmd, update_val)
                self.conn.commit()
                messagebox.showinfo("Success", f"Password changed successfully.")
            except sql.Error as err:
                messagebox.showerror("Error", f"Could not update password: {err}")

    def run(self):
        self.mainloop()

# Running the application
if __name__ == "__main__":
    app = RoyalBankApp()
    app.run()
