import sqlite3
from datetime import date

# Add a new expense to the database
def add_expense(connect):
    while True:
        title = input("Enter expense title: ").strip()
        
        if title:
            break
        
        print("Title can't be empty.")
    
    while True:
        try:
            amount = float(input("Enter amount: "))
            
            if amount < 0:
                print("Amount can't be negative.")
                continue
            
            break
        except ValueError:
            print("Please enter a Valid number!")
            
    while True:
        category = input("Enter category: ").strip().capitalize()

        if category:
            break

        print("Category can't be empty.")
        
    today = str(date.today())

    cursor = connect.cursor()

    cursor.execute("""
        INSERT INTO expenses (title, amount, category, date)
        VALUES (?, ?, ?, ?)
    """, (title, amount, category, today))

    connect.commit()

    print("Expense added!")
    
# Show all saved expenses
def show_expenses(connect):
    cursor = connect.cursor()
    
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    
    if not expenses:
        print("No expenses yet")
    else:
        number = 1
        for i in expenses:
            print(number, "| ID:", i[0], "|", " | ".join(map(str, i[1:])))
            number += 1

# Delete an expense by ID
def delete_expense(connect):
    while True:
        try:
            expense_id = int(input("Enter expense ID: "))
            break
        except ValueError:
            print("Please enter a Valid ID!")
    
    cursor = connect.cursor()
    
    cursor.execute("DELETE FROM expenses WHERE id = ?", 
                   (expense_id,))
    
    if cursor.rowcount == 1:
        print("Expense deleted!")
    else:
        print("Expense not found!")
        
    connect.commit()

# Count total per category
def total_per_category(connect):
    cursor = connect.cursor()
    
    cursor.execute("""SELECT category, SUM(amount)
                FROM expenses
                GROUP BY category""")
    
    totals = cursor.fetchall()
    
    if not totals:
        print("No expenses yet.")
    else:
        for i in totals:
            print(" - ".join(map(str, i)))

# Count total for one category
def total_for_one_category(connect):
    category = input("Enter the category name: ").strip()
    
    cursor = connect.cursor()
    
    category = category.upper()
    cursor.execute("""SELECT category, SUM(amount)
                   FROM expenses
                   WHERE UPPER(category) = ?
                   GROUP BY category""", (category,))
    
    totals = cursor.fetchall()
    
    if not totals:
        print("No expenses yet.")
    else:
        for i in totals:
            print(" - ".join(map(str, i)))
        
# Update expense by ID
def update_expense(connect):
    while True:
            try:
                expense_id = int(input("Enter expense ID: "))
                break
            except ValueError:
                print("Please enter a Valid ID!")
    while True:
        try:
            new_amount = float(input("Enter the new amount: "))
            
            if new_amount < 0:
                print("Amount can't be negative.")
                continue
            
            break
        except ValueError:
            print("Please enter a Valid number!")
    
    cursor = connect.cursor()
    
    cursor.execute("""UPDATE expenses
                SET amount = ?
                WHERE id = ?;
                """, (new_amount, expense_id))
    
    if cursor.rowcount > 0:
        print("Expense is updated!")
    else:
        print("Expense not found!")
        
    connect.commit()


# Program menu
def menu(connect):
    while True:
        print("""\n ===== EXPENSE TRACKER =====
    1. Add expense
    2. Show all expenses
    3. Delete expense
    4. Update expense
    5. Total per category
    6. Total for one category
    7. Exit
                """)
        choose = input("Choose an option NUMBER: ")
        if choose == "1":
            add_expense(connect)
        elif choose == "2":
            show_expenses(connect)
        elif choose == "3":
            delete_expense(connect)
        elif choose == "4":
            update_expense(connect)
        elif choose == "5":
            total_per_category(connect)
        elif choose == "6":
            total_for_one_category(connect)
        elif choose == "7":
            break
        else:
            print("Wrong answer!")
            
def main():
    connect = sqlite3.connect("expenses.db")

    cursor = connect.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        amount REAL,
        category TEXT,
        date TEXT
    )
    """)

    connect.commit()

    menu(connect)

    connect.close()
    
    
if __name__ == "__main__":
    main()