import sqlite3
from datetime import datetime

class ProductManagement:
    def __init__(self):
        pass

    def get_products(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Products')
        products = cursor.fetchall()
        conn.close()
        return products
    
    def add_product(self, name, category, price, cost, quantity):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Products (name, category, price, cost, quantity) VALUES (?, ?, ?, ?, ?)', (name, category, price, cost,quantity))
        product_id = cursor.lastrowid
        conn.commit()
        cursor.execute('INSERT INTO Inventory (product_id, date, quantity, type) VALUES (?, ?, ?, "Agregado")',
                        (product_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), quantity))
        conn.commit()
        conn.close()

    def update_product(self, product_id, name, price, quantity):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        
        try:
            # Obtener el nombre del producto correspondiente al product_id
            cursor.execute('SELECT name FROM Products WHERE id=?', (product_id,))
            product_name = cursor.fetchone()[0]
            
            # Actualizar el producto en la tabla Products
            cursor.execute('UPDATE Products SET name=?, price=?, quantity=? WHERE id=?', (name, price, quantity, product_id))
            conn.commit()
            
            # Registrar el cambio en el inventario
            cursor.execute('INSERT INTO Inventory (product_name, date, quantity, type) VALUES (?, ?, ?, "Actualizado")',
                        (product_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), quantity))
            conn.commit()
            conn.close()
            print(f"Updated product: {product_name}, Price: {price}, Quantity: {quantity}")
        except Exception as e:
            print(f"Error updating product: {e}")
            conn.rollback()
        finally:
            conn.close()


    def delete_product(self, product_id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Products WHERE id=?', (product_id,))
        conn.commit()
        conn.close()

    def get_product_price(self, product_id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM Products WHERE id = ?", (product_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    
    #Aqui comienzan las comidas
    def get_foods(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Foods')
        foods = cursor.fetchall()
        conn.close()
        return foods
    
    def get_food_price(self, food_id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT price FROM Foods WHERE id = ?', (food_id,))
        price = cursor.fetchone()[0]
        conn.close()
        return price
    
    def add_food(self, name, price):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Foods (name, price) VALUES (?, ?)', (name, price))
        food_id = cursor.lastrowid * -1
        cursor.execute('UPDATE Foods SET id = ? WHERE id = ?', (food_id, cursor.lastrowid))
        conn.commit()
        conn.close()

    def update_food(self, food_id, name, price):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        
        try:
            # Obtener el nombre del producto correspondiente al food_id
            cursor.execute('SELECT name FROM Foods WHERE id=?', (food_id,))
            food_name = cursor.fetchone()[0]
            
            # Actualizar comida en la tabla Foods
            cursor.execute('UPDATE Foods SET name=?, price=?, WHERE id=?', (name, price, food_id))
            conn.commit()
        except Exception as e:
            print(f"Error updating food: {e}")
            conn.rollback()
        finally:
            conn.close()


    def delete_food(self, food_id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Foods WHERE id=?', (food_id,))
        conn.commit()
        conn.close()