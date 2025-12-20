# bank_project/bank_app/services/storage.py

import json
from pathlib import Path
from bank_project.account import bank

# Always save/load to ONE location: bank_project/data/accounts.json
DATA_FILE = (Path(__file__).resolve().parents[2] / "data" / "accounts.json")


def save_data(accounts):
    """Converts Bank objects into JSON-friendly dictionaries and saves to disk."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

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
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable_data, f, indent=4)


def load_data():
    """Loads JSON data and reconstructs Bank objects into the accounts dictionary."""
    if not DATA_FILE.exists():
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
