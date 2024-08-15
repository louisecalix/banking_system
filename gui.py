import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from accounts import SavingsAccount, CheckingAccount, JointAccount
from users import User, UserManagement
from widgets import WidgetsFactory
from controller import LogicController, BankFacade
import json


# -------------------------login account-----------------------------
class LoginWindow(tk.Tk):
    def __init__(self, logic_controller=LogicController()):
        super().__init__()
        self.logic_controller = logic_controller
        self.config_window()
        self.create_widgets()
        self.display()

    def config_window(self):
        self.title('Login')
        self.geometry('600x600')
        self.resizable(False, False)
        self.configure(bg='#3a4c4d')

    def create_widgets(self):
        factory = WidgetsFactory()

        self.login_label = factory.create_label(self, 'Login', ('Courier', 40))
        self.login_label.pack(pady=60)

        self.username_label = factory.create_label(self, 'Username', ("Courier", 10))
        self.username_label.pack()

        self.username_entry = factory.create_entry(self, width=25)
        self.username_entry.pack()

        self.password_label = factory.create_label(self, 'Password', ("Courier", 10))
        self.password_label.pack()

        self.password_entry = factory.create_entry(self, '*', width=25)
        self.password_entry.pack()

        self.login_button = factory.create_button(self, 'Log in', width=10, height=2, command=self.handle_login)
        self.login_button.pack(pady=10)

        self.register_button = factory.create_button(self, 'Create a new account', width=20, height=2, command=self.open_register_window)
        self.register_button.pack(pady=70)


    def handle_login(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if not all([entered_username, entered_password]):
            messagebox.showerror('Error', 'All fields must be filled')
            return
        
        BankFacade.login(self.logic_controller, entered_username, entered_password)
        if UserManagement.active_account is not None:
            self.open_dashboard()


    def open_register_window(self):
        register_window = RegisterWindow(self)
        self.withdraw()

    def open_dashboard(self):
        dashboard_window = BankDashboard(self)
        self.withdraw()

    def display(self):
        self.mainloop()

class RegisterWindow(tk.Toplevel): # --------------------------------register--------------------------------
    def __init__(self, parent):
        super().__init__(parent)
        self.logic_controller = LogicController()
        self.config_window()
        self.create_widgets()
        
    def config_window(self):
        self.title('Login')
        self.geometry('600x600')
        self.resizable(False, False)
        self.configure(bg='#3a4c4d')

    def create_widgets(self):
        factory = WidgetsFactory()
        self.create_label = factory.create_label(self, 'CREATE NEW ACCOUNT', ('Courier', 20))
        self.create_label.pack(pady=20)

        self.name_label = factory.create_label(self, "Name: ", ("Courier", 10))
        self.name_label.pack()

        self.name_entry = factory.create_entry(self)
        self.name_entry.pack()

        self.username_label = factory.create_label(self, "Username: ", ("Courier", 10))
        self.username_label.pack()

        self.username_entry = factory.create_entry(self)
        self.username_entry.pack()

        self.password_label = factory.create_label(self, "Password: ", ("Courier", 10))
        self.password_label.pack()

        self.password_entry = factory.create_entry(self, '*')
        self.password_entry.pack()

        self.confirm_password_label = factory.create_label(self, "Confirm Password: ", ("Courier",10))
        self.confirm_password_label.pack()

        self.confirm_password_entry = factory.create_entry(self, '*')
        self.confirm_password_entry.pack()

        self.age_label = factory.create_label(self, "Age: ", ("Courier", 10))
        self.age_label.pack()

        self.age_entry = factory.create_entry(self)
        self.age_entry.pack()

        gender_type = ['Female', 'Male']
        self.gender_label = factory.create_label(self, 'Gender', ('Courier', 10))
        self.gender_label.pack()
        self.gender_combobox = factory.create_combobox(self, values=gender_type)
        self.gender_combobox.pack()
        self.gender_combobox.set(gender_type[0])

        self.address_label = factory.create_label(self, "Address: ", ("Courier", 10))
        self.address_label.pack()

        self.address_entry = factory.create_entry(self)
        self.address_entry.pack()

        self.phone_label = factory.create_label(self, "Phone Number: ", ("Courier", 10))
        self.phone_label.pack()

        self.phone_entry = factory.create_entry(self)
        self.phone_entry.pack()

        self.create_button = factory.create_button(self, "Create account", width=20, height=2, command=self.create_account)
        self.create_button.pack(pady=20)

        self.back_button = factory.create_button(self, 'Return', width=20, command=self.main_callback)
        self.back_button.pack(pady=20)

    def create_account(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        age = self.age_entry.get()
        gender = self.gender_combobox.get()
        address = self.address_entry.get()
        phone_number = self.phone_entry.get()


        if not all([name, username, password, confirm_password, age, gender, address, phone_number]):
            messagebox.showerror('Error', 'All fields must be filled')
            return
        
        for account in UserManagement._customer:
            if account.get_username() == username:
                messagebox.showerror('Username error', 'This username is already taken')
                return
        
        if len(password) < 8:
            messagebox.showerror('Password Error', 'Your password should have at least 8 characters')
            return

        if password != confirm_password:
            messagebox.showerror('Error', 'Password and Confirm Password must match')
            return
        
        try:
            age_int = int(age)
        except ValueError:
            messagebox.showerror('Age Error', 'Please enter a valid age number')
            return
        
        try:
            phone_number_int = int(phone_number)
        except ValueError:
            messagebox.showerror('Phone number Error', 'Please enter a valid phone number')
            return
    
        BankFacade.register(self.logic_controller, name, username, password, age, gender, address, phone_number)
        self.destroy()
        LoginWindow()

    def main_callback(self):
        self.destroy()
        LoginWindow()


class BankDashboard(tk.Toplevel): # ---------------------dashboard window---------------------------
    def __init__(self, parent):
        super().__init__(parent)
        self.config_window()
        self.create_widgets()
        
    def config_window(self):
        self.title('Dashobard')
        self.geometry('600x600')
        self.resizable(False, False)
        self.configure(bg='#3a4c4d')

    def create_widgets(self):
        factory = WidgetsFactory()

        self.dashboard_label = factory.create_label(self, 'DASHBOARD', ("Courier", 30))
        self.dashboard_label.pack(pady=40)

        if UserManagement.active_account is not None:
            self.welcome_label = factory.create_label(self, f'Welcome, {UserManagement.active_account.get_name()}!', ("Courier", 10))
            self.welcome_label.pack()

        self.user_id_label = factory.create_label(self, f'USER ID: {UserManagement.active_account.get_user_id()}', ("Courier", 10))
        self.user_id_label.pack()


        self.view_account_button = factory.create_button(self, 'View accounts', width=30, height=2, command=self.show_accounts)
        self.view_account_button.pack(pady=20)

        self.add_account_button = factory.create_button(self, 'Open new account', width=30, height=2, command=self.open_account)
        self.add_account_button.pack(pady=20)

        self.logout_button = factory.create_button(self, 'Logout', width=30, height=3, command=self.loguot)
        self.logout_button.pack(pady=20)

    def show_accounts(self):
        accounts = UserManagement.active_account.get_accounts()

        if not accounts:
            messagebox.showerror('No account', 'No accounts found')
        else:
            self.view_account()

            
    def view_account(self):
        self.withdraw()
        AccountViewer(self, self.update_dashboard)


    def loguot(self):
        self.destroy()
        BankFacade.logout()

    def open_account(self):
        self.withdraw()  
        OpenAccount(self, self.update_dashboard)

    def update_dashboard(self):
        self.deiconify()  
        print("Updating BankDashboard")


class OpenAccount(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.config_window()
        self.create_widgets()

    def config_window(self):
        self.title('Open new account')
        self.geometry('600x600')
        self.resizable(False, False)
        self.configure(bg='#3a4c4d')

    def create_widgets(self):
        factory = WidgetsFactory()

        self.account_type_label = factory.create_label(self, 'Account Type', ('Courier', 20))
        self.account_type_label.pack(pady=20)

        account_types = ['Savings Account', 'Checking Account', 'Joint Account']

        self.account_type_combobox = factory.create_combobox(self, values=account_types)
        self.account_type_combobox.set(account_types[0])
        self.account_type_combobox.pack(pady=10)

        self.deposit_label = factory.create_label(self, 'Initial Deposit', ('Courier', 15))
        self.deposit_label.pack()

        self.deposit_entry = factory.create_entry(self)
        self.deposit_entry.pack(pady=10)

        self.account_type_combobox.bind('<<ComboboxSelected>>', self.update_widgets)

        self.coholder_label = factory.create_label(self, 'Co-Holder', ('Courier', 15))
        self.coholder_entry = factory.create_entry(self)

        self.create_account_button = factory.create_button(self, 'Create Account', self.create_account)
        self.create_account_button.pack(pady=20)

    def update_widgets(self, event):
        selected_account_type = self.account_type_combobox.get()

        if selected_account_type == 'Joint Account':
            self.coholder_label.pack()
            self.coholder_entry.pack()
        else:
            self.coholder_label.pack_forget()
            self.coholder_entry.pack_forget()

    def coholder_exists(self, coholder_username):
        try:
            with open("info.json", "r") as file:
                info = json.load(file)
                for user_data in info['user']:
                    if user_data['username'] == coholder_username:
                        return True
        except FileNotFoundError:
            pass

        return False


    def create_account(self):
        account_type = self.account_type_combobox.get()
        initial_deposit = self.deposit_entry.get()
        coholder_username = self.coholder_entry.get()

        if account_type == 'Joint Account' and not self.coholder_exists(coholder_username):
            messagebox.showerror("Error", f"The co-holder with username '{coholder_username}' does not exist.")
            return

        if not initial_deposit.isdigit() or int(initial_deposit) <= 0:
            messagebox.showerror("Deposit Error", "Invalid initial deposit. Please enter a positive numeric value.")
            return

        try:
            initial_deposit = int(initial_deposit)

            min_initial_deposit = {
                'Savings Account': 500,
                'Checking Account': 25000,
                'Joint Account': 50000
            }

            if initial_deposit < min_initial_deposit.get(account_type, 0):
                messagebox.showerror("Invalid Initial Deposit",
                                    f"Minimum initial deposit for {account_type} is {min_initial_deposit[account_type]}")
                return

            if account_type == 'Savings Account':
                new_account = SavingsAccount(UserManagement.active_account, initial_deposit)
            elif account_type == 'Checking Account':
                new_account = CheckingAccount(UserManagement.active_account, initial_deposit)
            elif account_type == 'Joint Account':
                co_holder = self.coholder_entry.get()
                new_account = JointAccount(UserManagement.active_account, initial_deposit, co_holder)

            else:
                messagebox.showerror("Account Type Error", "Invalid account type.")
                return

            UserManagement.active_account.add_account(new_account)
            UserManagement.save_account_data()

            messagebox.showinfo("Account created", f"Creating {account_type} with initial deposit: {initial_deposit}")
            self.destroy()

            if self.callback:
                self.callback()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid initial deposit as a number.")


# ----------------------------------------------------------------
class AccountViewer(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.config_window()
        self.create_widgets()
        
    def config_window(self):
        self.title('Accounts')
        self.geometry('600x600')
        # self.resizable(False)
        self.configure(bg='#3a4c4d')

    def create_widgets(self):
        factory = WidgetsFactory()

        self.account_label = factory.create_label(self, 'Your Accounts', ('Courier', 20))
        self.account_label.pack(pady=20)
        self.amount_label = factory.create_label(self, 'Enter amount:')
        self.amount_label.pack()
        self.amount_entry = factory.create_entry(self)
        self.amount_entry.pack()

        accounts = UserManagement.active_account.get_accounts()

        for account in accounts:
            frame = factory.create_frame(self, width=400, height=100, bg='#3a4c4d', bd=3, relief=tk.GROOVE)
            frame.pack(pady=20)

            account_type_label = factory.create_label(frame, f'Account Type: {account.get_account_type()}', ('Courier', 12))
            account_type_label.pack()

            balance_label = factory.create_label(frame, f'Balance: {account.get_initial_balance()}', ('Courier', 12))
            balance_label.pack()

            deposit_button = factory.create_button(frame, text='Deposit', width=15, command=lambda acc=account, label=balance_label: self.handle_transaction(acc, 'deposit', label))
            deposit_button.pack(side=tk.LEFT, padx=10)

            withdraw_button = factory.create_button(frame, text='Withdraw', width=15, command=lambda acc=account, label=balance_label: self.handle_transaction(acc, 'withdraw', label))
            withdraw_button.pack(side=tk.LEFT, padx=10)
            

        self.total_balance_button = factory.create_button(self, 'Total Balance', command=self.get_total_bal, width=30, height=2)
        self.total_balance_button.pack(pady=10)

        self.return_button = factory.create_button(self, 'Return', command=self.destroy_callback, width=30, height=2)
        self.return_button.pack(pady=20)


    def handle_transaction(self, account, transaction_type, balance_label):
        amount_input = self.amount_entry.get()

        try:
            amount = float(amount_input)
        except ValueError:
            messagebox.showerror('Invalid Amount', f'Please enter a valid number for the {transaction_type}')
            return

        if transaction_type == 'withdraw' and amount > account.get_initial_balance():
            messagebox.showerror('Insufficient Funds', 'Withdrawal amount exceeds the account balance')
            return

        if transaction_type == 'deposit':
            account.deposit(amount)
        elif transaction_type == 'withdraw':
            account.withdraw(amount)

        balance_label.config(text=f'Balance: {account.get_initial_balance()}')
        messagebox.showinfo('Successful', f'{transaction_type.capitalize()} successfully')


    def handle_deposit(self, account):
        self.handle_transaction(account, 'deposit')

    def handle_withdraw(self, account):
        self.handle_transaction(account, 'withdraw')

    def get_total_bal(self):
        accounts = UserManagement.active_account.get_accounts()
        total_balance = sum(account.get_initial_balance() for account in accounts)
        messagebox.showinfo('Total Balance', f'Total Balance for all accounts: {total_balance}')

    def destroy_callback(self):
        self.destroy()
        self.callback()
