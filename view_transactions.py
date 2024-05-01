import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class YourApp(tk.Toplevel):
    def __init__(self, parent, conn, mycursor):
        super().__init__(parent)
        self.conn = conn
        self.mycursor = mycursor
        self.title("View Transactions")
        self.setup_gui()
        
    def setup_gui(self):
        # Create labels and entry widgets for account number and account name
        tk.Label(self, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)
        self.acc_no_entry = tk.Entry(self)
        self.acc_no_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self, text="Account Name:").grid(row=1, column=0, padx=10, pady=5)
        self.acc_name_entry = tk.Entry(self)
        self.acc_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Add a button to trigger the fetch_and_display_transactions function
        view_button = tk.Button(self, text="View Transactions", command=self.fetch_and_display_transactions)
        view_button.grid(row=2, column=0, columnspan=2, pady=10)
        
    def fetch_and_display_transactions(self):
        # Get account number and account name from entries
        acc_no = self.acc_no_entry.get().strip()
        acc_name = self.acc_name_entry.get().strip().upper()

        # Validate account number and name inputs
        if not acc_no.isdigit() or len(acc_no) != 8:
            messagebox.showerror("Error", "Invalid account number format. Please enter an 8-digit account number.")
            return
        if not acc_name.isalpha():
            messagebox.showerror("Error", "Invalid account name format. Please enter only alphabetic characters.")
            return
        
        # Fetch customer details
        SQL_cmd1 = "SELECT * FROM customer_details WHERE Account_Number = %s AND Account_Name = %s"
        values1 = (acc_no, acc_name)
        self.mycursor.execute(SQL_cmd1, values1)
        
        customer_data = self.mycursor.fetchone()
        if customer_data is None:
            messagebox.showerror("Error", "Invalid account number or name.")
            return
        
        # Fetch transactions for the account
        SQL_cmd2 = "SELECT date, withdrawal_amount, amount_deposited FROM transactions WHERE Account_Number = %s"
        values2 = (acc_no,)
        self.mycursor.execute(SQL_cmd2, values2)
        data = self.mycursor.fetchall()
        
        if not data:
            messagebox.showinfo("No Transactions", "No transactions found for the provided account number.")
            return
        
        # Display transactions in a new top-level window
        transactions_window = tk.Toplevel(self)
        transactions_window.title("Transaction Details")
        
        # Create a treeview widget to display transactions
        tree = ttk.Treeview(transactions_window, columns=("date", "withdrawn", "deposited"), show="headings")
        tree.heading("date", text="Date")
        tree.heading("withdrawn", text="Amount Withdrawn")
        tree.heading("deposited", text="Amount Deposited")

        # Populate the treeview with transaction data
        for idx, row in enumerate(data):
            tree.insert("", "end", values=row)
        
        tree.pack(expand=True, fill=tk.BOTH)
        
        # Add a scrollbar to the treeview if there are many transactions
        scrollbar = ttk.Scrollbar(transactions_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.config(yscrollcommand=scrollbar.set)
        
# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main root window if you don't need it
    
    conn = setup_database_connection()  # Replace with your database connection setup function
    mycursor = conn.cursor()
    
    app = YourApp(root, conn, mycursor)
    app.mainloop()
