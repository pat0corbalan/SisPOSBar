import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM Users WHERE id = ?', (user_id,))
        user_id = cursor.fetchone()
        conn.close()
        if not user_id:
            return None
        return User(user_id[0])

    def verificar_expiracion(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT registration_date FROM Users WHERE id = ?', (self.id,))
        subscription_date_str = cursor.fetchone()[0]
        conn.close()

        print("Fecha de suscripción (string):", subscription_date_str)

        # Eliminar caracteres adicionales al final si es necesario
        subscription_date_str = subscription_date_str.split('.')[0]

        subscription_date = datetime.strptime(subscription_date_str, '%Y-%m-%d %H:%M:%S')
        current_date = datetime.now()
        expiration_date = subscription_date + relativedelta(months=1)  # Sumar un mes a la fecha de suscripción

        # Depuradores
        print("Fecha de suscripción (datetime):", subscription_date)
        print("Fecha de expiración:", expiration_date)
        print("Fecha actual:", current_date)

        if current_date > expiration_date:
            # La suscripción ha expirado
            return False
        else:
            # La suscripción sigue activa
            return True

class LoginManagement:
    def __init__(self):
        pass
    
    def get_login(self, username):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM Users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def register_user(self, username, password_hash):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Users (username, password_hash, registration_date) VALUES (?, ?, ?)',
                    (username, password_hash, datetime.now()))
        conn.commit()
        conn.close()