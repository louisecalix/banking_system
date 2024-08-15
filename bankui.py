import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# factory widgets
class WidgetFactory:
    def create_button(self, parent, text, command=None, width=None, height=None, bg='#c7cccc'):
        return tk.Button(parent, text=text, command=command, width=width, height=height, bg=bg)
    
    def create_label(self, parent, text, font=("Courier", 10), bg='#3a4c4d', foreground='white'):
        label = tk.Label(parent, text=text, bg=bg, foreground=foreground)
        label.configure(font=font)
        return label
    
    def create_entry(self, parent, show='', width=40, bg='white'):
        return tk.Entry(parent, show=show, width=width, bg=bg)
    
    def create_text(self, parent):
        return tk.Text(parent)
    
    def create_combobox(self, parent, values=[], state='readonly'):
        return ttk.Combobox(parent, values=values, state=state)
    
    def create_separator(self, parent, orient):
        return ttk.Separator(parent, orient=orient)
    

class Account:
    def __init__(self, name, username, password, account_number, account_type, initial_balance) -> None:
        self.__name = name
        self.__username = username
        self.__password = password
        self.__account_number = account_number
        self.__account_type = account_type
        self.__initial_balance = float(initial_balance)

    def get_name(self):
        return self.__name

    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password
    
    def get_account_number(self):
        return self.__account_number
    
    def get_account_type(self):
        return self.__account_type
    
    def get_initial_balance(self):
        return self.__initial_balance
    
    def set_initial_balance(self, amount):
        self.__initial_balance = amount
        return self.__initial_balance
    

class BankAccount(Account):
    def __init__(self, name, username, password, account_number, account_type, initial_balance) -> None:
        super().__init__(name, username, password, account_number, account_type, initial_balance)

    def _credit(self, amount):
        current_balance = super().get_initial_balance()
        new_balance_amount = current_balance + amount
        super().set_initial_balance(new_balance_amount)
    
    def deposit(self, amount):
        if amount <= 0:
            return 'Amount must be greater than 0'
        self._credit(amount)
        print(f'New Balance: {self.get_initial_balance()}')


    def _debit(self, amount):
        current_balance = super().get_initial_balance()
        new_balance_amount = current_balance - amount
        super().set_initial_balance(new_balance_amount)


    def withdraw(self, amount):
        if amount <= 0:
            return 'Amount must be greater than 0'
        self._debit(amount)
        print(f'New Balance: {self.get_initial_balance()}')


# -----------------------logic controller---------------------
class LogicController:
    @staticmethod
    def handle_login_control(username, password):
        for account in UserManagement._savingsaccount + UserManagement._checkingaccount + UserManagement._jointaccount:
            if account.get_username() == username and account.get_password() == password:
                print('Logged in succcessfully!')
                UserManagement.active_account = account
                break

        else:
            print('Login Failed')
            messagebox.showerror('Login Error', 'Credentials Invalid')


    @staticmethod
    def handle_logout_control():
        UserManagement.active_account = None
        print('User logged out successfully')
        LogicController.mainwindow_callback()


    @staticmethod
    def handle_account_creation_control(name, username, password, account_type, initial_deposit):
        account_id = len(UserManagement._savingsaccount + UserManagement._checkingaccount + UserManagement._jointaccount)
        print("Account Creation - Name:", name, "Username:", username, "Password:", password, "Type:", account_type, "Initial Deposit:", initial_deposit)
        new_account = BankAccount(name, username, password, account_id, account_type, initial_deposit)

        if account_type == "Savings":
            UserManagement._savingsaccount.append(new_account)
        elif account_type == "Checking":
            UserManagement._checkingaccount.append(new_account)
        elif account_type == "Joint":
            UserManagement._jointaccount.append(new_account)

        messagebox.showinfo(f"Account Created", f"Account with account ID of [{account_id}] is created")


    def mainwindow_callback():
        MainWindow(LogicController)


#  --------------------------------user management------------------------------
class UserManagement:
    _customer = []
    _savingsaccount = []
    _checkingaccount = []
    _jointaccount = []
    active_account = None


