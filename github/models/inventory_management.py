import sqlite3

class InventoryManagement:
    def __init__(self):
        pass

    def get_inventory(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.id, p.name, i.quantity, i.type, i.date
            FROM Inventory i
            JOIN Products p ON i.product_id = p.id
        ''')
        inventory = cursor.fetchall()
        conn.close()
        return inventory


    def adjust_inventory(self, product_id, adjustment):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE Inventory SET quantity = quantity + ? WHERE product_id = ?', (adjustment, product_id))
        conn.commit()
        conn.close()
