# bank_project/bank_app/services/dual_storage.py

from bank_project.bank_app.services import storage as json_storage
from bank_project.bank_app.services import db_storage


class DualStorage:
    """
    Mirror storage:
    - LOAD from SQLite (source of truth)
    - WRITE to both SQLite + JSON
    """

    def load_accounts(self):
        # Source of truth
        accounts = db_storage.load_accounts()

        # Keep JSON in sync on startup too
        json_storage.save_data(accounts)
        return accounts

    def save_all(self, accounts):
        # DB: upsert every account
        for acc in accounts.values():
            db_storage.upsert_account(acc)

        # JSON: write full snapshot
        json_storage.save_data(accounts)

    def sync_account(self, acc):
        # Write this account to DB
        db_storage.upsert_account(acc)

        # JSON is a snapshot file, so easiest is save all accounts elsewhere.
        # But to keep this function simple, we just update snapshot later via save_all().
        # If you want "always up to date JSON", call save_all(accounts) instead of sync_account.
        # We'll keep it simple and let main call save_all after each change if you want true mirroring.
        pass

    def delete_account(self, name: str, accounts):
        # Delete in DB
        db_storage.delete_account(name)

        # Update JSON snapshot
        json_storage.save_data(accounts)

    def log_tx(self, account_name: str, tx_type: str, amount=None, note=None):
        # JSON doesn’t store transaction table; it stores history inside the account object.
        # DB gets the full transaction log:
        db_storage.log_transaction(account_name, tx_type, amount, note)
