from ..controllers.database import DatabaseConnection

class Channel:
    def __init__(self,nombre,servidor_id):
        self.nombre = nombre
        self.servidor_id = servidor_id

    def create_channel(self):
        try:
            query = """INSERT INTO canales (nombre, servidor_id) VALUES (%s, %s)"""
            params = self.nombre,self.servidor_id

            cursor = DatabaseConnection.execute_query(query,params)

            if cursor.rowcount > 0:
                canal_id = cursor.lastrowid
                return canal_id
            else:
                return None
        except Exception as e:
            print(f"Error al crear el canal {str(e)}")
            return None