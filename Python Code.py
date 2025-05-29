import tkinter as tk
from tkinter import messagebox, Toplevel
import mysql.connector
import datetime

# Database Configuration
DB_CONFIG = {
    'host': "localhost",
    'user': "root",
    'password': "12344321",
    'database': "db"
}

class BloodBankDB:
    def __init__(self):
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

    def get_all_blood_data(self):
        self.cursor.execute("SELECT * FROM BloodBank")
        return self.cursor.fetchall()

    def get_units(self, blood_group):
        self.cursor.execute("SELECT units FROM BloodBank WHERE Blood_Grp = %s", (blood_group,))
        result = self.cursor.fetchone()
        return int(result[0]) if result else 0

    def update_units(self, blood_group, new_units):
        self.cursor.execute("UPDATE BloodBank SET units = %s WHERE Blood_Grp = %s", (new_units, blood_group))
        self.connection.commit()

    def validate_admin(self, username, password):
        self.cursor.execute("SELECT * FROM Admins WHERE username = %s AND password = %s", (username, password))
        return self.cursor.fetchone() is not None

    def get_transactions(self):
        self.cursor.execute("SELECT name, blood_grp, units, action, date, gender, contact_number FROM Transactions")
        return self.cursor.fetchall()

    def add_transaction(self, name, blood_grp, units, action, gender, contact_number):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""
            INSERT INTO Transactions (name, blood_grp, units, action, date, gender, contact_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, blood_grp, units, action, date, gender, contact_number))
        self.connection.commit()

    def clear_transactions(self):
        self.cursor.execute("TRUNCATE TABLE Transactions")
        self.connection.commit()


class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Admin Login")
        self.on_login_success = on_login_success
        self.db = BloodBankDB()
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Admin Login", font=('arial', 18, 'bold')).grid(row=0, columnspan=2, pady=10)

        tk.Label(self.root, text="Username:", font=('arial', 12)).grid(row=1, column=0, sticky='e')
        self.username_entry = tk.Entry(self.root, font=('arial', 12))
        self.username_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Password:", font=('arial', 12)).grid(row=2, column=0, sticky='e')
        self.password_entry = tk.Entry(self.root, font=('arial', 12), show='*')
        self.password_entry.grid(row=2, column=1)

        login_btn = tk.Button(self.root, text="Login", command=self.login, bg="DodgerBlue2", fg="white", font=('arial', 12))
        login_btn.grid(row=3, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.db.validate_admin(username, password):
            self.root.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


class BloodBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VasClear Innovators Blood Bank Management System")
        self.db = BloodBankDB()
        self.display_main()

    def display_main(self):
        tk.Label(self.root, text="Welcome to VasClear!", font=('arial', 20, 'bold')).grid(row=0, columnspan=4, pady=10)

        data = self.db.get_all_blood_data()
        tk.Label(self.root, text="Blood Group", font=('arial', 12, 'bold')).grid(row=1, column=0)
        tk.Label(self.root, text="Units", font=('arial', 12, 'bold')).grid(row=1, column=1)

        for idx, (blood_group, units) in enumerate(data, start=2):
            tk.Label(self.root, text=blood_group, font=('arial', 10)).grid(row=idx, column=0)
            tk.Label(self.root, text=str(units), font=('arial', 10)).grid(row=idx, column=1)
            tk.Button(self.root, text="Donate", command=lambda bg=blood_group: self.open_window(bg, "donate"), bg="green", fg="white").grid(row=idx, column=2)
            tk.Button(self.root, text="Request", command=lambda bg=blood_group: self.open_window(bg, "request"), bg="red", fg="white").grid(row=idx, column=3)

        tk.Button(self.root, text="View Transactions", command=self.view_transactions, bg="blue", fg="white").grid(row=len(data) + 2, columnspan=4, pady=20)

    def open_window(self, blood_group, action):
        win = Toplevel(self.root)
        win.title(f"{action.title()} Blood - {blood_group}")

        tk.Label(win, text=f"{action.title()} Blood", font=('arial', 18, 'bold')).grid(row=0, columnspan=2, pady=10)

        tk.Label(win, text="Name:").grid(row=1, column=0)
        name_entry = tk.Entry(win)
        name_entry.grid(row=1, column=1)

        tk.Label(win, text="Gender:").grid(row=2, column=0)
        gender_entry = tk.Entry(win)
        gender_entry.grid(row=2, column=1)

        tk.Label(win, text="Contact Number:").grid(row=3, column=0)
        contact_entry = tk.Entry(win)
        contact_entry.grid(row=3, column=1)

        tk.Label(win, text="Units:").grid(row=4, column=0)
        units_entry = tk.Entry(win)
        units_entry.grid(row=4, column=1)

        def submit():
            name = name_entry.get()
            gender = gender_entry.get()
            contact = contact_entry.get()
            try:
                units = int(units_entry.get())
                current_units = self.db.get_units(blood_group)

                if action == "donate":
                    self.db.update_units(blood_group, current_units + units)
                elif units <= current_units:
                    self.db.update_units(blood_group, current_units - units)
                else:
                    messagebox.showerror("Error", "Not enough units available")
                    return

                self.db.add_transaction(name, blood_group, units, action, gender, contact)
                messagebox.showinfo("Success", f"Blood {action.title()}ed Successfully")
                win.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for units.")

        tk.Button(win, text="Submit", command=submit, bg="blue", fg="white").grid(row=5, columnspan=2, pady=10)

    def view_transactions(self):
        win = Toplevel(self.root)
        win.title("Transaction Records")

        headers = ["Name", "Blood Group", "Units", "Action", "Date", "Gender", "Contact Number"]
        for i, header in enumerate(headers):
            tk.Label(win, text=header, font=('arial', 12, 'bold')).grid(row=0, column=i)

        for row_idx, transaction in enumerate(self.db.get_transactions(), start=1):
            for col_idx, item in enumerate(transaction):
                tk.Label(win, text=str(item), font=('arial', 10)).grid(row=row_idx, column=col_idx)


if __name__ == "__main__":
    def launch_app():
        root = tk.Tk()
        app = BloodBankApp(root)
        root.mainloop()

    login_root = tk.Tk()
    login_app = LoginWindow(login_root, on_login_success=launch_app)
    login_root.mainloop()
