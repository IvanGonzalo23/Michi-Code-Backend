from flask import request, jsonify, session
from ..models.Servers import Server  


class ServerController:
    @staticmethod
    def create_server():
        try:
            # Verifica si el usuario ha iniciado sesión
            if "user_id" not in session:
                return jsonify({"error": "Acceso no autorizado"}), 401  # 401 Unauthorized

            # Obtiene los datos del formulario, incluida la imagen del servidor
            data = request.form
            nombre_servidor = data.get("nombre_servidor")
            imagen_servidor = request.files["imagen_servidor"]

            # Obtiene el ID del usuario que ha iniciado sesión
            usuario_id = session["user_id"]

            # Crea una instancia de la clase Server y llama al método para crear el servidor
            new_server = Server(nombre=nombre_servidor, created_by=usuario_id)
            if new_server.create_server(imagen_servidor):
                return jsonify({"success": True, "message": "Servidor creado exitosamente"}), 201  # 201 Created
            else:
                return jsonify({"error": "Error al crear el servidor"}), 500  # 500 Internal Server Error

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # 500 Internal Server Error
