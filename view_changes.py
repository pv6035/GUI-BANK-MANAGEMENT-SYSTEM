import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector as sql

class YourApp1(tk.Toplevel):
    def __init__(self, master, conn, mycursor):
        super().__init__(master)
        self.conn = conn
        self.mycursor = mycursor
        
        # Set up the top-level window
        self.title("View Changes Made in Your Account")
        self.geometry("500x400")

        # Create labels and entry widgets for account number and account name
        tk.Label(self, text="Account Number:").grid(row=0, column=0, padx=10, pady=10)
        self.acc_no_entry = tk.Entry(self)
        self.acc_no_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Account Name:").grid(row=1, column=0, padx=10, pady=10)
        self.acc_name_entry = tk.Entry(self)
        self.acc_name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create a button to fetch and display changes
        view_button = tk.Button(self, text="View Changes", command=self.fetch_and_display_changes)
        view_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Create a scrolled text widget to display changes
        self.result_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=15)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def fetch_and_display_changes(self):
        acc_no = self.acc_no_entry.get()
        acc_name = self.acc_name_entry.get().upper()

        # Validate account number and name inputs
        if not acc_no.isdigit() or len(acc_no) != 8:
            messagebox.showerror("Error", "Invalid account number format. Please enter an 8-digit account number.")
            return
        if not acc_name.isalpha():
            messagebox.showerror("Error", "Invalid account name format. Please enter only alphabetic characters.")
            return
        
        # Verify account number and name in the database
        SQL_cmd1 = "SELECT * FROM customer_details WHERE Account_Number = %s AND Account_Name = %s"
        values1 = (acc_no, acc_name)
        self.mycursor.execute(SQL_cmd1, values1)
        
        if self.mycursor.fetchone() is None:
            messagebox.showerror("Error", "Invalid account number or name.")
            return
        
        # Fetch changes for the account from the `change_table`
        SQL_cmd2 = "SELECT * FROM change_table WHERE Account_Number = %s"
        values2 = (acc_no,)
        self.mycursor.execute(SQL_cmd2, values2)
        data = self.mycursor.fetchall()

        # Clear previous results from the scrolled text widget
        self.result_text.delete(1.0, tk.END)

        if not data:
            messagebox.showinfo("No Changes", "No changes found for the provided account number.")
            return
        
        # Display changes in the scrolled text widget
        for idx, row in enumerate(data):
            change_info = (
                f"Change {idx + 1}:\n"
                f"Date: {row[2]}\n"
                f"Old Data [City/Phone Number/Email]: {row[3]}\n"
                f"New Data [City/Phone Number/Email]: {row[4]}\n\n"
            )
            self.result_text.insert(tk.END, change_info)

        # Auto-scroll to the beginning of the text
        self.result_text.see(1.0)

# Function to set up the database connection
def setup_database_connection():
    return sql.connect(host="localhost", user="your_username", passwd="your_password", database="your_database")

# Example usage of YourApp1
if __name__ == "__main__":
    root = tk.Tk()
    conn = setup_database_connection()  # Replace with your database connection setup function
    mycursor = conn.cursor()
    app = YourApp1(root, conn, mycursor)
    root.mainloop()
