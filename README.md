# Secure Bank Management System (CLI)

A robust, object-oriented banking application built in Python that simulates real-world account management. This project demonstrates clean architecture, defensive programming, layered design, and persistent state handling using both a relational database and JSON snapshots within a command-line interface.

---

## Features

- **User Authentication**  
  Secure login system requiring valid account holder credentials.

- **Defensive Programming**  
  Extensive input validation using `try-except` blocks and guard clauses to prevent crashes from invalid data types, empty input, or malformed commands.

- **Financial Integrity Controls**  
  Business rules enforce:
  - No overdrafts
  - No negative deposits or withdrawals
  - No unauthorized or self-transfers

- **Transaction Audit Trail**  
  All financial and security-related actions (deposits, withdrawals, transfers, password changes, deletions) are logged and persisted.

- **Layered Architecture (Service Pattern)**  
  - **UI Layer:** Command-line interface (input/output & navigation)  
  - **Service Layer:** Business logic, validation, and rules  
  - **Persistence Layer:** SQLite database with mirrored JSON snapshots  

- **Dual Persistence Strategy**  
  - **SQLite** acts as the primary source of truth  
  - **JSON** is automatically mirrored as a human-readable backup/export

- **Automated Testing**  
  Unit tests written with `pytest` validate core banking logic and service-layer behavior.

---

## Technical Overview

- **Language:** Python 3.10+
- **Paradigm:** Object-Oriented Programming (OOP)
- **Architecture:** Layered / Service-based design
- **Concepts:**  
  - Defensive Programming  
  - State Management  
  - Separation of Concerns  
  - Persistence & Data Integrity  
- **Control Flow:** Python `match-case` for clean, readable command routing
- **Storage:**  
  - SQLite (`bank.db`) — primary persistence  
  - JSON (`accounts.json`) — mirrored snapshot
- **Testing:** pytest

---

## How to Run

### Prerequisites
- Python 3.10 or higher
- `pytest` (optional, for running tests)

### Run the Application

From the project root directory:

```bash
python -m bank_project.bank_app.main
```

### Run the Application
```
python -m pytest
```

## Project structure

```
Bank_Management_System/
│
├── bank_project/
│   ├── account.py                  # Bank account domain model
│   │
│   ├── bank_app/
│   │   ├── main.py                 # CLI interface & application flow
│   │   ├── migrate_json_to_db.py   # One-time JSON → SQLite migration
│   │   │
│   │   ├── services/
│   │   │   ├── bank_service.py     # Business logic layer
│   │   │   ├── storage.py          # JSON persistence
│   │   │   ├── db_storage.py       # SQLite persistence
│   │   │   ├── dual_storage.py     # Mirrored DB + JSON backend
│   │   │   └── __init__.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── data/
│   │   ├── bank.db                 # SQLite database (gitignored)
│   │   ├── accounts.json       # JSON snapshot backup
│   │
│   └── __init__.py
│
├── tests/
│   ├── test_bank_account.py        # Unit tests for account model
│   ├── test_bank_service.py        # Unit tests for service layer
│   └── __init__.py
│
├── requirements.txt
├── .gitignore
└── README.md

```
---

## Future Enhancements

- Password hashing using industry-standard algorithms (bcrypt / argon2)
- Role-based admin accounts for system-wide monitoring and control
- Database indexing and constraints for improved performance and integrity
- REST API implementation using Flask or FastAPI
- CI pipeline for automated testing and quality checks

---

## Why This Project Matters

This project focuses on real backend engineering fundamentals:

- Designing clean service boundaries using a layered architecture
- Maintaining consistent state across multiple persistence layers (SQLite + JSON)
- Safely handling untrusted user input through defensive programming
- Writing testable, maintainable, and extensible Python code
- Applying production-style architecture and persistence patterns

It serves as a strong portfolio example for **backend**, **software engineering**, or **Python-focused** roles.

