class bank:

    # =============================
    # Class-level tracking
    # =============================
    # Shared across all bank accounts
    num_bank_acc = 0
    total_bank_balance = 0

    # =============================
    # Account Initialization
    # =============================
    def __init__(self, name, password, initial_balance=0):

        # Store account information
        self.name = name
        self.password = password
        self.balance = initial_balance
        bank.total_bank_balance += initial_balance

        # Track transaction history for this account
        self.history = []

        # Log account creation
        if initial_balance == 0:
            self.history.append(f"Account created with $0")

        # Update global bank totals
        bank.num_bank_acc += 1

    # =============================
    # Account Security
    # =============================

    def change_accout_password(self, new_password):

        # Update account password
        self.password = new_password

        # Record password change in history
        self.history.append("Security: Password was updated.")

        return f"Password changed successfully for {self.name}."

    # =============================
    # Deposits
    # =============================

    def deposit(self, amount):

        # Validate deposit amount
        if amount > 0:
            self.balance += amount
            bank.total_bank_balance += amount

            # Log successful deposit
            msg = f"Deposited: ${amount}. New balance: ${self.balance}."
            self.history.append(msg)
            return msg

        else:
            return "Deposit amount must be positive."

    # =============================
    # Withdrawals
    # =============================
    def withdraw(self, amount):

        # Validate withdrawal amount
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                bank.total_bank_balance -= amount

                # Log successful withdrawal
                msg = f"Withdrew: ${amount}. New balance: ${self.balance}."
                self.history.append(msg)
                return msg
            else:
                return "Insufficient funds."
        else:
            return "Withdrawal amount must be positive."

    # =============================
    # Account Info
    # =============================
    def check_balance(self):

        # Return formatted account balance
        return f"Current balance: ${self.balance}."

    # =============================
    # Transaction History
    # =============================
    def get_history(self):

        # Return recent transactions only
        if not self.history:
            return "No transactions yet."
        return "\n".join(self.history[-5:])  # Returns the last 5 transactions
