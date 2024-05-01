import tkinter as tk
from tkinter import messagebox

class AccountDeletionApp:
    def __init__(self, master, conn, mycursor):
        self.master = master
        self.conn = conn
        self.mycursor = mycursor

    # Create a top-level window for account deletion
        self.deletion_window = tk.Toplevel(master)  # Assign Toplevel window object to self.deletion_window
        self.deletion_window.title("Account Deletion")
        
        # Create labels and entry widgets for account number and account name
        tk.Label(self.deletion_window, text="Account Number:").grid(row=0, column=0)
        self.acc_no_entry = tk.Entry(self.deletion_window)
        self.acc_no_entry.grid(row=0, column=1)

        tk.Label(self.deletion_window, text="Account Name:").grid(row=1, column=0)
        self.acc_name_entry = tk.Entry(self.deletion_window)
        self.acc_name_entry.grid(row=1, column=1)

        # Add a button to trigger the deletion process
        self.delete_button = tk.Button(self.deletion_window, text="Delete Account", command=self.delete_account)
        self.delete_button.grid(row=2, column=0, columnspan=2)

    def delete_account(self):
        acc_no = self.acc_no_entry.get()
        acc_name = self.acc_name_entry.get().upper()

        # Validate account number and account name inputs
        if not acc_no.isdigit() or len(acc_no) != 8:
            messagebox.showerror("Error", "Invalid account number format. Please enter an 8-digit account number.")
            return
    
        if not acc_name.isalpha():
            messagebox.showerror("Error", "Invalid account name format. Please enter only alphabetic characters.")
            return
    
        # Check if the account number and name exist in the database
        SQL_cmd1 = "SELECT * FROM customer_details WHERE Account_Number = %s AND Account_Name = %s"
        values1 = (acc_no, acc_name)
        self.mycursor.execute(SQL_cmd1, values1)
    
        if self.mycursor.fetchone() is None:
            messagebox.showerror("Error", "Invalid account number or name.")
            return
    
        # Ask the user for confirmation before deleting the account
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete your account? All your data will be lost permanently.")
        if not confirm:
            messagebox.showinfo("Account Deletion", "Account not deleted.")
            return
    
        # Delete the account from customer_details
        SQL_cmd2 = "DELETE FROM customer_details WHERE Account_Number = %s AND Account_Name = %s"
        values2 = (acc_no, acc_name)
        self.mycursor.execute(SQL_cmd2, values2)

        # Delete transactions and changes for the account
        SQL_cmd3 = "DELETE FROM transactions WHERE Account_Number = %s"
        values3 = (acc_no,)
        self.mycursor.execute(SQL_cmd3, values3)

        SQL_cmd4 = "DELETE FROM change_table WHERE Account_Number = %s"
        values4 = (acc_no,)
        self.mycursor.execute(SQL_cmd4, values4)

        # Commit the changes
        self.conn.commit()
    
        messagebox.showinfo("Account Deletion", "Account deleted successfully.")
        # Close the account deletion window
        self.deletion_window.destroy()


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    conn = setup_database_connection()  # Replace with your database connection setup function
    mycursor = conn.cursor()
    app = AccountDeletionApp(root, conn, mycursor)
    root.mainloop()
