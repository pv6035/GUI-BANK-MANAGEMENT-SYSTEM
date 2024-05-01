import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector as sql
from datetime import datetime

class CreateAccountWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Create a New Bank Account")
        self.geometry("400x450")
        
        # Create widgets for each input field
        tk.Label(self, text="Enter your desired 8-digit account number:").grid(row=0, column=0, sticky=tk.W)
        self.acc_no_entry = tk.Entry(self)
        self.acc_no_entry.grid(row=0, column=1)

        tk.Label(self, text="Enter your first name:").grid(row=1, column=0, sticky=tk.W)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self, text="Enter your city:").grid(row=2, column=0, sticky=tk.W)
        self.city_entry = tk.Entry(self)
        self.city_entry.grid(row=2, column=1)

        tk.Label(self, text="Enter your 10-digit phone number:").grid(row=3, column=0, sticky=tk.W)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=3, column=1)

        tk.Label(self, text="Enter your date of birth (YYYY-MM-DD):").grid(row=4, column=0, sticky=tk.W)
        self.dob_entry = tk.Entry(self)
        self.dob_entry.grid(row=4, column=1)

        tk.Label(self, text="Enter your gender (M/F/O):").grid(row=5, column=0, sticky=tk.W)
        self.gender_entry = tk.Entry(self)
        self.gender_entry.grid(row=5, column=1)

        tk.Label(self, text="Enter your email address:").grid(row=6, column=0, sticky=tk.W)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=6, column=1)

        tk.Label(self, text="Enter your account type (C/S):").grid(row=7, column=0, sticky=tk.W)
        self.acc_type_entry = tk.Entry(self)
        self.acc_type_entry.grid(row=7, column=1)

        tk.Label(self, text="Enter opening balance:").grid(row=8, column=0, sticky=tk.W)
        self.balance_entry = tk.Entry(self)
        self.balance_entry.grid(row=8, column=1)

        # Add a button to create an account
        tk.Button(self, text="Create Account", command=self.create_account).grid(row=9, column=0, columnspan=2, pady=10)
        
        # Connect to the database
        self.conn = sql.connect(host="localhost", user="root", passwd="root@123", database="the_royal_bank")
        self.mycursor = self.conn.cursor()
        self.conn.autocommit = True

    def create_account(self):
        # Get the input data
        acc_no = self.acc_no_entry.get()
        name = self.name_entry.get().upper()
        city = self.city_entry.get().upper()
        phone_no = self.phone_entry.get()
        dob = self.dob_entry.get()
        gender = self.gender_entry.get().upper()
        email = self.email_entry.get().lower()
        acc_type = self.acc_type_entry.get().upper()
        balance = self.balance_entry.get()

        # Validate the inputs
        if not acc_no.isdigit() or len(acc_no) != 8:
            messagebox.showerror("Invalid Account Number", "Account number must be exactly 8 digits.")
            return
        if not name.isalpha():
            messagebox.showerror("Invalid Name", "Name must contain only letters.")
            return
        if not city.isalpha():
            messagebox.showerror("Invalid City", "City must contain only letters.")
            return
        if not phone_no.isdigit() or len(phone_no) != 10:
            messagebox.showerror("Invalid Phone Number", "Phone number must be exactly 10 digits.")
            return
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Date of Birth must be in YYYY-MM-DD format.")
            return
        if gender not in ["M", "F", "O"]:
            messagebox.showerror("Invalid Gender", "Gender must be M (Male), F (Female), or O (Other).")
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return
        if acc_type not in ["C", "S"]:
            messagebox.showerror("Invalid Account Type", "Account type must be C (Current) or S (Savings).")
            return
        try:
            balance = float(balance)
        except ValueError:
            messagebox.showerror("Invalid Balance", "Balance must be a numeric value.")
            return

        # Check balance requirements based on account type
        if (acc_type == "C" and balance < 10000) or (acc_type == "S" and balance < 500):
            messagebox.showerror("Invalid Balance", f"Minimum balance for {acc_type} account type is {10000 if acc_type == 'C' else 500}.")
            return

        # SQL command to insert data into the 'customer_details' table
        SQL_cmd = ("INSERT INTO customer_details "
                   "(Account_Number, Account_Name, City, Phone_no, DOB, Gender, Email, Account_Type, Initial_Amount)"
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        val = (acc_no, name, city, phone_no, dob, gender, email, acc_type, balance)

        try:
            self.mycursor.execute(SQL_cmd, val)
            self.conn.commit()
            messagebox.showinfo("Success", "Account Created Successfully!")
            self.destroy()  # Close the CreateAccountWindow
        except sql.Error as err:
            messagebox.showerror("Error", f"Could not create account: {err}")

# To use this window, you would create an instance of it from the main application when the user wants to create a new account. Here's an example:
if __name__ == "__main__":
    app = tk.Tk()  # Create a main application window
    create_account_window = CreateAccountWindow(app)
    app.mainloop()  # Start the application loop
