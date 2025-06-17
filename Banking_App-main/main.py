from Banking.account import SavingsAccount, CurrentAccount
from Banking.transactions import deposit, withdraw


accounts = {}
def create_account():
    name = input("Enter account holder's name: ").strip()
    account_type = input("Enter account type (Savings/Current): ").strip().lower()
    initial_deposit = input("Enter initial deposit amount: ")
    if account_type == "savings":
        account = SavingsAccount(name, balance=float(initial_deposit))
    elif account_type == "current":
        account = CurrentAccount(name, balance=float(initial_deposit))
    else:
        print("Invalid account type. Please choose either 'Savings' or 'Current'.")
        return None
    accounts[account.account_number] = account
    print(f"Account created successfully for {account.account_number} with initial deposit of {initial_deposit}.")
    return account

def login():
    account_number = int(input("Enter your account number: "))
    if account_number in accounts:
        user_account = accounts[account_number]
        str1 = f" Welcome {user_account.name} to the Bank Of Ro706 "
        str1 = str1.center(100,"*")
        print()
        print(str1)
        print()
        while True:
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check your balance")
            if isinstance(user_account, SavingsAccount):
                print("4. Calculate Interest")
            print("99. logout")

            action = input("Choose an action: ").strip().lower()
            if action == "deposit" or action == "1":
                amount = float(input("Enter deposit amount: "))
                deposit(user_account, amount)
            elif action == "withdraw" or action == "2":
                amount = float(input("Enter withdrawal amount: "))
                withdraw(user_account, amount)
            elif action == "check balance" or action == "3":
                print("Current Balance:", user_account.get_balance())
            elif action == "calculate_interest" or action == "4" and isinstance(user_account, SavingsAccount):
                print("Calculating interest for Savings Account.")
                user_account.calculate_interest()
            elif action == "logout" or action == "99":
                print("Logging out of the banking system.")
                break
            else:
                print("Invalid action. Please try again.")
            user_account.display_balance()
    else:
        print("Account not found. Please create an account first.")
        return None
    
def main():
    str1 = f" Welcome to the Bank Of Ro706 - Banking System "
    str1 = str1.center(100,"*")
    print()
    print(str1)
    print()
    while True:
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        action = input("Choose an action: ").strip().lower()
        if action == "create account" or action == "1":
            create_account()
        elif action == "login" or action == "2":
            login()
        elif action == "exit" or action == "3":
            print("Thanks for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid action. Please try again.")

if __name__ == "__main__":
   main()