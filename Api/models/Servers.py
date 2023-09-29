import os
from ..controllers.database import DatabaseConnection  # Importa tu clase DatabaseConnection
from werkzeug.utils import secure_filename

class Server:
    def __init__(self, nombre, created_by):
        self.nombre = nombre
        self.created_by = created_by

    def create_server(self,imagen_servidor):
        try:
            # Consulta SQL para insertar un nuevo servidor asociado al usuario
            query = "INSERT INTO servidores (nombre, created_by, imagen) VALUES (%s, %s, %s)"
            params = (self.nombre, self.created_by,imagen_servidor.filename)
            
            # Ejecuta la consulta utilizando DatabaseConnection
            cursor = DatabaseConnection.execute_query(query, params)
            
            # Comprueba si se insertó correctamente el servidor
            if cursor.rowcount > 0:
                servidor_id = cursor.lastrowid  # Obtiene el ID del servidor recién insertado

                ruta_imagen = os.path.abspath(os.path.join("Api", "static", "imagenes_servidores", secure_filename(imagen_servidor.filename)))
                imagen_servidor.save(ruta_imagen)

                query = "INSERT INTO usuarios_servidores (usuario_id, servidor_id) VALUES (%s, %s)"
                params = (self.created_by, servidor_id)
                cursor = DatabaseConnection.execute_query(query, params)
                return True
            else:
                return False
        except Exception as e:
            # Maneja cualquier error de la base de datos aquí
            print(f"Error al crear el servidor: {str(e)}")
            return False
