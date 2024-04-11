import sqlite3
from datetime import datetime

class CashRegisterManagement:
    def __init__(self):
        pass

    def add_to_cash_register(self, amount):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO CashRegister (amount, date) VALUES (?, ?)',
                    (amount, datetime.now()))
        conn.commit()
        conn.close()

    def get_cash_register_entries(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CashRegister')
        entries = cursor.fetchall()
        conn.close()
        return entries
