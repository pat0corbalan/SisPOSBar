import sqlite3
from datetime import datetime
from models.payment_integration import PaymentIntegration

class SaleProcess:
    def __init__(self, db_path='db/database.db'):
        self.db_path = db_path

    def make_sale(self, selected_items, quantities, total, payment_method_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Obtener la tasa de interés del método de pago
            payment_integration = PaymentIntegration()
            interest_rate = payment_integration.get_interes(payment_method_id)

            # Calcular el total con el interés aplicado
            total_with_interest = total * (1 + interest_rate / 100)

            # Insertar la venta en la tabla Sales
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO Sales (date, total) VALUES (?, ?)', (date, total_with_interest))
            sale_id = cursor.lastrowid

            # Insertar los detalles de la venta en la tabla SalesDetails
            for i, item_id in enumerate(selected_items):
                quantity = quantities[i]
                if int(item_id) > 0:
                    cursor.execute('INSERT INTO SalesDetails (sale_id, product_id, quantity) VALUES (?, ?, ?)', (sale_id, item_id, quantity))
                else:
                    cursor.execute('INSERT INTO SalesDetails (sale_id, food_id, quantity) VALUES (?, ?, ?)', (sale_id, item_id, quantity))

            # Insertar el método de pago en la tabla SalesPaymentMethods
            cursor.execute('INSERT INTO SalesPaymentMethods (sale_id, payment_method_id, amount) VALUES (?, ?, ?)', (sale_id, payment_method_id, total_with_interest))

            conn.commit()
            return sale_id
        except sqlite3.Error as e:
            print("Error en la transacción SQL:", e)
            return None
        finally:
            if conn:
                conn.close()