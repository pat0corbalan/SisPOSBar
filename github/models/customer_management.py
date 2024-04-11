import sqlite3

class CustomerManagement:
    def __init__(self):
        pass

    def get_customers(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Customers')
        customers = cursor.fetchall()
        conn.close()
        return customers

    def add_customer(self, name, email, phone):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Customers (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
        conn.commit()
        conn.close()

    def update_customer(self, customer_id, name, email, phone):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE Customers SET name = ?, email = ?, phone = ? WHERE id = ?', (name, email, phone, customer_id))
        conn.commit()
        conn.close()

    def delete_customer(self, customer_id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Customers WHERE id = ?', (customer_id,))
        conn.commit()
        conn.close()
