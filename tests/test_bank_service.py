import pytest
from bank_project.bank_app.services.bank_service import BankService


def test_create_account_adds_to_accounts_dict():
    accounts = {}
    service = BankService(accounts)

    acc = service.create_account("Alice", "pw")

    assert "Alice" in service.accounts
    assert acc.name == "Alice"
    assert acc.balance == 0


def test_login_success():
    accounts = {}
    service = BankService(accounts)
    service.create_account("Alice", "pw")

    acc = service.login("Alice", "pw")

    assert acc.name == "Alice"


def test_login_wrong_password_raises():
    accounts = {}
    service = BankService(accounts)
    service.create_account("Alice", "pw")

    with pytest.raises(ValueError):
        service.login("Alice", "wrong")


def test_transfer_moves_money_between_accounts():
    accounts = {}
    service = BankService(accounts)

    sender = service.create_account("Alice", "pw")
    receiver = service.create_account("Bob", "pw")

    # Give sender money
    service.deposit(sender, 100)

    msg = service.transfer(sender, "Bob", 40)

    assert "Transferred" in msg
    assert sender.balance == 60
    assert receiver.balance == 40


def test_transfer_insufficient_funds_raises():
    accounts = {}
    service = BankService(accounts)

    sender = service.create_account("Alice", "pw")
    service.create_account("Bob", "pw")

    with pytest.raises(ValueError):
        service.transfer(sender, "Bob", 999)
