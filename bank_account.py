import json
import os
from account import bank

# =============================
# Constants & Configuration
# =============================

# File used to persist account data between program runs
DATA_FILE = "accounts.json"

# Valid actions for the main menu (create, login, exit)
MAIN_ACTIONS = {"new", "exi", "done"}

# Valid actions available after logging into an account
ACCOUNT_ACTIONS = {
    "deposit",
    "withdraw",
    "check balance",
    "change password",
    "transfer",
    "check history",
    "delete account",
    "dev",
    "exit"
}

# =============================
# Persistence (Save / Load)
# =============================


def save_data(accounts):

    serializable_data = {}

    # Convert each bank object into a dictionary
    for name, acc in accounts.items():
        serializable_data[name] = {
            "name": acc.name,
            "password": acc.password,
            "balance": acc.balance,
            "history": acc.history
        }

    # Write the dictionary to accounts.json
    with open(DATA_FILE, "w") as f:
        json.dump(serializable_data, f, indent=4)


def load_data():

    # Load accounts from a JSON file and rebuild bank objects.
    # If the file doesn't exist or is corrupted, return an empty dict.

    # If no save file exists, start with no accounts
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as f:
            raw_data = json.load(f)
            loaded_accounts = {}

            # Reset the class-level counter before rebuilding objects
            bank.num_bank_acc = 0

            # Reconstruct each account back into a bank object
            for name, info in raw_data.items():
                # Reconstruct the object
                acc = bank(info["name"], info["password"], info["balance"])
                acc.history = info["history"]  # Restore the history list
                loaded_accounts[name] = acc
            return loaded_accounts

    # If JSON is broken or missing expected keys, fail safely
    except (json.JSONDecodeError, KeyError):
        return {}

# =============================
# App Startup
# =============================


# Load existing accounts from file (if any)
accounts = load_data()


is_running = True

# =============================
# Main Menu Loop (Create / Login / Exit)
# =============================

