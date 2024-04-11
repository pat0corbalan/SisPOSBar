import sqlite3
import datetime

class Dashboard:
    def __init__(self):
        self.total_sales = 0
        self.total_inventory = 0

    def get_total_sales(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(total) FROM Sales')
        result = cursor.fetchone()
        if result and result[0]:
            self.total_sales = result[0]
        conn.close()

    def get_total_inventory(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(quantity) FROM Products')
        result = cursor.fetchone()
        if result and result[0]:
            self.total_inventory = result[0]
        conn.close()

    def get_inventory_by_category(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT category, SUM(quantity) FROM Products GROUP BY category ORDER BY category')
        inventory_by_category = cursor.fetchall()
        conn.close()
        print(f"Datos de inventario por categoría: {inventory_by_category}")
        return inventory_by_category


    def get_top_products(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.name, SUM(sd.quantity) AS total_quantity, SUM(sd.quantity * p.price) AS total_revenue
            FROM SalesDetails sd
            JOIN Products p ON sd.product_id = p.id
            GROUP BY p.name
            UNION
            SELECT f.name, SUM(sd.quantity) AS total_quantity, SUM(sd.quantity * f.price) AS total_revenue
            FROM SalesDetails sd
            JOIN Foods f ON sd.food_id = f.id
            GROUP BY f.name
            ORDER BY total_quantity DESC LIMIT 5
        ''')
        top_products = cursor.fetchall()
        conn.close()
        return top_products


    def get_inventory(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, quantity FROM Products')
        inventory = cursor.fetchall()
        conn.close()
        return inventory

    def get_financial_reports(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()

        try:
            # Calcular el total de ventas
            cursor.execute('SELECT SUM(total) FROM Sales')
            total_sales = cursor.fetchone()[0] or 0

            # Calcular el total de costos
            cursor.execute('''
                SELECT SUM(Inventory.quantity * Products.cost) AS total_cost
                FROM Inventory
                JOIN Products ON Inventory.product_id = Products.id
                WHERE Inventory.type IN ('Agregado', 'Actualizado')
            ''')
            total_costs = cursor.fetchone()[0] or 0

            # Calcular el total de gastos
            cursor.execute('SELECT SUM(amount) FROM Expenses')
            total_expenses = cursor.fetchone()[0] or 0

            # Calcular el egreso
            total_egress = total_expenses + total_costs

            # Calcular el beneficio neto
            total_profit = total_sales - total_egress

            return total_sales, total_costs, total_expenses, total_egress, total_profit

        except Exception as e:
            print(f"Error calculating financial reports: {e}")
            return None, None, None, None, None

        finally:
            conn.close()

    def get_sales_by_period(self, period):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()

        try:
            if period == 'day':
                cursor.execute('SELECT strftime("%Y-%m-%d", date) AS day, SUM(total) FROM Sales GROUP BY day ORDER BY day')
            elif period == 'week':
                cursor.execute('SELECT strftime("%Y-%W", date) AS week, SUM(total) FROM Sales GROUP BY week ORDER BY week')
            elif period == 'month':
                cursor.execute('SELECT strftime("%Y-%m", date) AS month, SUM(total) FROM Sales GROUP BY month ORDER BY month')
            elif period == 'year':
                cursor.execute('SELECT strftime("%Y", date) AS year, SUM(total) FROM Sales GROUP BY year ORDER BY year')

            sales_by_period = cursor.fetchall()
            return sales_by_period

        except Exception as e:
            print(f"Error getting sales by period: {e}")
            return None

        finally:
            conn.close()


    def get_daily_summary(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()

        try:
            # Obtener el total de costos por fecha
            cursor.execute('''
                SELECT Inventory.date, SUM(Inventory.cost * Inventory.quantity) AS total_cost
                FROM Inventory
                JOIN Products ON Inventory.product_id = Products.id
                WHERE Inventory.type = 'Agregado'
                GROUP BY Inventory.date
            ''')
            costs_by_date = cursor.fetchall()

            # Calcular el ingreso total
            cursor.execute('''
                SELECT Sales.date, SUM(Sales.total) AS total_income
                FROM Sales
                GROUP BY Sales.date
            ''')
            incomes_by_date = cursor.fetchall()

            # Calcular los gastos generales
            general_expenses = 5000  # Este valor es solo un ejemplo, debes obtenerlo de tu base de datos o cálculos reales

            # Combinar los resultados en un diccionario para facilitar la visualización
            summary = {}
            for date, total_cost in costs_by_date:
                total_income = 0
                for income_date, income_amount in incomes_by_date:
                    if income_date == date:
                        total_income = income_amount
                        break

                profit = total_income - total_cost
                summary[date] = {
                    'total_cost': total_cost,
                    'total_income': total_income,
                    'profit': profit,
                    'general_expenses': general_expenses
                }

            return summary

        except Exception as e:
            print(f"Error calculating daily summary: {e}")
            return {}

        finally:
            conn.close()

