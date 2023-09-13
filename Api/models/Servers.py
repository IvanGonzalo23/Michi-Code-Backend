from ..controllers.database import DatabaseConnection  

class Server:
    def __init__(self, nombre, created_by):
        self.nombre = nombre
        self.created_by = created_by

    def create_server(self):
        try:
            
            query = "INSERT INTO servidores (nombre, created_by) VALUES (%s, %s)"
            params = (self.nombre, self.created_by)
            
        
            cursor = DatabaseConnection.execute_query(query, params)
            
           
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
       
            print(f"Error al crear el servidor: {str(e)}")
            return False
