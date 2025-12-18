import json
import os
from account import bank


def save_data(accounts):

    serializable_data = {}
    for name, acc in accounts.items():
        serializable_data[name] = {
            "name": acc.name,
            "password": acc.password,
            "balance": acc.balance,
            "history": acc.history
        }
    with open("accounts.json", "w") as f:
        json.dump(serializable_data, f, indent=4)


def load_data():

    if not os.path.exists("accounts.json"):
        return {}

    try:
        with open("accounts.json", "r") as f:
            raw_data = json.load(f)
            loaded_accounts = {}

            bank.num_bank_acc = 0
            for name, info in raw_data.items():
                # Reconstruct the object
                acc = bank(info["name"], info["password"], info["balance"])
                acc.history = info["history"]  # Restore the history list
                loaded_accounts[name] = acc
            return loaded_accounts
    except (json.JSONDecodeError, KeyError):
        return {}


accounts = load_data()


is_running = True

while is_running:

    action = input("would you like to create a new account or access existing account?\n"
                   "type new for new account, exi for existing account or done to exit out the program: ").strip().lower()

    if action not in ["new", "exi", "done"]:
        print("Invalid action. Please try again.")
        continue

    if action == "done":
        save_data(accounts)
        print("THANK YOU FOR USING THE BANK ACCOUNT APP")
        is_running = False

    elif action == "new":
        name = input("Enter account holder name: ").strip()

        if name.isalpha() == False:
            print("Name must contain only alphabetic characters. Try again.")
            continue

        password = input("Enter account password: ").strip()

        if name in accounts:
            print("Username already exists. Try again.")
            continue

        else:
            accounts[name] = bank(name, password, 0)
            save_data(accounts)
            print("Account created successfully!")
            continue

    elif action == "exi":
        name = input("Enter account holder name: ").strip()

        if name.isalpha() == False:
            print("Name must contain only alphabetic characters. Try again.")
            continue

        password = input("Enter account password: ").strip()

        if name in accounts and accounts[name].password == password:
            bank_acc = accounts[name]
            print("Access granted.")

            while True:

                print(
                    "\nAvailable actions:\n"
                    "-deposit\n-withdraw\n-check balance\n-change password\n-transfer\n-check history\n-delete account\n-exit")

                user_action = input("Enter action: ").strip().lower()

                if user_action not in ["deposit", "withdraw", "check balance", "change password", "transfer", "dev", "exit", "check history", "delete account"]:
                    print("Invalid action. Please try again.")
                    continue

                match user_action:
                    case "deposit":

                        try:
                            amount = float(input("Enter amount to deposit: "))

                            if amount <= 0:
                                print("Deposit amount must be positive.")
                                continue
                            else:
                                print(bank_acc.deposit(amount))
                                save_data(accounts)

                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                            continue

                    case "withdraw":
                        try:
                            amount = float(input("Enter amount to withdraw: "))

                            if amount <= 0 or amount > bank_acc.balance:
                                print(
                                    "Withdrawal amount must be positive and within available balance.")
                                continue
                            else:
                                print(bank_acc.withdraw(amount))
                                save_data(accounts)

                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                            continue

                    case "check balance":
                        print(bank_acc.check_balance())

                    case "change password":
                        new_password = input("Enter new password: ").strip()
                        print(bank_acc.change_acccout_password(new_password))
                        save_data(accounts)

                    case "delete account":

                        if bank_acc.balance > 0:
                            print(
                                f"\nBLOCKER: You cannot delete an account with a remaining balance.")
                            print(f"Current Balance: ${bank_acc.balance}")
                            print(
                                "Please withdraw all funds before attempting to delete this account.")
                            continue

                        print(
                            f"\nYou are about to delete the account for {bank_acc.name}.")
                        print(
                            "\nWARNING: This action is permanent and cannot be undone.")
                        confirm = input(
                            f"Type 'DELETE {bank_acc.name.upper()}' to confirm: ").strip()

                        if confirm == f"DELETE {bank_acc.name.upper()}":
                            # 3. Remove from memory and update total counter
                            accounts.pop(bank_acc.name)
                            bank.num_bank_acc -= 1

                            # 4. Save the empty state to JSON
                            save_data(accounts)

                            print(
                                f"\nSUCCESS: Account for {bank_acc.name} has been closed and deleted.")
                            break  # Exit the account management loop
                        else:
                            print(
                                "\nDeletion cancelled. Confirmation text did not match.")

                    case "check history":
                        print("\n--- Transaction History ---")
                        print(bank_acc.get_history())

                    case "transfer":

                        recipient_name = input(
                            "Enter recipient account holder name: ").strip()
                        accounts_recipient = accounts.get(recipient_name)

                        if not accounts_recipient:
                            print(
                                f"Error: Account for '{recipient_name}' not found.")
                            continue

                        if recipient_name == bank_acc.name:
                            print("Error: You cannot transfer money to yourself.")
                            continue

                        try:
                            amount = float(
                                input("Enter amount to transfer: "))

                            if amount <= 0 or amount > bank_acc.balance:
                                print(
                                    "Invalid amount. It must be positive and not exceed your balance.")
                                continue

                            bank_acc.withdraw(amount)
                            accounts_recipient.deposit(amount)
                            save_data(accounts)
                            print(
                                f"Transferred ${amount} to {recipient_name}.")

                        except ValueError:
                            print("Invalid input. Please enter a numeric amount.")

                    case "dev":
                        print("Developer mode activated.")
                        print('        _   ,_,   _')
                        print('       / `\'=) (=\'` \\')
                        print('      /.-.-.\\ /.-.-.\\ ')
                        print('      `      "      `')

                        while True:

                            dev_action = input(
                                "what would you like to do check number of accounts, check total bank balance, or quit? ").strip().lower()

                            match dev_action:
                                case "check number of accounts":
                                    print(
                                        f"Total bank accounts: {bank.num_bank_acc}")

                                case "check total bank balance":
                                    print(
                                        f"Total bank balance across all accounts: ${bank.toatal_bank_balance}")

                                case "quit":
                                    print("Exiting developer mode.")
                                    break
                                case _:
                                    print(
                                        "Invalid developer action. Please try again.")

                    case "exit":
                        print("Exiting account management.")
                        save_data(accounts)
                        break

                    case _:
                        print("Invalid action. Please try again.")
        else:
            print("Access denied. Incorrect name or password.")
            continue


# add some comments
