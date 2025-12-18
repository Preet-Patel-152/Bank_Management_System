class bank:
    num_bank_acc = 0

    def __init__(self, name, password, initial_balance=0):
        self.name = name
        self.password = password
        self.balance = initial_balance
        self.history = []
        self.history.append(f"Account created with ${initial_balance}")

        if initial_balance == 0:
            self.history.append(f"Account created with $0")

        bank.num_bank_acc += 1

    def change_acccout_password(self, new_password):
        self.password = new_password
        self.history.append("Security: Password was updated.")
        return f"Password changed successfully for {self.name}."

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            msg = f"Deposited: ${amount}. New balance: ${self.balance}."
            self.history.append(msg)
            return msg
        else:
            return "Deposit amount must be positive."

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                msg = f"Withdrew: ${amount}. New balance: ${self.balance}."
                self.history.append(msg)
                return msg
            else:
                return "Insufficient funds."
        else:
            return "Withdrawal amount must be positive."

    def check_balance(self):
        return f"Current balance: ${self.balance}."

    def get_history(self):
        if not self.history:
            return "No transactions yet."
        return "\n".join(self.history[-5:])  # Returns the last 5 transactions
