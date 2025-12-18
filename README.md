# Secure Bank Management System (CLI)

A robust, object-oriented banking application built with Python. This project demonstrates advanced logic handling, defensive programming, and secure data management within a command-line interface.

## Key Features

- **User Authentication:** Secure login system requiring matching account holder names and passwords.
- **Defensive Programming:** Comprehensive input validation using `try-except` blocks and logical guard clauses to prevent crashes from invalid data types or empty strings.
- **Financial Integrity:** Logic-driven transaction handling that prevents overdrafts, negative deposits, and unauthorized self-transfers.
- **Automated Audit Trail:** A built-in transaction history system that records every financial movement and security update (password changes) per account.
- **Object-Oriented Architecture:** Modular design with a dedicated `bank` class to handle state management and business logic independently from the user interface.

## Technical Overview

- **Language:** Python 3.10+
- **Concepts:** Object-Oriented Programming (OOP), Data Sanitization, Error Handling, State Management.
- **Modern Syntax:** Utilizes Python's `match-case` statements for clean, readable action routing.

## Project Structure

- `main.py`: The entry point of the application. Handles the UI loop, user input, and navigation between account states.
- `account.py`: Contains the `bank` class definition, managing the internal logic for balances, history, and security.

## Future Roadmaps
- [ ] **Data Persistence:** Integration with JSON to allow permanent storage of user accounts.
- [ ] **Encryption:** Implementing password hashing for enhanced security.
- [ ] **Admin Dashboard:** Expanded developer tools for system-wide monitoring.
