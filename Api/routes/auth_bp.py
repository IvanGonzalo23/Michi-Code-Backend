from flask import Blueprint,render_template
from ..controllers.user_controller import UserController


class AuthBlueprint:
    def __init__(self, name, import_name):
        self.bp = Blueprint(name, import_name)
        self.configure_routes()

    def configure_routes(self):
        @self.bp.route("/", methods=["GET"])
        def index():
            return render_template("index.html")


