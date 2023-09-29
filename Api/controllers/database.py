import mysql.connector

class DatabaseConnection:
    _connection = None
    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._connection = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3306,
            password="root",
            database="michicode"
            )
        return cls._connection
    
    
    
    @classmethod
    def execute_query(cls,query,params=None):
        cursor = cls.get_connection().cursor()
        cursor.execute(query,params)
        cls._connection.commit()
        return cursor
    
    
    @classmethod
    def fetch_one(cls,query,params=None):
        cursor = cls.get_connection().cursor()
        cursor.execute(query,params)
        return cursor.fetchone()
    
    
    @classmethod
    def get_user_by_email_and_password(cls, email, password):
        query = "SELECT * FROM usuarios WHERE email = %s AND contrasenia = %s"
        params = (email, password)
        result = cls.fetch_one(query, params)
        return result
    
    
    
    @classmethod
    def close_connection(cls):
        if cls.connection is not None:
            cls._connection.close()
            cls._connection = None
            