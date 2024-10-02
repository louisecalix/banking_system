# Simple Banking System

This is a simple banking system built in **Python** using **Object-Oriented Programming (OOP)** principles. The system allows users to create and manage bank accounts (savings or checking) and stores account information in a **JSON** file. A **joint account** feature is also planned but is not fully implemented yet. The project uses **Tkinter** for the graphical user interface (GUI).

## Features

- **Create New Account**: Users can open a new bank account (savings or checking) through a GUI.
- **View Account Details**: After creating an account, users can view their account details.
- **JSON Storage**: Account details are stored in a JSON file for persistence.
- **Tkinter GUI**: A user-friendly interface for account creation and management.
- **OOP Design**: Implements Python classes and inheritance for a clean, modular structure.
- **Joint Account**: A feature for creating joint accounts is in progress and will be available in future updates.

## Project Structure

- **`accounts.py`**: Contains the core classes for the banking system, including `Account`, `SavingsAccount`, `CheckingAccount`, and their methods.
- **`gui.py`**: Handles the Tkinter GUI for interacting with the banking system.
- **`info.json`**: The file where account data is stored.
- **`controller.py`**: The file where the bank logic is being developed.
- **`main.py`**: The file where you can run the whole program.

## Technologies Used

- **Python 3.8**
- **Tkinter**: For the user interface.
- **JSON**: For storing account information.
- **Object-Oriented Programming (OOP)**: For structuring the banking system.

## How to Run Locally

To run this project on your local machine:

1. **Clone the repository**:
   Open your terminal and run the following command:
   ```bash
   git clone https://github.com/yourusername/banking-system.git

2. **Navigate to the project directory**:
   After cloning, navigate into the project directory:
   ```bash
   cd banking-system

3. **Install Dependencies**:
   Ensure you have Python and Tkinter installed on your system.

4. **Run the application**:
   Execute the Python script to start the Tkinter GUI. In your terminal or command prompt, run:
   ```bash
   python main.py
