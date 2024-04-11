import sqlite3

class SalesHistory:
    def __init__(self):
        pass

    def get_sales_history(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Sales.id, Sales.date, Sales.total, Products.name
            FROM Sales
            JOIN SalesDetails ON Sales.id = SalesDetails.sale_id
            JOIN Products ON SalesDetails.product_id = Products.id
            ORDER BY Sales.date DESC
        ''')
        sales_history = cursor.fetchall()
        conn.close()
        return sales_history
