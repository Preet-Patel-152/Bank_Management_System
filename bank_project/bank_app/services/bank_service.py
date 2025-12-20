# bank_project/bank_app/services/bank_service.py

from bank_project.account import bank


class BankService:
    """Business logic layer (no input/print here)."""

    def __init__(self, accounts):
        self.accounts = accounts

    # -------- Validation helpers --------
    @staticmethod
    def validate_name(name):
        if not name or not name.strip():
            raise ValueError("Name cannot be empty.")
        if not name.isalpha():
            raise ValueError("Name must contain only alphabetic characters.")

    @staticmethod
    def validate_amount(amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")

    # -------- Account actions --------
    def create_account(self, name, password):
        self.validate_name(name)
        if name in self.accounts:
            raise ValueError("Username already exists.")
        acc = bank(name, password, 0)
        self.accounts[name] = acc
        return acc

    def login(self, name, password):
        self.validate_name(name)
        acc = self.accounts.get(name)
        if not acc or acc.password != password:
            raise ValueError("Access denied. Incorrect name or password.")
        return acc

    def deposit(self, acc, amount):
        self.validate_amount(amount)
        return acc.deposit(amount)

    def withdraw(self, acc, amount):
        self.validate_amount(amount)
        msg = acc.withdraw(amount)
        if msg.lower().startswith("insufficient"):
            raise ValueError(msg)
        return msg

    def transfer(self, sender, recipient_name, amount):
        self.validate_name(recipient_name)

        if recipient_name == sender.name:
            raise ValueError("You cannot transfer money to yourself.")

        recipient = self.accounts.get(recipient_name)
        if not recipient:
            raise ValueError(f"Account '{recipient_name}' not found.")

        self.validate_amount(amount)

        withdraw_msg = sender.withdraw(amount)
        if withdraw_msg.lower().startswith("insufficient"):
            raise ValueError(withdraw_msg)

        recipient.deposit(amount)
        return f"Transferred ${amount} to {recipient_name}."

    def delete_account(self, acc, confirmation_text):
        if acc.balance > 0:
            raise ValueError(
                "You cannot delete an account with a remaining balance.")

        required = f"DELETE {acc.name.upper()}"
        if confirmation_text.strip() != required:
            raise ValueError(
                "Deletion cancelled. Confirmation text did not match.")

        self.accounts.pop(acc.name, None)
        bank.num_bank_acc -= 1
