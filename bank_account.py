from account import bank

accounts = {}
accounts["Alice"] = bank("Alice", "password123", 1000)


is_running = True

while is_running:

    action = input("would you like to create a new account or access existing account?\n"
                   " type new for new account, exi for existing account or done to exit out the program: ").strip().lower()

    if action not in ["new", "exi", "done"]:
        print("Invalid action. Please try again.")
        continue

    if action == "done":
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
                    "deposit\nwithdraw\ncheck balance\nchange password\ntransfer\ncheck history\n exit")

                user_action = input("Enter action: ").strip().lower()

                if user_action not in ["deposit", "withdraw", "check balance", "change password", "transfer", "developer", "exit", "check history"]:
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

                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                            continue

                    case "check balance":
                        print(bank_acc.check_balance())

                    case "change password":
                        new_password = input("Enter new password: ").strip()
                        print(bank_acc.change_acccout_password(new_password))

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
                            print(
                                f"Transferred ${amount} to {recipient_name}.")

                        except ValueError:
                            print("Invalid input. Please enter a numeric amount.")

                    case "developer":
                        print("Developer mode activated.")
                        print('        _   ,_,   _')
                        print('       / `\'=) (=\'` \\')
                        print('      /.-.-.\\ /.-.-.\\ ')
                        print('      `      "      `')

                        while True:

                            dev_action = input(
                                "what would you like to do check number of accounts or quit? ").strip().lower()

                            match dev_action:
                                case "check number of accounts":
                                    print(
                                        f"Total bank accounts: {bank.num_bank_acc}")
                                case "quit":
                                    print("Exiting developer mode.")
                                    break
                                case _:
                                    print(
                                        "Invalid developer action. Please try again.")

                    case "exit":
                        print("Exiting account management.")
                        break

                    case _:
                        print("Invalid action. Please try again.")
        else:
            print("Access denied. Incorrect name or password.")
            continue


# add some comments
