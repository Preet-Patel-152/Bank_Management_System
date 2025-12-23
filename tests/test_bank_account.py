from bank_project.account import bank


def test_deposit_increases_balance():
    acc = bank("Alice", "pw", 0)
    msg = acc.deposit(100)

    assert acc.balance == 100
    assert "Deposited" in msg


def test_withdraw_decreases_balance():
    acc = bank("Bob", "pw", 200)
    msg = acc.withdraw(50)

    assert acc.balance == 150
    assert "Withdrew" in msg


def test_withdraw_insufficient_funds_does_not_change_balance():
    acc = bank("Cara", "pw", 25)
    msg = acc.withdraw(100)

    assert acc.balance == 25
    assert msg == "Insufficient funds."


def test_change_password_updates_password_and_logs_history():
    acc = bank("Dave", "old_pw", 0)
    msg = acc.change_accout_password("new_pw")

    assert acc.password == "new_pw"
    assert "Password was updated." in acc.history[-1]
    assert "Password changed successfully" in msg


def test_deposit_negative_amount_does_not_change_balance():
    acc = bank("Eve", "pw", 50)
    msg = acc.deposit(-20)

    assert acc.balance == 50
    assert msg == "Deposit amount must be positive."


def test_withdraw_negative_amount_does_not_change_balance():
    acc = bank("Frank", "pw", 75)
    msg = acc.withdraw(-30)

    assert acc.balance == 75
    assert msg == "Withdrawal amount must be positive."
