import tkinter as tk
from tkinter import messagebox
import mysql.connector as sql

class ViewAccountDetailsWindow(tk.Toplevel):
    def __init__(self, master, conn):
        super().__init__(master)
        self.conn = conn
        self.mycursor = conn.cursor()

        # Configure the window
        self.title("View Account Details")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Account number label and entry
        self.acc_no_label = tk.Label(self, text="Enter Account Number:")
        self.acc_no_label.grid(row=0, column=0, padx=10, pady=5)
        self.acc_no_entry = tk.Entry(self)
        self.acc_no_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Account name label and entry
        self.acc_name_label = tk.Label(self, text="Enter Account Holder Name:")
        self.acc_name_label.grid(row=1, column=0, padx=10, pady=5)
        self.acc_name_entry = tk.Entry(self)
        self.acc_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # View details button
        self.view_button = tk.Button(self, text="View Details", command=self.view_account_details)
        self.view_button.grid(row=2, columnspan=2, pady=10)
        
        # Text box to display account details
        self.details_textbox = tk.Text(self, height=10, width=50)
        self.details_textbox.grid(row=3, columnspan=2, padx=10, pady=10)

    def view_account_details(self):
        # Clear any existing text
        self.details_textbox.delete(1.0, tk.END)

        # Get the entered account number and name
        acc_no = self.acc_no_entry.get().strip()
        acc_name = self.acc_name_entry.get().strip().upper()

        # Validate the inputs
        if not acc_no.isdigit() or len(acc_no) != 8:
            messagebox.showerror("Input Error", "Invalid account number format. Account number must contain exactly 8 digits.")
            return
        
        if not acc_name.isalpha():
            messagebox.showerror("Input Error", "Invalid account holder name format. Name must contain only alphabetic characters.")
            return

        # Query the database for the account details
        try:
            SQL_cmd1 = "SELECT * FROM customer_details WHERE Account_Number = %s AND Account_Name = %s"
            values1 = (acc_no, acc_name)
            self.mycursor.execute(SQL_cmd1, values1)
            
            result = self.mycursor.fetchall()
            
            if not result:
                messagebox.showerror("Not Found", "Invalid account number or name. Please try again.")
                return
            
            # Display the account details in the text box
            account_details = result[0]
            self.details_textbox.insert(tk.END, f"Account Number: {account_details[0]}\n")
            self.details_textbox.insert(tk.END, f"Account Name: {account_details[1]}\n")
            self.details_textbox.insert(tk.END, f"City: {account_details[2]}\n")
            self.details_textbox.insert(tk.END, f"Phone Number: {account_details[3]}\n")
            self.details_textbox.insert(tk.END, f"Date of Birth: {account_details[4]}\n")
            self.details_textbox.insert(tk.END, f"Gender: {account_details[5]}\n")
            self.details_textbox.insert(tk.END, f"Email: {account_details[6]}\n")
            self.details_textbox.insert(tk.END, f"Account Type: {account_details[7]}\n")
            self.details_textbox.insert(tk.END, f"Balance: ₹{account_details[8]:,.2f}\n")

        except sql.Error as err:
            messagebox.showerror("Database Error", f"An error occurred while fetching account details: {err}")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    conn = sql.connect(host="localhost", user="root", passwd="your_password", database="your_database")
    app = ViewAccountDetailsWindow(root, conn)
    root.mainloop()
