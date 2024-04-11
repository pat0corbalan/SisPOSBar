import sqlite3

class EmployeeManagement:
    def __init__(self):
        pass

    def get_employees(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Employees')
        employees = cursor.fetchall()
        conn.close()
        return employees

    def add_employee(self, name, position, email, phone):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Employees (name, position, email, phone) VALUES (?, ?, ?, ?)', (name, position, email, phone))
        conn.commit()
        conn.close()

    def update_employee(self, employee_id, name, position, email, phone):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE Employees SET name=?, position=?, email=?, phone=? WHERE id=?', (name, position, email, phone, employee_id))
        conn.commit()
        conn.close()

    def delete_employee(self, employee_id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Employees WHERE id=?', (employee_id,))
        conn.commit()
        conn.close()
