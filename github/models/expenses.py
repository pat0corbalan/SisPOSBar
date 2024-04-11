import sqlite3

class ExpensesManagement:
    def __init__(self):
        pass
    
    def add_expense(self, description, amount, date, category):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Expenses (description, amount, date, category) VALUES (?, ?, ?, ?)', (description, amount, date, category))
        conn.commit()
        conn.close()

    def get_all_expenses(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Expenses')
        expenses = cursor.fetchall()
        conn.close()
        return expenses