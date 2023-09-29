from ..controllers.database import DatabaseConnection

class Message:
    def __init__(self,contenido,usuario_id,servidor_id,canal_id):
        self.contenido = contenido
        self.usuario_id = usuario_id
        self.servidor_id = servidor_id
        self.canal_id = canal_id

    def create_message(self):
        try:
            query = """INSERT INTO mensajes (contenido, usuario_id, servidor_id, canal_id) VALUES (%s, %s, %s, %s)"""
            params = (self.contenido, self.usuario_id, self.servidor_id, self.canal_id)

            cursor = DatabaseConnection.execute_query(query,params)

            if cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al crear un mensaje: {str(e)}")
    
    @classmethod
    def edit_message(self, message_id, new_content):
        try:
            query = "UPDATE mensajes SET contenido = %s WHERE id = %s"
            params = (new_content, message_id)

            cursor = DatabaseConnection.execute_query(query, params)

            if cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al editar el mensaje: {str(e)}")
            return False

    @classmethod
    def delete_message(self, message_id):
        try:
            query = "DELETE FROM mensajes WHERE id = %s"
            params = (message_id,)

            cursor = DatabaseConnection.execute_query(query, params)

            if cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al eliminar el mensaje: {str(e)}")
            return False