#  ---------------------------------main window------------------------------------------------
class MainWindow(tk.Tk): # Login Window
    def __init__(self, logic_controller):
        super().__init__()
        self.logic_controller = logic_controller
        self.config_window()
        self.create_widgets()
        self.display()

    def config_window(self):
        self.title("Login")
        self.geometry("400x400")
        self.resizable(False, False)
        self.configure(bg='#3a4c4d')
    
    def create_widgets(self):
        factory = WidgetFactory()

        self.login_label = factory.create_label(self, 'Login', ('Courier', 40))
        self.login_label.pack(pady=20)

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

        self.register_button = factory.create_button(self, 'Create a new account', width=20, height=2, command=self.open_creation_window)
        self.register_button.pack(pady=30)


    def handle_login(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if not all([entered_username, entered_password]):
            messagebox.showerror('Error', 'All fields must be filled')
            return
        
        BankFacade.login(self.logic_controller, entered_username, entered_password)

        if UserManagement.active_account:
            account_type = UserManagement.active_account.get_account_type()
            if account_type == 'Savings':
                self.open_savings_window()
            elif account_type == 'Checking':
                self.open_checking_window()
            elif account_type == 'Joint':
                self.open_joint_window()



    def open_creation_window(self):
        createaccountwindow = CreateAccountWindow(self)
        self.withdraw()

    def open_savings_window(self):
        savingswindow = SavingsWindow(self)
        self.withdraw()


    def open_checking_window(self):
        checkingwindow = CheckingWindow(self)    
        self.withdraw()


    def open_joint_window(self):
        jointwindow = JointWindow(self)
        self.withdraw()


    def display(self):
        self.mainloop()


#  -----------------------------register window----------------------------
class CreateAccountWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.logic_controller = LogicController()
        self.config_window()
        self.create_widgets()
        self.configure(bg='#3a4c4d')

    def config_window(self):
        self.title('Create account')
        self.geometry('400x500')

    def create_widgets(self):
        factory = WidgetFactory()
        self.create_label = factory.create_label(self, 'CREATE NEW ACCOUNT', ('Courier', 20))
        self.create_label.pack(pady=10)

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



        account_types = ["Savings", "Checking", "Joint"]
        self.account_type_label = factory.create_label(self, "Type of account", ("Courier", 10))
        self.account_type_label.pack()

        self.account_type_combobox = ttk.Combobox(self, values=account_types)
        self.account_type_combobox.pack()
        self.account_type_combobox.set(account_types[0])



        self.initial_depo_label = factory.create_label(self, "Initial Deposit", ("Courier", 10))
        self.initial_depo_label.pack()

        self.initial_depo_entry = factory.create_entry(self)
        self.initial_depo_entry.pack()

        self.create_button = factory.create_button(self, "Create account", width=20, height=2, command=self.create_account)
        self.create_button.pack(pady=20)

        self.back_button = factory.create_button(self, 'Return', width=20, command=self.main_callback)
        self.back_button.pack(pady=20)

    def main_callback(self):
        self.destroy()
        MainWindow(LogicController)


    def create_account(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        account_type = self.account_type_combobox.get()
        initial_deposit = self.initial_depo_entry.get()

        if not all([name, username, password, confirm_password, account_type, initial_deposit]):
            messagebox.showerror('Error', 'All fields must be filled')
            return
        
        for account in UserManagement._savingsaccount + UserManagement._checkingaccount + UserManagement._jointaccount:
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
            initial_deposit_float = float(initial_deposit)
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid number for the initial deposit')
            return
        
        minimum_deposit = {'Savings': 500, 'Checking': 25000, 'Joint': 50000}
        if account_type == 'Savings':
            if float(initial_deposit) < minimum_deposit[account_type]:
                messagebox.showerror('Deposit Error', 'The initial minimum deposit for a Savings account is 500 Pesos')
                return
            
        elif account_type == 'Checking':
            if float(initial_deposit) < minimum_deposit[account_type]:
                messagebox.showerror('Deposit Error', 'The initial minimum deposit for a Checking account is 25,000 Pesos')
                return
            
        elif account_type == 'Joint':
            if float(initial_deposit) < minimum_deposit[account_type]:
                messagebox.showerror('Deposit Error', 'The initial minimum deposit for a Joint account is 50,000 Pesos')
                return
            
    
        BankFacade.register(self.logic_controller, name, username, password, account_type, initial_deposit)
        self.destroy()
        MainWindow(LogicController)



#  ---------------------------------- accounts window -----------------------

class AccountWindowBase(tk.Toplevel): # composite dp
    def __init__(self, parent):
        super().__init__(parent)
        self.config_window()
        self.create_widgets()
        self.configure(bg='#3a4c4d')

    def config_window(self):
        raise NotImplementedError("Subclasses must implement this method")

    def create_widgets(self):
        factory = WidgetFactory()
        self.show_info_button = factory.create_button(self, 'Show Account Information',command=self.open_information, width=30, height=3)
        self.show_info_button.pack(pady=10)

        self.deposit_button = factory.create_button(self, 'Deposit', command=self.open_deposit, width=30, height=3)
        self.deposit_button.pack(pady=10)

        self.withdraw_button = factory.create_button(self, 'Withdraw', command=self.open_withdraw, width=30, height=3)
        self.withdraw_button.pack(pady=10)

        self.check_balance_button = factory.create_button(self, 'Check Balance', command=self.open_balance, width=30, height=3)
        self.check_balance_button.pack(pady=10)

        self.logout_button = factory.create_button(self, 'Logout', command=self.logout, width=30, height=3)
        self.logout_button.pack(pady=10)    

    def logout(self):
        self.destroy()
        BankFacade.logout()

    def open_information(self):
        BankFacade.display_infomation(self)

    def open_deposit(self):
        DepositWindow(self.master, UserManagement.active_account)

    def open_withdraw(self):
        WithdrawWindow(self.master, UserManagement.active_account)

    def open_balance(self):
        BankFacade.check_balance(self)

    def open_account_options(self):
        AccountWindowBase(self.master)


class SavingsWindow(AccountWindowBase):
    def config_window(self):
        self.title('Savings Account')
        self.geometry('400x400')

class CheckingWindow(AccountWindowBase):
    def config_window(self):
        self.title('Checking Account')
        self.geometry('400x400')

class JointWindow(AccountWindowBase):
    def config_window(self):
        self.title('Joint Account')
        self.geometry('400x400')




# ------------------------------------account options-------------------------------

class DepositWindow(tk.Toplevel):
    def __init__(self, parent, account):
        super().__init__(parent)
        self.account = account
        self.config_window()
        self.create_widgets()
        self.configure(bg='#3a4c4d')

    def config_window(self):
        self.title('Deposit')
        self.geometry('400x400')

    def create_widgets(self):
        factory = WidgetFactory()

        self.deposit_label = factory.create_label(self, 'Deposit', ('Courier', 20))
        self.deposit_label.pack(pady=20)

        self.deposit_entry = factory.create_entry(self)
        self.deposit_entry.pack()

        self.deposit_button = factory.create_button(self, 'Submit', command=self.deposited, width=20, height=2)
        self.deposit_button.pack(pady=20)

    def deposited(self):
        amount_str = self.deposit_entry.get()
        
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror('Invalid Amount', 'Please enter a valid number for the deposit')
            return

        self.account.deposit(amount)
        print('Deposited')
        self.destroy()




class WithdrawWindow(tk.Toplevel):
    def __init__(self, parent, account):
        super().__init__(parent)
        self.account = account
        self.config_window()
        self.create_widgets()
        self.configure(bg='#3a4c4d')

    def config_window(self):
        self.title('Withdraw')
        self.geometry('400x400')

    def create_widgets(self):
        factory = WidgetFactory()

        self.withdraw_label = factory.create_label(self, 'Withdraw', ('Courier', 20))
        self.withdraw_label.pack(pady=20)

        self.withdraw_entry = factory.create_entry(self)
        self.withdraw_entry.pack()

        self.withdraw_button = factory.create_button(self, 'Submit', command=self.withdrawn, width=20, height=2)
        self.withdraw_button.pack(pady=20)

    def withdrawn(self):
        amount_str = self.withdraw_entry.get()
        
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror('Invalid Amount', 'Please enter a valid number for the withdrawal')
            return
        
        if amount > self.account.get_initial_balance():
            messagebox.showerror('Insufficient Funds', 'Withdrawal amount exceeds the account balance')
            return

        self.account.withdraw(amount)
        print('Withdrawn')
        self.destroy()


class AccountInformation(tk.Toplevel):
    def __init__(self, parent, account):
        super().__init__(parent)
        self.account = account
        self.config_window()
        self.create_widgets()
        self.configure(bg='#3a4c4d')

    def config_window(self):
        self.title('Account Informations')
        self.geometry('400x400')

    def create_widgets(self):
        factory = WidgetFactory()
        self.account_label = factory.create_label(self, 'Account Information', ('Courier', 20))
        self.account_label.pack(pady=20)

        self.get_name_label = factory.create_label(self, text=f'NAME:   {self.account.get_name()}')
        self.get_name_label.pack()

        self.get_username_label = factory.create_label(self, text=f'USERNAME:   {self.account.get_username()}')
        self.get_username_label.pack()
        
        self.get_password_label = factory.create_label(self, text=f'PASSWORD:   {self.account.get_password()}')
        self.get_password_label.pack()

        self.get_ID_label = factory.create_label(self, text=f'ACCOUNT ID:     {self.account.get_account_number()}')
        self.get_ID_label.pack()

        self.get_type_label = factory.create_label(self, text=f'    ACCOUNT TYPE:     {self.account.get_account_type()} Account')
        self.get_type_label.pack()

        self.get_balance_label = factory.create_label(self, text=f' BALANCE:     {self.account.get_initial_balance()}')
        self.get_balance_label.pack()

        self.return_button = factory.create_button(self, 'Return', command=self.back, width=30, height=2)
        self.return_button.pack(pady=20)

    def back(self):
        self.destroy()
    


#  ----------------------------------bank facade---------------------------------------------
class BankFacade:
    def __init__(self, logic_controller) -> None:
        self.logic_controller = LogicController()
        self.bank_main =  MainWindow(self.logic_controller)

    @staticmethod
    def login(logic_controller, username, password):
        logic_controller.handle_login_control(username, password)

    @staticmethod
    def logout():
        logic_controller.handle_logout_control()

    @staticmethod
    def register(logic_controller, name, username, password, account_type, initial_deposit):
        logic_controller.handle_account_creation_control(name, username, password, account_type, initial_deposit)

    def display_infomation(self):
        user = UserManagement.active_account
        AccountInformation(self, user)

    def deposit(self, amount):
        UserManagement.active_account.deposit(amount)

    def withdraw(self, amount):
        UserManagement.active_account.withdraw(amount)

    def check_balance(self):
        balance = UserManagement.active_account.get_initial_balance()
        messagebox.showinfo("Account Balance", f"Your account balance is {balance}")
        print(f'Total balance: {balance}')
  
    def start(self):
        self.bank_main.mainloop()




if __name__ == "__main__":
    logic_controller = LogicController()
    facade = BankFacade(logic_controller)
    facade.start()