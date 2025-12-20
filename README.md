# Secure Bank Management System (CLI)

A robust, object-oriented banking application built in Python that simulates real-world account management. This project demonstrates clean architecture, defensive programming, and persistent state handling within a command-line interface.

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
  - No unauthorized transactions

- **Transaction Audit Trail**  
  Every deposit, withdrawal, and security update (password change) is recorded per account.

- **Object-Oriented Architecture**  
  Core banking logic is encapsulated in a dedicated account class, fully separated from the user interface layer.

- **Persistent Storage**  
  Account data is serialized to JSON, allowing application state to persist across program executions.

---

## Technical Overview

- **Language:** Python 3.10+
- **Paradigm:** Object-Oriented Programming (OOP)
- **Concepts:**  
  - Defensive Programming  
  - State Management  
  - Input Sanitization  
  - Separation of Concerns  
- **Control Flow:** Python `match-case` for clean, readable command routing
- **Storage:** JSON

---
---

## How to Run

### Prerequisites
- Python 3.10 or higher

### Run the Application

From the project root directory, run:

```bash
python -m bank_project.bank_app.main 
```

## Project Structure

```text
Bank_Management_System/
│
├── bank_project/
│   ├── account.py          # Bank account class & core business logic
│   ├── bank_app/
│   │   ├── main.py         # CLI interface & application loop
│   │   └── __init__.py
│   ├── data/
│   │   └── accounts.json   # Persistent account storage
│   └── __init__.py
│
├── .gitignore
├── README.md
```



