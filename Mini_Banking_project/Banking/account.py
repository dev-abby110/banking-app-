import sys
class BankAccount:
    account_number=1210001450000
    def __init__(self,name, balance=0):
        self.name = name
        self.account_number = BankAccount.account_number
        BankAccount.account_number += 1
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True, f"Deposit of {amount} successful. New balance: {self.__balance}"
        else:
            return False, f"Deposit of {amount} failed. Amount must be positive."

    def withdraw(self, amount):
        if 0 < amount:
            if amount <= self.__balance:
                self.__balance -= amount
                return True, f"Withdrawal of {amount} successful. New balance: {self.__balance}"
            else:
                return False, f"Withdrawal of {amount} failed. Insufficient funds. Current balance: {self.__balance}"
        return False, "Withdrawal amount must be positive."

    def get_balance(self):
        return self.__balance
    
    def display_balance(self):
        return f"Balance: {self.__balance} for account {self.account_number}"


class SavingsAccount(BankAccount):
    def __init__(self, name, balance=0, interest_rate=0.05, account_type="Savings"):
        super().__init__(name, balance)
        self.account_type = account_type
        self.interest_rate = interest_rate

    def calculate_interest(self):
        months=int(input("Enter number of months to apply interest: "))
        if months < 0:
            print("Months cannot be negative.")
            return
        interest = self.get_balance() * self.interest_rate * months
        self.deposit(interest)
        print(f"Interest applied: {interest}. New balance: {self.get_balance()}")

class CurrentAccount(BankAccount):
    def __init__(self, name, balance=0, overdraft_limit=10000, account_type="Current"):
        super().__init__(name, balance)
        self.account_type = account_type
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.get_balance() + self.overdraft_limit:
                self._BankAccount__balance -= amount
                print(f"Withdrawal of {amount} successful. New balance: {self.get_balance()}")
            else:
                print(f"Withdrawal of {amount} failed. Exceeds overdraft limit.")
        else:
            print("Withdrawal amount must be positive.")


if __name__ == "__main__":
   account = BankAccount("Alice", 1000)
   print(account.display_balance())
   print(account.deposit(500))
   print(account.withdraw(200))
   print(account.display_balance())

   savings_account = SavingsAccount("Bob", 2000)
   print(savings_account.display_balance())
   savings_account.calculate_interest()
   print(savings_account.display_balance())

   current_account = CurrentAccount("Charlie", 3000)
   print(current_account.display_balance())
   print(current_account.withdraw(3500))
   print(current_account.display_balance())