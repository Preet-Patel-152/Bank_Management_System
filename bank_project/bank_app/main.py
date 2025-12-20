import json
import os
from bank_project.account import bank
from bank_project.bank_app.services.storage import save_data, load_data
from bank_project.bank_app.services.bank_service import BankService


# =============================
# Constants & Configuration
# =============================

# File used to persist account data between program runs
DATA_FILE = os.path.join(os.path.dirname(
    __file__), "..", "data", "accounts.json")
DATA_FILE = os.path.abspath(DATA_FILE)

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
# App Startup
# =============================


def main():
    """Main entry point for the Bank Management System."""

    # Load existing accounts from file (if any)
    accounts = load_data()
    service = BankService(accounts)

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
            password = input("Enter account password: ").strip()

            # Prevent duplicate usernames
            if name in accounts:
                print("Username already exists. Try again.")
                continue

            # Create the account object and save immediately
            else:
                try:
                    service.create_account(name, password)
                    save_data(service.accounts)
                    print("Account created successfully!")
                except ValueError as e:
                    print(e)
                continue

        # -------------------------
        # Login to existing account
        # -------------------------
        elif action == "exi":
            name = input("Enter account holder name: ").strip()
            password = input("Enter account password: ").strip()

            # Check username exists and password matches
            try:
                current_account = service.login(name, password)
                print("Access granted.")
            except ValueError as e:
                print(e)
                continue

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
                            amount = float(
                                input("Enter amount to deposit: "))

                            # Reject zero/negative deposits
                            if amount <= 0:
                                print("Deposit amount must be positive.")
                                continue
                            else:
                                try:
                                    print(service.deposit(
                                        current_account, amount))
                                    save_data(service.accounts)
                                except ValueError as e:
                                    print(e)

                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                            continue

                    # -------------------------
                    # Withdraw money
                    # -------------------------
                    case "withdraw":

                        try:
                            amount = float(input("Enter amount to withdraw: "))
                            print(service.withdraw(current_account, amount))
                            save_data(service.accounts)
                        except ValueError as e:
                            print(e)

                    # -------------------------
                    # Check balance (read-only)
                    # -------------------------
                    case "check balance":

                        print(current_account.check_balance())

                    # -------------------------
                    # Change password
                    # -------------------------
                    case "change password":

                        new_password = input(
                            "Enter new password: ").strip()
                        print(current_account.change_accout_password(
                            new_password))
                        save_data(accounts)  # Save new password

                    # -------------------------
                    # Delete account (only if balance is zero)
                    # -------------------------
                    case "delete account":

                        print(
                            f"\nYou are about to delete the account for {current_account.name}.")
                        print(
                            "\nWARNING: This action is permanent and cannot be undone.")
                        confirm = input(
                            f"Type 'DELETE {current_account.name.upper()}' to confirm: ").strip()

                        try:
                            service.delete_account(current_account, confirm)
                            save_data(service.accounts)
                            print(
                                f"\nSUCCESS: Account for {current_account.name} has been closed and deleted.")
                            break
                        except ValueError as e:
                            print(e)

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

                        try:
                            amount = float(input("Enter amount to transfer: "))
                            print(service.transfer(
                                current_account, recipient_name, amount))
                            save_data(service.accounts)
                        except ValueError as e:
                            print(e)

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


if __name__ == "__main__":
    main()
