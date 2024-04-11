import sqlite3

class SettingsManagement:
    def __init__(self):
        pass
    
    def get_settings(self):
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Settings')
        settings = cursor.fetchone()
        conn.close()
        return settings

    def update_setting(self, company_name, address, phone_number):
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE Settings SET company_name = ?, address = ?, phone_number = ? WHERE id = 1', (company_name, address, phone_number))
            conn.commit()
            if cursor.rowcount > 1:
                print("Actualización exitosa")
            else:
                print("No se realizó ninguna actualización")
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            conn.close()
