from flask import Blueprint,render_template
from ..controllers.database import DatabaseConnection  
from flask_bcrypt import check_password_hash


class AuthBlueprint:
    def __init__(self, name, import_name):
        self.bp = Blueprint(name, import_name)
        self.configure_routes()

    def configure_routes(self):
        @self.bp.route("/", methods=["GET", "POST"])
        def index():
            return render_template("index.html")

        @self.bp.route("/registro", methods=["GET"])
        def form():
            return render_template("form.html")


