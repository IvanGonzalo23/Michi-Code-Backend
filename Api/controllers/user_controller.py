from flask import request, jsonify,session,render_template
from ..models.Users import User  # Asegúrate de importar la clase User desde el modelo adecuado
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
class UserController:
    @staticmethod
    def create_user():
        try:
            if request.is_json:
                data = request.get_json()
                new_user = User.create_user(
                    data["username"],
                    data["name"],
                    data["lastname"],
                    data["password"],
                    data["fecha"],
                    data["email"]
                )

                user_data = new_user.serialize()
                
                response = {
                    "message": "Usuario creado exitosamente",
                    "user": user_data  # Aquí se incluyen los datos del usuario serializados
                }
                return jsonify(response), 201  # 201 Created
            else:
                return jsonify({"error": "Solicitud debe ser de tipo application/json"}), 415
        except Exception as e:
            error_response = {
                "message": "Error al crear el usuario",
                "error": str(e)
            }
            return jsonify(error_response), 500  # 500 Internal Server Error
        
    @staticmethod
    def login():
        try:
            data = request.json
            email_username = data.get("email_username")
            contrasenia = data.get("contrasenia")

            # Verifica las credenciales
            user = User.verificar_credenciales(email_username, contrasenia)

            if user:
                print("credenciales validas")
                # Credenciales válidas, el usuario ha iniciado sesión con éxito
                session["user_id"] = user.id_user  # Almacena el ID del usuario en la sesión
                response = {
                    "message": "Inicio de sesión exitoso",
                    "user": user.serialize()
                }
                return jsonify(response), 200  # 200 OK
            else:
                # Credenciales incorrectas, devuelve un mensaje de error
                error_response = {
                    "message": "Credenciales incorrectas"
                }
                return jsonify(error_response), 401  # 401 Unauthorized

        except Exception as e:
            error_response = {
                "message": "Error en el inicio de sesión",
                "error": str(e)
            }
            return jsonify(error_response), 500
    
    @staticmethod
    def edit_profile(user_id):
        try:
            if "user_id" not in session or session["user_id"] != user_id:
                return jsonify({"message": "Acceso no autorizado"}), 401  # 401 Unauthorized

            data = request.json
            username = data.get("username")
            password = data.get("password")

            # Busca al usuario por su ID
            user = User.get_user_by_id(user_id)

            if not user:
                return jsonify({"message": "Usuario no encontrado"}), 404  # 404 Not Found

            # Actualiza los campos de perfil (por ejemplo, nombre de usuario y contraseña)
            if username:
                user.username = username
            if password:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                user.password = hashed_password

            # Guarda los cambios en la base de datos
            user.update_user()

            response = {
                "message": "Perfil de usuario actualizado exitosamente",
                "user": user.serialize()
            }
            return jsonify(response), 200  # 200 OK

        except Exception as e:
            error_response = {
                "message": "Error al actualizar el perfil de usuario",
                "error": str(e)
            }
            return jsonify(error_response), 500  # 500 Internal Server Error
        
        
    @staticmethod
    def delete_user():
        try:
            user_id = session.get("user_id") 

            # Llama a la función delete_user para eliminar al usuario
            if User.delete_user(user_id):
                # Eliminación exitosa, puedes realizar cualquier acción adicional que desees
                response = {
                    "message": "Usuario eliminado exitosamente"
                }
                return jsonify(response), 200  # 200 OK
            else:
                error_response = {
                    "message": "Error al eliminar al usuario"
                }
                return jsonify(error_response), 400  # 400 Bad Request (puedes personalizar el código de estado según tus necesidades)
        except Exception as e:
            error_response = {
                "message": "Error al eliminar al usuario",
                "error": str(e)
            }
            return jsonify(error_response), 500  # 500 Internal Server Error
