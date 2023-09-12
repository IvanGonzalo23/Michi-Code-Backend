from flask import Flask,jsonify,render_template,request,redirect,url_for,session
from config import Config
from .models.Users import User
from .routes.auth_bp import AuthBlueprint


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
                
                if User.verificar_credenciales(email_username, contrasenia):
                    session['email_username'] = email_username
                    session["contrasenia"] = contrasenia
                    return redirect(url_for('muro'))

        return render_template("login.html")
    
    @app.route("/inicio", methods=["GET","POST"])
    def muro():
        
        email_username = session.get('email_username')
    
        if email_username:
            print(f"Usuario/email: {email_username}")
            return render_template('inicio.html')
        else:
            return redirect('/login')
        
    @app.route("/createuser",methods=["POST"])
    def create():
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
            
            new_user.create_user()
            return redirect(url_for('muro'))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app
    