from flask import Flask,jsonify,render_template,request,redirect,url_for,session
from config import Config
from .models.Users import User
from flask_cors import CORS
from .routes.auth_bp import AuthBlueprint
from .models.Servers import Server
from .routes.user_bp import userbp
from .routes.channel_bp import channel_bp
from .routes.server_bp import serverbp
from .routes.error_handler import errors
from .models.exceptions import NotFound,BadRequest,Forbidden,ServerError
def init_app():
    app = Flask(__name__,static_folder=Config.STATICS_FOLDER,template_folder=Config.TEMPLATES_FOLDER)
    app.config.from_object(Config)
    CORS(app,supports_credentials=True)
    
    auth_bp = AuthBlueprint('auth', __name__)

    app.register_blueprint(auth_bp.bp)
    app.register_blueprint(serverbp)
    app.register_blueprint(channel_bp)
    app.register_blueprint(userbp)
    app.register_blueprint(errors)

    @app.route("/login",methods=["GET","POST"])
    def login():
        try:
            if request.method == 'POST':
                    email_username = request.form.get('email_username')
                    contrasenia = request.form.get('contrasenia')
                    verificado, user_id = User.verificar_credenciales(email_username, contrasenia)
                    if verificado:
                        session["user_id"] = user_id
                        session['email_username'] = email_username
                        session["contrasenia"] = contrasenia
                        return redirect(url_for('muro'))
        except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        return render_template("login.html")
    

    @app.route("/formulario", methods=["GET","POST"])
    def show_form():
        if request.method == "POST":
            return redirect("/inicio")
        return render_template("form.html")



    @app.route("/inicio", methods=["GET","POST"])
    def muro():
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
                imagen_servidor = request.files["imagenServidor"]

                servidor = Server(nombre=nombre_servidor, created_by=id_usuario)
                if servidor.create_server(imagen_servidor):

                    return redirect(url_for("muro"))
                else:
                    return jsonify({'success': False, 'error': 'Error al crear el servidor'})

            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
    
    return app
    