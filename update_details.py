import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime as dt
import mysql.connector as sql

class UpdateDetailsWindow(tk.Toplevel):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.title("Update Account Details")
        self.geometry("400x350")
        
        # Set the database connection and cursor
        self.conn = conn
        self.mycursor = self.conn.cursor()
        
        # Create labels and entry widgets for account information
        tk.Label(self, text="Account Number:").grid(row=0, column=0, padx=10, pady=10)
        self.account_number_entry = tk.Entry(self)
        self.account_number_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Account Holder Name:").grid(row=1, column=0, padx=10, pady=10)
        self.account_holder_entry = tk.Entry(self)
        self.account_holder_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Create buttons to choose update options
        tk.Label(self, text="Select Update Option:").grid(row=2, columnspan=2, pady=10)
        tk.Button(self, text="Update City", command=self.update_city).grid(row=3, columnspan=2, pady=5)
        tk.Button(self, text="Update Phone Number", command=self.update_phone_number).grid(row=4, columnspan=2, pady=5)
        tk.Button(self, text="Update Email", command=self.update_email).grid(row=5, columnspan=2, pady=5)
        
    def update_city(self):
        account_number = self.account_number_entry.get()
        account_holder_name = self.account_holder_entry.get().upper()
        
        # Validate the account number and account holder name
        if not self.validate_input(account_number, account_holder_name):
            return
        
        # Get new city from the user
        new_city = tk.simpledialog.askstring("Update City", "Enter your new city:")
        
        if new_city and new_city.isalpha():
            new_city = new_city.upper()
            
            try:
                # Record the change in the change table
                old_city = self.get_old_value(account_number, account_holder_name, 'City')
                dat = dt.datetime.today()
                self.mycursor.execute("INSERT INTO change_table (Account_Number, Date, Old, New) VALUES (%s, %s, %s, %s)",
                                      (account_number, dat, old_city, new_city))

                # Update the city in the database
                self.mycursor.execute("UPDATE customer_details SET City = %s WHERE Account_Number = %s", (new_city, account_number))

                self.conn.commit()
                
                messagebox.showinfo("Success", "City updated successfully.")
            except sql.Error as err:
                self.conn.rollback()
                messagebox.showerror("Error", f"Failed to update city: {err}")
        else:
            messagebox.showerror("Error", "Invalid city format. Please use alphabets only.")
    
    def update_phone_number(self):
        account_number = self.account_number_entry.get()
        account_holder_name = self.account_holder_entry.get().upper()
        
        # Validate the account number and account holder name
        if not self.validate_input(account_number, account_holder_name):
            return
        
        # Get new phone number from the user
        new_pno = tk.simpledialog.askstring("Update Phone Number", "Enter your new phone number:")
        
        if new_pno and new_pno.isdigit() and len(new_pno) == 10:
            try:
                # Record the change in the change table
                old_pno = self.get_old_value(account_number, account_holder_name, 'Phone_no')
                dat = dt.datetime.today()
                self.mycursor.execute("INSERT INTO change_table (Account_Number, Date, Old, New) VALUES (%s, %s, %s, %s)",
                                      (account_number, dat, old_pno, new_pno))

                # Update the phone number in the database
                self.mycursor.execute("UPDATE customer_details SET Phone_no = %s WHERE Account_Number = %s", (new_pno, account_number))
                
                self.conn.commit()
                
                messagebox.showinfo("Success", "Phone number updated successfully.")
            except sql.Error as err:
                self.conn.rollback()
                messagebox.showerror("Error", f"Failed to update phone number: {err}")
        else:
            messagebox.showerror("Error", "Invalid phone number format. It should be 10 digits.")
    
    def update_email(self):
        account_number = self.account_number_entry.get()
        account_holder_name = self.account_holder_entry.get().upper()
        
        # Validate the account number and account holder name
        if not self.validate_input(account_number, account_holder_name):
            return
        
        # Get new email address from the user
        new_email = tk.simpledialog.askstring("Update Email", "Enter your new email address:")
        
        if new_email and "@" in new_email and "." in new_email:
            try:        
                # Record the change in the change table
                old_email = self.get_old_value(account_number, account_holder_name, 'Email')
                dat = dt.datetime.today()
                self.mycursor.execute("INSERT INTO change_table (Account_Number, Date, Old, New) VALUES (%s, %s, %s, %s)",
                                      (account_number, dat, old_email, new_email))

                # Update the email address in the database
                self.mycursor.execute("UPDATE customer_details SET Email = %s WHERE Account_Number = %s", (new_email, account_number))
                
                self.conn.commit()
                
                messagebox.showinfo("Success", "Email address updated successfully.")
            except sql.Error as err:
                self.conn.rollback()
                messagebox.showerror("Error", f"Failed to update email: {err}")
        else:
            messagebox.showerror("Error", "Invalid email format. Please use a valid email address.")
    
    def validate_input(self, account_number, account_holder_name):
        """Validate account number and account holder name."""
        # Check account number format
        if not (account_number.isdigit() and len(account_number) == 8):
            messagebox.showerror("Error", "Invalid account number format. It should be 8 digits.")
            return False
        
        # Check account holder name format
        if not account_holder_name.isalpha():
            messagebox.showerror("Error", "Invalid account holder name. Please use alphabets only.")
            return False
        
        # Validate the account information in the database
        self.mycursor.execute("SELECT * FROM customer_details WHERE Account_Number = %s AND Account_Name = %s",
                              (account_number, account_holder_name))
        if self.mycursor.fetchone() is None:
            messagebox.showerror("Error", "Invalid account number or name.")
            return False
        
        return True
    
    def get_old_value(self, account_number, account_holder_name, column):
        """Retrieve the old value for a given column from the customer_details table."""
        self.mycursor.execute(f"SELECT {column} FROM customer_details WHERE Account_Number = %s AND Account_Name = %s",
                              (account_number, account_holder_name))
        result = self.mycursor.fetchone()
        
        if result:
            return result[0]
        else:
            return None
