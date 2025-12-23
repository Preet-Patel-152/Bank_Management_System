# bank_project/bank_app/migrate_json_to_db.py

from bank_project.bank_app.services import storage as json_storage
from bank_project.bank_app.services import db_storage


def migrate():
    """
    One-time migration:
    - Load accounts from JSON (accounts.json)
    - Upsert into SQLite (bank.db)
    - Also migrate last 5 history lines into transactions table (optional)
    """

    # Load from JSON
    accounts = json_storage.load_data()

    if not accounts:
        print("No accounts found in JSON. Nothing to migrate.")
        return

    # Ensure DB is ready
    db_storage.init_db()

    migrated_count = 0

    for name, acc in accounts.items():
        # Upsert account into DB (safe to run multiple times)
        db_storage.upsert_account(acc)
        migrated_count += 1

        # OPTIONAL: migrate history strings into DB transactions table
        # (not perfect parsing, but keeps a record)
        for entry in acc.history[-5:]:
            db_storage.log_transaction(
                account_name=name,
                tx_type="MIGRATED_HISTORY",
                amount=None,
                note=str(entry)
            )

    print(
        f"Migration complete ✅  Migrated/updated {migrated_count} accounts into SQLite.")


if __name__ == "__main__":
    migrate()
