import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import mysql.connector as sql

from create_account import CreateAccountWindow
from transactions import TransactionsWindow
from update_details import UpdateDetailsWindow
from view_customer_details import ViewAccountDetailsWindow
from view_transactions import YourApp
from view_changes import YourApp1
from delete_account import AccountDeletionApp

class RoyalBankApp1(tk.Tk):
    def __init__(self):
        super().__init__()

        # Connect to the database
        self.conn = sql.connect(host="localhost", user="root", passwd="root@123", database="the_royal_bank")
        self.mycursor = self.conn.cursor()
        self.conn.autocommit = True

        # Configure the main window
        self.title("The Royal Bank")
        self.geometry("500x400")

        # Create frames for better layout organization
        self.menu_frame = tk.Frame(self, bg="#E6F7FF")
        self.menu_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a status bar at the bottom of the main window
        self.status_bar = tk.Label(self, text="Welcome to The Royal Bank", relief=tk.SUNKEN, anchor=tk.W, bg="#C2E7FF")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create menu buttons
        self.create_menu_buttons()
    
    def create_menu_buttons(self):
        # Define operations with labels and functions
        operations = [
            ("Create a New Bank Account", self.create_account, "Create a new bank account"),
            ("Transactions", self.transactions, "Perform transactions"),
            ("Update Details", self.update_details, "Update account details"),
            ("View Customer Details", self.view_customer_details, "View customer details"),
            ("View Transaction History", self.view_transactions, "View transaction history"),
            ("View Changes Made", self.view_changes, "View changes made"),
            ("Delete Account", self.delete_account, "Delete a bank account"),
            ("Quit", self.quit_app, "Quit the application")
        ]

        # Create buttons with themed styling
        for label, function, tooltip in operations:
            button = ttk.Button(self.menu_frame, text=label, command=function)
            button.pack(fill=tk.X, pady=5, padx=5)
            
            # Add tooltip for each button
            self.create_tooltip(button, tooltip)
    
    def create_tooltip(self, widget, text):
        tooltip = tk.Label(self, text=text, bg="#FFD", wraplength=150, justify="left", borderwidth=1, relief=tk.SOLID)
        widget.bind("<Enter>", lambda event: tooltip.place(x=event.x_root - self.winfo_x(), y=event.y_root - self.winfo_y() + 25))
        widget.bind("<Leave>", lambda event: tooltip.place_forget())
        
    def update_status(self, text):
        """Update the status bar with a new message."""
        # Check if the main window and status bar exist before updating
        if self.winfo_exists():
            if hasattr(self, 'status_bar') and self.status_bar.winfo_exists():
                try:
                    self.status_bar.config(text=text)
                except tk.TclError:
                    # Catch any TclError and log it (optional)
                    print("Error: Attempted to update a non-existent status bar.")
                    pass

    
    # Callback functions for each operation
    def create_account(self):
        create_account_window = CreateAccountWindow(self)
        create_account_window.mainloop()
        self.update_status("Created a new bank account.")

    def transactions(self):
        transactions_window = TransactionsWindow(self, self.conn)
        transactions_window.grab_set()  
        self.wait_window(transactions_window)
        self.update_status("Performed transactions.")


    def update_details(self):
        update_window = UpdateDetailsWindow(self, self.conn)
        self.wait_window(update_window)
        self.update_status("Opened update details window.")

    def view_customer_details(self):
        view_account_details = ViewAccountDetailsWindow(self, self.conn)
        self.wait_window(view_account_details)
        self.update_status("Viewed customer details.")

    def view_transactions(self):
        view_transactions_window = YourApp(self, self.conn, self.mycursor)
        view_transactions_window.mainloop()
        self.update_status("Viewed transaction history.")

    def view_changes(self):
        view_change = YourApp1(self, self.conn, self.mycursor)

        if isinstance(view_change, tk.Toplevel):
            view_change.wait_window()  # Wait for the view_change window to be closed
            self.update_status("Viewed changes made.")
        else:
            print("Error initializing YourApp1.")
    
    def delete_account(self):
        delete_account = AccountDeletionApp(self, self.conn, self.mycursor)
        delete_account.deletion_window.wait_window()
        self.update_status("Deleted a bank account.")


    def quit_app(self):
        print("Quitting application")
        self.quit()

    def update_status(self, text):
        """Update the status bar with a new message."""
        try:
            self.status_bar.config(text=text)
        except AttributeError:
            print("Error: The status bar is not initialized or not a valid widget.")


# Running the application
if __name__ == "__main__":
    app = RoyalBankApp1()
    app.mainloop()
