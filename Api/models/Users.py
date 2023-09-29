from ..controllers.database import DatabaseConnection
from flask_bcrypt import Bcrypt,check_password_hash

bcrypt = Bcrypt()

class User:
    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.name = kwargs.get("name")
        self.lastname = kwargs.get("lastname")
        self.password = kwargs.get("password")
        self.fecha = kwargs.get("fecha")
        self.email = kwargs.get("email")
        self.id_user = kwargs.get("user_id")



    def serialize(self):
        return{
            "username":self.username,
            "name":self.name,
            "lastname":self.lastname,
            "password":self.password,
            "fecha":self.fecha,
            "email":self.email,
            "user_id":self.id_user
        }

    @classmethod
    def create_user(cls, username, name, lastname, password, fecha, email):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        query = "INSERT INTO michicode.usuarios(username, nombre, lastname, contrasenia, fecha_de_nacimiento, email) VALUES (%s, %s, %s, %s, %s, %s) "
        params = (username, name, lastname, hashed_password, fecha, email)
        try:
            DatabaseConnection.execute_query(query, params)

            user_id_query = "SELECT LAST_INSERT_ID()"
            user_id = DatabaseConnection.fetch_one(user_id_query)[0]

            # Crea una instancia de la clase User y devuelve el usuario creado
            new_user = cls(username=username, name=name, lastname=lastname, password=hashed_password, fecha=fecha, email=email, id_user=user_id)
            return new_user
        except Exception as e:
            raise e
    
    @classmethod
    def verificar_credenciales(cls,email_username, contrasenia):
        query = "SELECT id, email, username, contrasenia,nombre,lastname,fecha_de_nacimiento FROM usuarios WHERE (email = %s OR username = %s)"
        params = (email_username, email_username)
        result = DatabaseConnection.fetch_one(query, params)

        if result is not None:
            id_user, stored_email, stored_username, stored_password_hash, name, lastname, fecha = result
            if (
                stored_email == email_username or stored_username == email_username
            ) and check_password_hash(stored_password_hash, contrasenia):
                return cls(
                    id_user=id_user,
                    username=stored_username,
                    email=stored_email,
                    name=name,
                    lastname=lastname,
                    fecha=fecha,
                    password = stored_password_hash
                )  

        return False

    @classmethod
    def get_user_by_id(cls, user_id):
        query = "SELECT id, username, nombre, lastname, fecha_de_nacimiento, email FROM usuarios WHERE id = %s"
        params = (user_id,)
        
        try:
            result = DatabaseConnection.fetch_one(query, params)
            if result:
                id, username, name, lastname, fecha, email = result
                return cls(
                    id_user=id,
                    username=username,
                    name=name,
                    lastname=lastname,
                    fecha=fecha,
                    email=email
                )
            return None  # No se encontró el usuario
        except Exception as e:
            raise e


    @classmethod
    def update_user(cls, id_usuario, nuevo_username, nueva_contrasenia):
        try:
            # Comprobar si el nuevo username ya está en uso
            username_exists_query = "SELECT id FROM usuarios WHERE username = %s"
            params = (nuevo_username,)
            existing_user_id = DatabaseConnection.fetch_one(username_exists_query, params)

            if existing_user_id:
                raise Exception("El nuevo nombre de usuario ya está en uso")

            # Generar el hash de la nueva contraseña
            nueva_contrasenia_hash = bcrypt.generate_password_hash(nueva_contrasenia).decode('utf-8')

            # Actualizar el nombre de usuario y la contraseña
            update_query = "UPDATE usuarios SET username = %s, contrasenia = %s WHERE id = %s"
            params = (nuevo_username, nueva_contrasenia_hash, id_usuario)
            DatabaseConnection.execute_query(update_query, params)

            return True  # Cambio de credenciales exitoso
        except Exception as e:
            raise e
    

    @classmethod
    def delete_user(cls, user_id):
        try:
            # Verificar si el usuario existe
            user = cls.get_user_by_id(user_id)
            if not user:
                raise Exception("Usuario no encontrado")

            # Eliminar al usuario de la base de datos
            delete_query = "DELETE FROM usuarios WHERE id = %s"
            params = (user_id,)
            DatabaseConnection.execute_query(delete_query, params)

            return True  # Eliminación exitosa
        except Exception as e:
            raise e
