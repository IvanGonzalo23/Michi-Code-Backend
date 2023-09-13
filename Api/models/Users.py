from ..controllers.database import DatabaseConnection
from flask_bcrypt import Bcrypt,check_password_hash

bcrypt = Bcrypt()

class User:
    def __init__(self, username=None, name=None, lastname=None, password=None, fecha=None, email=None, id_user=None):
        self.username = username
        self.name = name
        self.lastname = lastname
        self.password = password
        self.fecha = fecha
        self.email = email
        self.id_user = id_user

    def create_user(self):
        hashed_password = bcrypt.generate_password_hash(self.password).decode('utf-8')
        query = "INSERT INTO michicode.usuarios(username, nombre, lastname, contrasenia, fecha_de_nacimiento, email) VALUES (%s, %s, %s, %s, %s, %s) "
        params = (self.username, self.name, self.lastname, hashed_password, self.fecha, self.email)
        try:
            DatabaseConnection.execute_query(query, params)
            
            user_id_query = "SELECT LAST_INSERT_ID()"
            user_id = DatabaseConnection.fetch_one(user_id_query)[0]
            
            return user_id
        except Exception as e:
            raise e
    
    
    def verificar_credenciales(email_username, contrasenia):
        try:
            query = "SELECT id, email, username, contrasenia FROM usuarios WHERE (email = %s OR username = %s)"
            params = (email_username, email_username)
            result = DatabaseConnection.fetch_one(query, params)

            if result is not None:
                id_user, stored_email, stored_username, stored_password_hash = result
                if (
                    stored_email == email_username or stored_username == email_username
                ) and check_password_hash(stored_password_hash, contrasenia):
                    print("Éxito")
                    return True,id_user
                else:
                    print("Contraseña incorrecta")
            else:
                print("Usuario no encontrado")

        except Exception as e:
            print("Error:", str(e))

        return False
