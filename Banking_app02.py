import random
import json
import os

# Dictionary to hold account data
accounts = {}

DATA_FILE = "accounts_data.json"

# Load data from file if it exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        accounts = json.load(f)


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(accounts, f, indent=4)


# Create an Account
def create_account():
    account_number = str(random.randint(10000, 99999))
    if account_number in accounts:
        print("Account number collision. Try again.")
        return

    name = input("Enter account holder name: ").strip()
    password = input("Set a password for your account: ").strip()
    try:
        initial_balance = float(input("Enter initial balance: "))
        if initial_balance < 0:
            print("Initial balance must be non-negative.")
            return
    except ValueError:
        print("Invalid input for balance.")
        return

    accounts[account_number] = {
        'name': name,
        'password': password,
        'balance': initial_balance,
        'transactions': [f"Account created with balance: {initial_balance}"]
    }
    save_data()
    print(f"Account created successfully! Your account number is {account_number}")


def authenticate(account_number):
    password = input("Enter password: ")
    return password == accounts[account_number]['password']


# Deposit money
def deposit_money():
    account_number = input('Enter your Account no: ')
    if account_number not in accounts:
        print('Account not found!')
        return
    if not authenticate(account_number):
        print("Authentication failed.")
        return

    try:
        amount = float(input('Enter the amount to deposit: '))
        if amount <= 0:
            print('Please enter a positive amount.')
            return
    except ValueError:
        print('Invalid input')
        return

    accounts[account_number]['balance'] += amount
    accounts[account_number]['transactions'].append(f'Deposited: {amount}')
    save_data()
    print('Deposit successful!')


# Withdraw money
def withdraw_money():
    account_number = input('Enter your account no: ')
    if account_number not in accounts:
        print('Account not found')
        return
    if not authenticate(account_number):
        print("Authentication failed.")
        return

    try:
        amount = float(input('Enter amount to withdraw: '))
        if amount <= 0:
            print('Amount must be positive')
            return
        if amount > accounts[account_number]['balance']:
            print('Insufficient balance')
            return
    except ValueError:
        print('Invalid input')
        return

    accounts[account_number]['balance'] -= amount
    accounts[account_number]['transactions'].append(f'Withdrawn: {amount}')
    save_data()
    print('Withdrawal successful')


# Check balance
def check_balance():
    account_number = input('Enter account no: ')
    if account_number not in accounts:
        print('Account not found')
        return
    if not authenticate(account_number):
        print("Authentication failed.")
        return

    balance = accounts[account_number]['balance']
    print(f'Current balance: {balance}')


# Transaction history
def transaction_history():
    account_number = input('Enter your account no: ')
    if account_number not in accounts:
        print('Account not found')
        return
    if not authenticate(account_number):
        print("Authentication failed.")
        return

    print('Transactions history:')
    for txn in accounts[account_number]['transactions']:
        print(txn)


# Bonus 1: Transfer Money
def transfer_money():
    from_acc = input("Enter your account number: ")
    if from_acc not in accounts:
        print("Sender account not found.")
        return
    if not authenticate(from_acc):
        print("Authentication failed.")
        return

    to_acc = input("Enter recipient account number: ")
    if to_acc not in accounts:
        print("Recipient account not found.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0 or amount > accounts[from_acc]['balance']:
            print("Invalid amount or insufficient balance.")
            return
    except ValueError:
        print("Invalid amount")
        return

    accounts[from_acc]['balance'] -= amount
    accounts[to_acc]['balance'] += amount
    accounts[from_acc]['transactions'].append(f"Transferred {amount} to {to_acc}")
    accounts[to_acc]['transactions'].append(f"Received {amount} from {from_acc}")
    save_data()
    print("Transfer successful.")


# Bonus 4: Interest Calculation
def calculate_interest():
    account_number = input("Enter your account number: ")
    if account_number not in accounts:
        print("Account not found.")
        return
    if not authenticate(account_number):
        print("Authentication failed.")
        return

    try:
        rate = float(input("Enter annual interest rate (%): "))
        time = float(input("Enter time in years: "))
        principal = accounts[account_number]['balance']
        interest = (principal * rate * time) / 100
        accounts[account_number]['balance'] += interest
        accounts[account_number]['transactions'].append(f"Interest added: {interest}")
        save_data()
        print(f"Interest of {interest} added. New balance: {accounts[account_number]['balance']}")
    except ValueError:
        print("Invalid input.")


# Menu loop
def main():
    while True:
        print('\n------ Main Banking Application --------')
        print('1. Create Account')
        print('2. Deposit Money')
        print('3. Withdraw Money')
        print('4. Check Balance')
        print('5. Transactions History')
        print('6. Transfer Money (Bonus)')
        print('7. Interest Calculation (Bonus)')
        print('8. Exit')

        choice = input('Enter your choice: ')
        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            transaction_history()
        elif choice == '6':
            transfer_money()
        elif choice == '7':
            calculate_interest()
        elif choice == '8':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
