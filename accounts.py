from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, user, account_type, initial_balance) -> None:
        self.__user = user
        self.__account_type = account_type
        self.__initial_balance = float(initial_balance)

    @abstractmethod
    def _credit(self, amount):
        pass

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def _debit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def get_user(self):
        pass

    @abstractmethod
    def get_account_type(self):
        pass

    @abstractmethod
    def get_initial_balance(self):
        pass

    @abstractmethod
    def set_initial_balance(self, amount):
        pass

class BankAccount(Account):
    def __init__(self, user, account_type, initial_balance) -> None:
        super().__init__(user, account_type, initial_balance)
        self._user = user
        self._account_type = account_type
        self._initial_balance = float(initial_balance)

    def get_user(self):
        return self._user
    
    def get_account_type(self):
        return self._account_type
    
    def get_initial_balance(self):
        return self._initial_balance
    
    def set_initial_balance(self, amount):
        self._initial_balance = amount
        return self._initial_balance
    

    def _credit(self, amount):
        current_balance = self._initial_balance
        new_balance_amount = current_balance + amount
        self._initial_balance = new_balance_amount

    def deposit(self, amount):
        if amount <= 0:
            print('Amount must be greater than 0')
        else:
            self._credit(amount)
            print(f'New Balance: {self.get_initial_balance()}')

    def _debit(self, amount):
        current_balance = self._initial_balance
        new_balance_amount = current_balance - amount
        self._initial_balance = new_balance_amount

    def withdraw(self, amount):
        if amount <= 0:
            print('Amount must be greater than 0')
        elif amount > self._initial_balance:
            print('Insufficient funds')
        else:
            self._debit(amount)
            print(f'New Balance: {self.get_initial_balance()}')

#  --------------------------account type-----------------------------------------------------
class SavingsAccount(BankAccount):
    def __init__(self, user, initial_balance):
        super().__init__(user, "Savings", initial_balance)

    def get_user(self):
        return self._user


class CheckingAccount(BankAccount):
    def __init__(self, user, initial_balance):
        super().__init__(user, "Checking", initial_balance)

    def get_user(self):
        return self._user

class JointAccount(BankAccount):
    def __init__(self, user, initial_balance, co_holder):
        super().__init__(user, "Joint", initial_balance)
        self.__co_holder = co_holder

    def get_co_holder(self):
        return self.__co_holder
    
    def get_user(self):
        return self._user
