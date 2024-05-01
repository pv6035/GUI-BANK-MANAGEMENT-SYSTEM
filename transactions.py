import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector as sql

class TransactionsWindow(tk.Toplevel):
    def __init__(self, master, conn):
        super().__init__(master)
        self.master = master
        self.conn = conn

        self.title("Perform Transactions")
        self.geometry("400x350")

        self.transaction_type_var = tk.StringVar(self.master, value="Deposit")  # Initialize StringVar

        tk.Label(self, text="Account Number:").grid(row=0, column=0, padx=10, pady=10)
        self.account_number_entry = tk.Entry(self)
        self.account_number_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Account Holder Name:").grid(row=1, column=0, padx=10, pady=10)
        self.account_holder_entry = tk.Entry(self)
        self.account_holder_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Transaction Type:").grid(row=2, column=0, padx=10, pady=10)
        tk.Radiobutton(self, text="Withdraw", variable=self.transaction_type_var, value="Withdraw").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(self, text="Deposit", variable=self.transaction_type_var, value="Deposit").grid(row=2, column=1, sticky="e")

        tk.Label(self, text="Amount:").grid(row=3, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self, text="Perform Transaction", command=self.perform_transaction).grid(row=4, columnspan=2, pady=20)

    def perform_transaction(self):
        account_number = self.account_number_entry.get()
        account_holder_name = self.account_holder_entry.get().upper()
        amount = self.amount_entry.get()

        if not account_number or not account_holder_name or not amount:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        if not account_number.isdigit() or len(account_number) != 8:
            messagebox.showerror("Error", "Invalid account number format. It should be 8 digits.")
            return

        if not account_holder_name.isalpha():
            messagebox.showerror("Error", "Invalid name format. Please use alphabets only.")
            return

        try:
            amount_float = float(amount)
            if amount_float <= 0:
                messagebox.showerror("Error", "Amount must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount format. Please enter a numeric value.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT Initial_Amount FROM customer_details WHERE Account_Number = %s AND Account_Name = %s", (account_number, account_holder_name))
            account_data = cursor.fetchone()

            if account_data is None:
                messagebox.showerror("Error", "Invalid account number or name.")
                return

            current_balance = account_data[0]

            if current_balance <= 0:
                messagebox.showerror("Error", "Unexpected data format in current balance. Please contact support.")
                return

            current_balance_float = float(current_balance)

            if self.transaction_type_var.get() == "Withdraw":
                if amount_float > current_balance_float:
                    messagebox.showerror("Error", "Insufficient funds for withdrawal.")
                    return

                cursor.execute("UPDATE customer_details SET Initial_Amount = Initial_Amount - %s WHERE Account_Number = %s", (amount_float, account_number))
                cursor.execute("INSERT INTO transactions(Account_Number, Date, Withdrawal_Amount, Amount_Deposited) VALUES(%s, %s, %s, %s)", (account_number, datetime.now(), amount_float, 0))

            elif self.transaction_type_var.get() == "Deposit":
                cursor.execute("UPDATE customer_details SET Initial_Amount = Initial_Amount + %s WHERE Account_Number = %s", (amount_float, account_number))
                cursor.execute("INSERT INTO transactions(Account_Number, Date, Withdrawal_Amount, Amount_Deposited) VALUES(%s, %s, %s, %s)", (account_number, datetime.now(), 0, amount_float))

            self.conn.commit()
            messagebox.showinfo("Success", "Transaction successful.")

        except sql.Error as err:
            self.conn.rollback()
            messagebox.showerror("Error", f"Failed to perform transaction: {err}")
