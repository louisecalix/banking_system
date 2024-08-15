import json

class User:
    def __init__(self, name, username, password, age, gender, address, phone_number, user_id) -> None:
        self.__name = name
        self.__username = username
        self.__password = password
        self.__age = age
        self.__gender = gender
        self.__address = address
        self.__phone_number = phone_number
        self.__user_id = user_id
        self.__accounts = []

    def get_name(self):
        return self.__name
    
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password
    
    def get_age(self):
        return self.__age
    
    def get_gender(self):
        return self.__gender
    
    def get_address(self):
        return self.__address
    
    def get_phone_number(self):
        return self.__phone_number
    
    def get_user_id(self):
        return self.__user_id

    def add_account(self, account):
        self.__accounts.append(account)

    def get_accounts(self):
        return self.__accounts

#  --------------------------------user management------------------------------
class UserManagement:
    _customer = []
    active_account = None

    @staticmethod
    def save_account_data():
        with open("info.json", "r") as file:
            load_data = json.load(file)

        accs = []

        for account in UserManagement.active_account.get_accounts():
            accs.append({
                "type": account.get_account_type(),
                "balance": account.get_initial_balance()
            })

        index = UserManagement.active_account.get_user_id()

        load_data["user"][index]["accounts"] = accs

        with open("info.json", "w") as file:
            json.dump(load_data, file, indent=4)

    @staticmethod
    def reset_active_account():
        UserManagement.active_account = None  