while is_running:

    # Main prompt: choose new account, existing account, or exit
    action = input("would you like to create a new account or access existing account?\n"
                   "type new for new account, exi for existing account or done to exit out the program: ").strip().lower()

    # Validate the main menu choice
    if action not in MAIN_ACTIONS:
        print("Invalid action. Please try again.")
        continue

    # -------------------------
    # Exit program safely
    # -------------------------
    if action == "done":
        save_data(accounts)
        print("THANK YOU FOR USING THE BANK ACCOUNT APP")
        is_running = False

    # -------------------------
    # Create a new account
    # -------------------------
    elif action == "new":
        name = input("Enter account holder name: ").strip()

        # Basic name validation: letters only
        if name.isalpha() == False:
            print("Name must contain only alphabetic characters. Try again.")
            continue

        password = input("Enter account password: ").strip()

        # Prevent duplicate usernames
        if name in accounts:
            print("Username already exists. Try again.")
            continue

        # Create the account object and save immediately
        else:
            accounts[name] = bank(name, password, 0)
            save_data(accounts)
            print("Account created successfully!")
            continue

    # -------------------------
    # Login to existing account
    # -------------------------
    elif action == "exi":
        name = input("Enter account holder name: ").strip()

        # Validate name format
        if name.isalpha() == False:
            print("Name must contain only alphabetic characters. Try again.")
            continue

        password = input("Enter account password: ").strip()

        # Check username exists and password matches
        if name in accounts and accounts[name].password == password:
            current_account = accounts[name]
            print("Access granted.")

            # =============================
            # Account Management Loop
            # =============================
            while True:

                # Show available account actions
                print(
                    "\nAvailable actions:\n"
                    "-deposit\n-withdraw\n-check balance\n-change password\n-transfer\n-check history\n-delete account\n-exit")

                user_action = input("Enter action: ").strip().lower()

                # Validate user action
                if user_action not in ACCOUNT_ACTIONS:
                    print("Invalid action. Please try again.")
                    continue

                # Use match-case to route to the selected feature
                match user_action:

                    # -------------------------
                    # Deposit money
                    # -------------------------
                    case "deposit":

                        try:
                            amount = float(input("Enter amount to deposit: "))

                            # Reject zero/negative deposits
                            if amount <= 0:
                                print("Deposit amount must be positive.")
                                continue
                            else:
                                print(current_account.deposit(amount))
                                save_data(accounts)  # Save after state change

                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                            continue

                    # -------------------------
                    # Withdraw money
                    # -------------------------
                    case "withdraw":

                        try:
                            amount = float(input("Enter amount to withdraw: "))

                            # Reject invalid or overdraft withdrawals
                            if amount <= 0 or amount > current_account.balance:
                                print(
                                    "Withdrawal amount must be positive and within available balance.")
                                continue
                            else:
                                print(current_account.withdraw(amount))
                                save_data(accounts)  # Save after state change

                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                            continue

                    # -------------------------
                    # Check balance (read-only)
                    # -------------------------
                    case "check balance":

                        print(current_account.check_balance())

                    # -------------------------
                    # Change password
                    # -------------------------
                    case "change password":

                        new_password = input("Enter new password: ").strip()
                        print(current_account.change_accout_password(new_password))
                        save_data(accounts)  # Save new password

                    # -------------------------
                    # Delete account (only if balance is zero)
                    # -------------------------
                    case "delete account":

                        # Do not allow deleting accounts with remaining funds
                        if current_account.balance > 0:
                            print(
                                f"\nBLOCKER: You cannot delete an account with a remaining balance.")
                            print(
                                f"Current Balance: ${current_account.balance}")
                            print(
                                "Please withdraw all funds before attempting to delete this account.")
                            continue

                        # Confirmation step to avoid accidental deletion
                        print(
                            f"\nYou are about to delete the account for {current_account.name}.")
                        print(
                            "\nWARNING: This action is permanent and cannot be undone.")
                        confirm = input(
                            f"Type 'DELETE {current_account.name.upper()}' to confirm: ").strip()

                        if confirm == f"DELETE {current_account.name.upper()}":
                            # Remove from memory and update total counter
                            accounts.pop(current_account.name)
                            bank.num_bank_acc -= 1

                            # Save the empty state to JSON
                            save_data(accounts)

                            print(
                                f"\nSUCCESS: Account for {current_account.name} has been closed and deleted.")
                            break  # Exit the account management loop
                        else:
                            print(
                                "\nDeletion cancelled. Confirmation text did not match.")

                    # -------------------------
                    # View transaction history
                    # -------------------------
                    case "check history":
                        print("\n--- Transaction History ---")
                        print(current_account.get_history())

                    # -------------------------
                    # Transfer money to another user
                    # -------------------------
                    case "transfer":

                        recipient_name = input(
                            "Enter recipient account holder name: ").strip()
                        recipient_account = accounts.get(recipient_name)

                        # Validate recipient exists
                        if not recipient_account:
                            print(
                                f"Error: Account for '{recipient_name}' not found.")
                            continue

                        # Prevent transferring to yourself
                        if recipient_name == current_account.name:
                            print("Error: You cannot transfer money to yourself.")
                            continue

                        try:
                            amount = float(
                                input("Enter amount to transfer: "))

                            # Validate transfer amount
                            if amount <= 0 or amount > current_account.balance:
                                print(
                                    "Invalid amount. It must be positive and not exceed your balance.")
                                continue

                            # Perform transfer: withdraw from sender, deposit to recipient
                            current_account.withdraw(amount)
                            recipient_account.deposit(amount)

                            # Save both accounts after transfer
                            save_data(accounts)

                            print(
                                f"Transferred ${amount} to {recipient_name}.")

                        except ValueError:
                            print("Invalid input. Please enter a numeric amount.")

                    # -------------------------
                    # Developer mode (admin tools)
                    # -------------------------
                    case "dev":
                        print("Developer mode activated.")
                        print('        _   ,_,   _')
                        print('       / `\'=) (=\'` \\')
                        print('      /.-.-.\\ /.-.-.\\ ')
                        print('      `      "      `')

                        # Separate loop for dev tools
                        while True:

                            dev_action = input(
                                "what would you like to do check number of accounts, check total bank balance, or quit? ").strip().lower()

                            match dev_action:
                                case "check number of accounts":
                                    print(
                                        f"Total bank accounts: {bank.num_bank_acc}")

                                case "check total bank balance":
                                    print(
                                        f"Total bank balance across all accounts: ${bank.total_bank_balance}")

                                case "quit":
                                    print("Exiting developer mode.")
                                    break
                                case _:
                                    print(
                                        "Invalid developer action. Please try again.")

                    # -------------------------
                    # Exit account management
                    # -------------------------
                    case "exit":
                        print("Exiting account management.")
                        save_data(accounts)
                        break

                    case _:
                        print("Invalid action. Please try again.")
        else:
            # Login failed
            print("Access denied. Incorrect name or password.")
            continue
