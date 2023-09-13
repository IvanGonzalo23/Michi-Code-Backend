from flask import Flask,jsonify,render_template,request,redirect,url_for,session
from config import Config
from .models.Users import User
from .routes.auth_bp import AuthBlueprint
from .models.Servers import Server


def init_app():
    app = Flask(__name__,static_folder=Config.STATICS_FOLDER,template_folder=Config.TEMPLATES_FOLDER)
    app.config.from_object(Config)
    
    
    auth_bp = AuthBlueprint('auth', __name__)

    app.register_blueprint(auth_bp.bp)
    
    @app.route("/login",methods=["GET","POST"])
    def login():
        if request.method == 'POST':
                email_username = request.form.get('email_username')
                contrasenia = request.form.get('contrasenia')
                verificado, user_id = User.verificar_credenciales(email_username, contrasenia)
                if verificado:
                    session["user_id"] = user_id
                    session['email_username'] = email_username
                    session["contrasenia"] = contrasenia
                    return redirect(url_for('muro'))

        return render_template("login.html")
    
    @app.route("/inicio", methods=["GET","POST"])
    def muro():
        
        """
        Despues del logeo recibe los datos del usuario, pero si crea un usuario y entra
        recibira el ID del usuario recien creado pero no el nombre o correo, en este caso
        recibira el nombre o correo del usuario anterior, este error me gustaria que puedas revisar
        
        """
        
        
        if request.method == "GET":
            email_username = session.get('email_username')
            id_usuario = session.get("user_id")
        
            if email_username:
                print(f"id: {id_usuario}")
                print(f"Usuario/email: {email_username}")
                return render_template('inicio.html')
            else:
                return redirect('/login')
        elif request.method == "POST":
            id_usuario = session.get("user_id")
            try:
                nombre_servidor = request.form.get('nombreServidor')

                servidor = Server(nombre=nombre_servidor, created_by=id_usuario)
                if servidor.create_server():
                    return redirect(url_for("muro"))
                else:
                    return jsonify({'success': False, 'error': 'Error al crear el servidor'})

            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})





        
        
        
    @app.route("/createuser",methods=["POST"])
    def create():
        """
        
            Recibe la informacion del formulario y la pone dentro de los parametros de la clase User para luego
            crear el usuario con la funcion create_user
            (hay un problema que no logro encontrar, cuando creo el usuario tambien guardo el id creado para despues
            ponerlo en el muro o en la pantalla principal, pero en los print puestos aparece el nombre del usuario anterior
            y no el usuario recien creado, necesitare que puedas ver eso)
        
        """
        try:
            new_username = request.form.get("username")
            new_email = request.form.get("email")
            new_name = request.form.get("nombre")
            new_lastname = request.form.get("apellido")
            new_dia = request.form.get("dia")
            new_mes = request.form.get("mes")
            new_anio = request.form.get("ano")
            new_password = request.form.get("password")
            
            new_user = User(username=new_username,
                            name=new_name,
                            lastname=new_lastname,
                            fecha=f"{new_anio}-{new_mes}-{new_dia}",
                            email=new_email,
                            password=new_password)
            
            user_id = new_user.create_user()
            session["user_id"] = user_id
            return redirect(url_for('muro'))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app