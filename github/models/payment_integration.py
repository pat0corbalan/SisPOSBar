import sqlite3

class PaymentIntegration:
    def __init__(self):
        pass

    def get_payment_methods(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM PaymentMethods')
        payment_methods = cursor.fetchall()
        conn.close()
        return payment_methods

    def add_payment_method(self, name, interes):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO PaymentMethods (name, interes) VALUES (?,?)', (name,interes))
        conn.commit()
        conn.close()

    def delete_payment_method(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM PaymentMethods WHERE id = ?')
        conn.commit()
        conn.close()

    def get_interes(self, payment_method_id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT interes FROM PaymentMethods WHERE id = ?', (payment_method_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return row[0]
        else:
            return 0.0  # Si no se encuentra la tasa de interés, devolvemos 0.0 como valor predeterminado