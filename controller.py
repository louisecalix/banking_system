from abc import ABC, abstractmethod
from tkinter import messagebox
from users import User, UserManagement
from accounts import SavingsAccount, CheckingAccount, JointAccount
import json


class LoginTemplate(ABC):
    @abstractmethod
    def create_user(self, account_data):
        pass

    @abstractmethod
    def handle_user_accounts(self, user, accounts_data):
        pass

    @abstractmethod
    def display_error(self, message):
        pass

    def handle_login_control(self, username, password):
        try:
            with open("info.json", "r") as file:
                info = json.load(file)
                for account_data in info["user"]:
                    if account_data['username'] == username and account_data['password'] == password:
                        user = self.create_user(account_data)
                        self.handle_user_accounts(user, account_data['accounts'])
                        UserManagement.active_account = user
                        print('Logged in successfully!')
                        break
                else:
                    print('Login Failed')
                    self.display_error('Credentials Invalid')

        except FileNotFoundError:
            self.display_error('No accounts found. Please create an account.')

    @abstractmethod
    def handle_logout_control(self):
        UserManagement.reset_active_account()
        print('User logged out successfully')
        self.mainwindow_callback()

    @abstractmethod
    def handle_account_creation_control(self, name, username, password, age, gender, address, phone_number):
        pass

    @abstractmethod
    def mainwindow_callback(self):
        pass


class LogicController(LoginTemplate):
    def create_user(self, account_data):
        return User(
            account_data['name'],
            account_data['username'],
            account_data['password'],
            account_data['age'],
            account_data['gender'],
            account_data['address'],
            account_data['phone_number'],
            account_data['user_id']
        )

    def handle_user_accounts(self, user, accounts_data):
        for account_info in accounts_data:
            account_type = account_info['type']
            balance = account_info['balance']
            if account_type == "Savings":
                account = SavingsAccount(user, balance)
            elif account_type == "Checking":
                account = CheckingAccount(user, balance)
            elif account_type == "Joint":
                co_holder = "Co-holder"
                account = JointAccount(user, balance, co_holder)
            else:
                raise ValueError("Invalid account type")

            user.add_account(account)

    def display_error(self, message):
        messagebox.showerror('Login Error', message)

    def handle_logout_control(self):
        from gui import LoginWindow
        super().handle_logout_control()
        LoginWindow()

    def handle_account_creation_control(self, name, username, password, age, gender, address, phone_number):
        try:
            with open("info.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {"user": []}
        except json.JSONDecodeError:
            existing_data = {"user": []}

        # Calculate the user_id based on the length of existing users
        user_id = len(existing_data["user"])

        new_user = {
            "name": name,
            "username": username,
            "password": password,
            "age": age,
            "gender": gender,
            "address": address,
            "phone_number": phone_number,
            "user_id": user_id,
            "accounts": []
        }

        existing_data["user"].append(new_user)

        with open("info.json", "w") as file:
            json.dump(existing_data, file, indent=4)

        new_user_obj = User(name, username, password, age, gender, address, phone_number, user_id)
        UserManagement._customer.append(new_user_obj)
        messagebox.showinfo(f"New User", f"User with User ID of [{user_id}] is created")


    def mainwindow_callback(self):
        super().mainwindow_callback()


class BankFacade:
    def __init__(self, logic_controller=LogicController()):
        from gui import LoginWindow
        self.logic_controller = logic_controller
        self.bank_main = LoginWindow()

    @staticmethod
    def login(logic_controller, username, password):
        logic_controller.handle_login_control(username, password)

    @staticmethod
    def logout():
        logic_controller = LogicController()
        logic_controller.handle_logout_control()

    @staticmethod
    def register(logic_controller, name, username, password, age, gender, address, phone_number):
        logic_controller.handle_account_creation_control(name, username, password, age, gender, address, phone_number)

    def deposit(self, amount):
        UserManagement.active_account.deposit(amount)

    def withdraw(self, amount):
        UserManagement.active_account.withdraw(amount)

    def start(self):
        self.bank_main.mainloop()