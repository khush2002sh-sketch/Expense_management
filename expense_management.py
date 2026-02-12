import sqlite3
from getpass import getpass
from datetime import datetime

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            category TEXT,
            date TEXT,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()

def register():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    username = input("Enter username: ")
    password = getpass("Enter password: ")

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("✅ Registered successfully!\\n")
    except:
        print("❌ Username already exists!\\n")

    conn.close()

def login():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    username = input("Enter username: ")
    password = getpass("Enter password: ")

    cur.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()

    conn.close()

    if user:
        print("✅ Login successful!\\n")
        return user[0]
    else:
        print("❌ Invalid credentials!\\n")
        return None

def add_expense(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        amount = float(input("Amount: ₹"))
        category = input("Category: ")
        description = input("Description: ")
        date = datetime.now().strftime("%Y-%m-%d")

        cur.execute("INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                    (user_id, amount, category, date, description))
        conn.commit()

        print("✅ Expense added!\\n")
    except:
        print("❌ Invalid input!\\n")

    conn.close()

def view_expenses(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT amount, category, date, description FROM expenses WHERE user_id=?", (user_id,))
    rows = cur.fetchall()

    print("\\n📊 Your Expenses:")
    total = 0

    for row in rows:
        print(f"₹{row[0]} | {row[1]} | {row[2]} | {row[3]}")
        total += row[0]

    print(f"\\nTotal Spending: ₹{total}\\n")

    conn.close()

def user_menu(user_id):
    while True:
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Logout")

        choice = input("Choose: ")

        if choice == "1":
            add_expense(user_id)
        elif choice == "2":
            view_expenses(user_id)
        elif choice == "3":
            break
        else:
            print("❌ Invalid choice\\n")

def main():
    init_db()

    while True:
        print("====== Expense Manager ======")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == "1":
            register()
        elif choice == "2":
            user_id = login()
            if user_id:
                user_menu(user_id)
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice\\n")

if __name__ == "__main__":
    main()
